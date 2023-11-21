from io import BytesIO

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS, cross_origin

from utils import format_program
from docxtpl import DocxTemplate

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

specialties = [
    {
        "id": 1,
        "code": "09.02.06",
        "value": "Сетевое и системное администрирование"
    },
    {
        "id": 2,
        "code": "09.02.06",
        "value": "Информационные системы и программирование"
    }
]

disciplines = [
    {
        "id": 1,
        "specialties": [1, 2],
        "value": "Информатика"
    },
    {
        "id": 2,
        "specialties": [1],
        "value": "Разработка программного обеспечения"
    },
]

competencies = [
    {
        "id": 1,
        "title": "ПК 01",
        "type": "practicial",
        "specialties": [1]
    },
    {
        "id": 2,
        "type": "general",
        "title": "ОК 01",
        "specialties": [1, 2]
    }
]


@app.get("/api/disciplines")
@cross_origin()
def send_disciplines():
    return jsonify(disciplines)


@app.get("/api/specialties")
@cross_origin()
def send_specialties():
    return jsonify(specialties)


@app.get("/api/speciality_disciplines/<int:ID>")
@cross_origin()
def send_disciplines_by_id(ID: int):
    founded_disciplines = []

    for discipline in disciplines:
        if ID in discipline["specialties"]:
            founded_disciplines.append(discipline)

    if len(founded_disciplines) == 0:
        return jsonify({"message": "Дисциплины указанной специальности не найдены"})

    else:
        return jsonify(founded_disciplines)


@app.get("/api/speciality_competencies/<int:ID>")
def send_competencies_by_id(ID: int):
    founded_competencies = []

    for competency in competencies:
        if ID in competency["specialties"]:
            founded_competencies.append(competency)

    if len(founded_competencies) == 0:
        return jsonify({"message": "Дисциплины указанной специальности не найдены"})

    else:
        return jsonify(founded_competencies)


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
