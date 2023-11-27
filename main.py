from io import BytesIO

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS, cross_origin

from utils import format_program
from docxtpl import DocxTemplate

from crud import get_all_disciplines, get_specialty_disciplines, get_specialty_competencies, get_all_specialties

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.get("/test")
def t_test():
    _disciplines = get_all_disciplines()
    return jsonify(_disciplines)


@app.get("/api/disciplines")
@cross_origin()
def send_disciplines():
    return jsonify(get_all_disciplines())


@app.get("/api/specialties")
@cross_origin()
def send_specialties():
    return jsonify(get_all_specialties())


@app.get("/api/speciality_disciplines/<int:id>")
@cross_origin()
def send_disciplines_by_id(id: int):
    _disciplines = get_specialty_disciplines(id)

    if len(_disciplines) == 0:
        return jsonify({"message": "Дисциплины указанной специальности не найдены"})

    return jsonify(_disciplines)


@app.get("/api/speciality_competencies/<int:id>")
def send_competencies_by_id(id: int):
    _competencies = get_specialty_competencies(id)

    if len(_competencies) == 0:
        return jsonify({"message": "Компетенции указанной специальности не найдены"})

    else:
        return jsonify(_competencies)


def process_program(program: dict):
    program = format_program(program)
    buffer = BytesIO()

    template = DocxTemplate("templates/template.docx")
    template.render(program)

    template.save(buffer)
    buffer.seek(0)

    return buffer


@app.post("/api/generate")
@cross_origin()
def generate_document():
    program = request.get_json()
    file_to_send = process_program(program)

    return send_file(file_to_send, download_name="generated.docx")


if __name__ == "__main__":
    app.run()
