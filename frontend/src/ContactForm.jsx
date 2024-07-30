import { useState } from "react";

// ContactForm component for creating or updating a contact
const ContactForm = ({ existingContact = {}, updateCallback }) => {
    // State to manage the form input values
    const [firstName, setFirstName] = useState(existingContact.firstName || "");
    const [lastName, setLastName] = useState(existingContact.lastName || "");
    const [email, setEmail] = useState(existingContact.email || "");

    // Check if we are updating an existing contact or creating a new one
    const updating = Object.entries(existingContact).length !== 0;

    // Function to handle form submission
    const onSubmit = async (e) => {
        e.preventDefault(); // Prevent the default form submission behavior

        // Collect form data into an object
        const data = {
            firstName,
            lastName,
            email
        };

        // Determine the URL and HTTP method based on whether we are updating or creating a contact
        const url = "http://127.0.0.1:5000/" + (updating ? `update_contact/${existingContact.id}` : "create_contact");
        const options = {
            method: updating ? "PATCH" : "POST",
            headers: {
                "Content-Type": "application/json" // Indicate that we are sending JSON data
            },
            body: JSON.stringify(data) // Convert data object to JSON string
        };

        // Send the request to the server
        const response = await fetch(url, options);

        // Check if the response status indicates an error
        if (response.status !== 201 && response.status !== 200) {
            const data = await response.json(); // Parse the response JSON
            alert(data.message); // Show error message
        } else {
            // Call the updateCallback function to refresh data (e.g., close modal, refresh contact list)
            updateCallback();
        }
    };

    return (
        // Form for creating or updating a contact
        <form onSubmit={onSubmit}>
            <div>
                <label htmlFor="firstName">First Name:</label>
                <input
                    type="text"
                    id="firstName"
                    value={firstName}
                    onChange={(e) => setFirstName(e.target.value)} // Update firstName state on input change
                />
            </div>
            <div>
                <label htmlFor="lastName">Last Name:</label>
                <input
                    type="text"
                    id="lastName"
                    value={lastName}
                    onChange={(e) => setLastName(e.target.value)} // Update lastName state on input change
                />
            </div>
            <div>
                <label htmlFor="email">Email:</label>
                <input
                    type="text"
                    id="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)} // Update email state on input change
                />
            </div>
            {/* Submit button with text based on whether we are updating or creating */}
            <button type="submit">{updating ? "Update" : "Create"}</button>
        </form>
    );
};

export default ContactForm;
