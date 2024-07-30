# localhost:5000 - address
# anything after 5000 is the endpoint, so localhost:5000/home is the home endpoint
# when a request is submitted, data needs to be sent with the endpoint
# google.com - domain/url
# request - anything sent to the server, such as an API call
# Requests have types:
# GET - Access a resource
# POST - Create something new 
# PUT/PATCH - Update something
# DELETE - Delete something 
# json - Information that comes alongside the request 
# Backend returns response, containing a few things:
# STATUS - 200 = success
# STATUS - 404 = error not found
# STATUS - 400 = bad request 
# STATUS - 403 = forbidden/unauthorized
# can also return json

from flask import request, jsonify
from config import app, db 
from models import Contact

# Define the route for getting all contacts
@app.route("/contacts", methods=["GET"])
def get_contacts():
    # Query all contacts from the database
    contacts = Contact.query.all()
    # Convert the list of Contact objects to a list of JSON objects
    json_contacts = list(map(lambda x: x.to_json(), contacts))
    # Return the list of JSON objects as a JSON response
    return jsonify({"contacts": json_contacts})

# Define the route for creating a new contact
@app.route("/create_contact", methods=["POST"])
def create_contact():
    # Get the first name, last name, and email from the request JSON
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")
    email = request.json.get("email")

    # If any of these fields are missing, return an error message
    if not first_name or not last_name or not email:
        return (
            jsonify({"message": "You must include a first name, last name, and email"}), 400,
        )
    
    # Create a new Contact object
    new_contact = Contact(first_name=first_name, last_name=last_name, email=email)
    try:
        # Add the new contact to the database session
        db.session.add(new_contact)
        # Commit the session to write to the database
        db.session.commit()
    except Exception as e:
        # If there's an error, return the error message
        return jsonify({"message": str(e)}), 400
    
    # If successful, return a success message
    return jsonify({"message": "User created"}), 201

# Define the route for updating an existing contact
@app.route("/update_contact/<int:user_id>", methods=["PATCH"])
def update_contact(user_id):
    # Get the contact by user_id
    contact = Contact.query.get(user_id)

    # If the contact doesn't exist, return an error message
    if not contact:
        return jsonify({"message": "User not found"}), 404

    # Get the data from the request JSON
    data = request.json
    # Update the contact's attributes
    contact.first_name = data.get("firstName", contact.first_name)
    contact.last_name = data.get("lastName", contact.last_name)
    contact.email = data.get("email", contact.email)

    # Commit the changes to the database
    db.session.commit()

    # Return a success message
    return jsonify({"message": "User updated."}), 200

# Define the route for deleting a contact
@app.route("/delete_contact/<int:user_id>", methods=["DELETE"])
def delete_contact(user_id):
    # Get the contact by user_id
    contact = Contact.query.get(user_id)

    # If the contact doesn't exist, return an error message
    if not contact:
        return jsonify({"message": "User not found"}), 404

    # Delete the contact from the database
    db.session.delete(contact)
    # Commit the changes to the database
    db.session.commit()

    # Return a success message
    return jsonify({"message": "User deleted!"}), 200

# Main block to run the app
if __name__ == "__main__":
    # Create all database tables
    with app.app_context():
        db.create_all()

    # Run the app in debug mode
    app.run(debug=True)
