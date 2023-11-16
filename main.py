from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

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
        "disciplines": [1]
    },
    {
        "id": 2,
        "type": "general",
        "title": "ОК 01",
        "disciplines": [1, 2]
    }
]


@app.get("/disciplines")
@cross_origin()
def send_disciplines():
    return jsonify(disciplines)


@app.get("/specialties")
@cross_origin()
def send_specialties():
    return jsonify(specialties)


@app.get("/speciality_disciplines/<int:ID>")
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


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
