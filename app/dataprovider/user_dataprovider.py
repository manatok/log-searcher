from app.model.user import User

# This is just for demo purposes and would ultimately live in the database
test_users = [
    {
        "id": 1,
        "email": "site1@test.com",
        "password": "test",
        "allowed_site_ids": ["site1", "site11"]
    },
    {
        "id": 2,
        "email": "site2@test.com",
        "password": "test",
        "allowed_site_ids": ["site2", "site22"]
    }
]


def get_user_by(column: str, value: str) -> User:
    """
    This is just a demo function for getting a User entity.
    This would be replaced when integrating with a real DB.
    """
    for user in test_users:
        if user[column] == value:
            return User(user["id"], user["email"], user["password"],
                        user["allowed_site_ids"])

    return None
