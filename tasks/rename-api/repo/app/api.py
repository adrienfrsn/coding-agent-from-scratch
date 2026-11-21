from app.users import fetch_usr


def user_profile(user_id: int) -> dict:
    user = fetch_usr(user_id)
    return {"id": user_id, "name": user["name"]}
