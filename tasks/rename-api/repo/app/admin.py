from app import users


def is_admin(user_id: int) -> bool:
    return users.fetch_usr(user_id)["admin"]
