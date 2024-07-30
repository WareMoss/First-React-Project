import React from "react";

// ContactList component for displaying and managing a list of contacts
const ContactList = ({ contacts, updateContact, updateCallback }) => {
    // Function to handle deleting a contact
    const onDelete = async (id) => {
        try {
            // Define the options for the DELETE request
            const options = {
                method: "DELETE"
            };
            // Send the DELETE request to the server
            const response = await fetch(`http://127.0.0.1:5000/delete_contact/${id}`, options);

            // Check if the response status indicates success
            if (response.status === 200) {
                // Call the updateCallback function to refresh the contact list
                updateCallback();
            } else {
                // Log an error message if the deletion fails
                console.error("Failed to delete");
            }
        } catch (error) {
            // Alert the user in case of a network or server error
            alert(error);
        }
    };

    return (
        <div>
            {/* Header for the contacts list */}
            <h2>Contacts</h2>
            {/* Table to display the contacts */}
            <table>
                <thead>
                    <tr>
                        <th>First Name</th>
                        <th>Last Name</th>
                        <th>Email</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {/* Map through the contacts array to create a table row for each contact */}
                    {contacts.map((contact) => (
                        <tr key={contact.id}>
                            <td>{contact.firstName}</td>
                            <td>{contact.lastName}</td>
                            <td>{contact.email}</td>
                            <td>
                                {/* Button to open the update form for the contact */}
                                <button onClick={() => updateContact(contact)}>Update</button>
                                {/* Button to delete the contact */}
                                <button onClick={() => onDelete(contact.id)}>Delete</button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default ContactList;
