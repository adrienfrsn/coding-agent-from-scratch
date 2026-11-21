from app.users import fetch_usr as load_user


def welcome_email(user_id: int) -> str:
    user = load_user(user_id)
    return f"To: {user['email']}\nHello {user['name']}!"
