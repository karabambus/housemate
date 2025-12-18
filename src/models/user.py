class User:
    """SOLID (S): Only represents user data"""

    def __init__(self, user_id, email, password_hash, first_name, last_name):
        self.user_id = user_id
        self.email = email
        self.password_hash = password_hash
        self.first_name = first_name
        self.last_name = last_name

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"