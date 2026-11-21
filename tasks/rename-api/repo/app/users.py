USERS = {
    1: {"name": "Alice", "email": "alice@example.com", "admin": True},
    2: {"name": "Bob", "email": "bob@example.com", "admin": False},
}


def fetch_usr(user_id: int) -> dict:
    if user_id not in USERS:
        raise KeyError(f"unknown user {user_id}")
    return USERS[user_id]
