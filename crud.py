from dotenv import load_dotenv
from os import getenv
from supabase import Client, create_client

_client: None | Client = None


def _init_supabase():
    global _client

    _url = getenv("SUPABASE_URL")
    _key = getenv("SUPABASE_KEY")
    _client = create_client(_url, _key)


load_dotenv()
_init_supabase()


def get_all_specialties():
    response = _client.table("specialties").select("*").execute()

    for item in response.data:
        item.pop("created_at", None)

    return response.data


def get_all_disciplines():
    response = _client.table('disciplines').select("*").execute()
    return response.data


def get_specialty_disciplines(id: int):
    response = _client.table("specialties_disciplines").select("disciplines(id, value)").eq("specialty_id", id).execute()
    response_list = []

    for item in response.data:
        response_list.append(item.get("disciplines"))

    return response_list


def get_specialty_competencies(id: int):
    response = _client.table("specialties_competencies").select("specialty_id, competencies(id, value, competency_type(value))").eq("specialty_id", id).execute()
    response_list = []

    for item in response.data:
        item.get("competencies")["type"] = item.get("competencies").get("competency_type").get("value")
        item.get("competencies").pop("competency_type", None)
        response_list.append(item.get("competencies"))

    return response_list
