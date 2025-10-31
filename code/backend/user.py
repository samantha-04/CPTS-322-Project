class User:
    def __init__(self, user_id, username, email, password):
        """
        Initialize a User object.

        :param user_id: Unique identifier for the user
        :param username: Username of the user
        :param email: Email address of the user
        """
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password # In final application, make sure to hash this
    
    def check_password(self, password):
        """
        Check if the provided password matches the user's password.

        :param password: Password to check
        :return: True if the password matches, False otherwise
        """
        return self.password == password  # In final application, use hashed password comparison
    
    
    def questionAnswer(self, question):
        self.question = question
   