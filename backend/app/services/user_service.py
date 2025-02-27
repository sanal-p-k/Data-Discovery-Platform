from models.user import User

class UserService:
    def __init__(self):
        # Mock data for demonstration
        self.users = {
            "admin": User(id=1, username="admin", email="admin@example.com", disabled=False),
        }

    def get_user(self, username: str) -> User:
        """
        Get a user by username.
        """
        return self.users.get(username)

    def authenticate_user(self, username: str, password: str) -> User:
        """
        Authenticate a user.
        """
        user = self.get_user(username)
        if not user:
            return None
        # Mock password check (replace with real implementation)
        if password != "password":
            return None
        return user