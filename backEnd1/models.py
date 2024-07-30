# Import the database object from the configuration module
from config import db

# Define the Contact model, inheriting from db.Model
class Contact(db.Model):
    # Define the id column as an integer primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Define the first_name column as a string of max length 80, non-unique, and non-nullable
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    
    # Define the last_name column as a string of max length 80, non-unique, and non-nullable
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    
    # Define the email column as a string of max length 120, unique, and non-nullable
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Define a method to return a JSON representation of the model
    def to_json(self):
        return {
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
        }
