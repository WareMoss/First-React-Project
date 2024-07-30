import { useState, useEffect } from "react";
import ContactList from "./ContactList";
import "./App.css";
import ContactForm from "./ContactForm";

function App() {
  // State to hold the list of contacts
  const [contacts, setContacts] = useState([]);
  
  // State to manage the modal's open/close status
  const [isModalOpen, setIsModalOpen] = useState(false);
  
  // State to hold the current contact being edited or created
  const [currentContact, setCurrentContact] = useState({});

  // Fetch contacts when the component mounts
  useEffect(() => {
    fetchContacts();
  }, []);

  // Function to fetch contacts from the server
  const fetchContacts = async () => {
    const response = await fetch("http://127.0.0.1:5000/contacts");
    const data = await response.json();
    setContacts(data.contacts);
  };

  // Function to close the modal
  const closeModal = () => {
    setIsModalOpen(false);
    setCurrentContact({});
  };

  // Function to open the modal for creating a new contact
  const openCreateModal = () => {
    if (!isModalOpen) setIsModalOpen(true);
  };

  // Function to open the modal for editing an existing contact
  const openEditModal = (contact) => {
    if (isModalOpen) return;
    setCurrentContact(contact);
    setIsModalOpen(true);
  };

  // Callback function to refresh the contact list after an update
  const onUpdate = () => {
    closeModal();
    fetchContacts();
  };

  return (
    <>
      {/* Render the contact list and pass necessary props */}
      <ContactList contacts={contacts} updateContact={openEditModal} updateCallback={onUpdate} />
      
      {/* Button to create a new contact */}
      <button onClick={openCreateModal}>Create New Contact</button>
      
      {/* Modal for creating or editing a contact */}
      {isModalOpen && <div className="modal">
        <div className="modal-content">
          {/* Close button for the modal */}
          <span className="close" onClick={closeModal}>&times;</span>
          
          {/* Render the contact form and pass necessary props */}
          <ContactForm existingContact={currentContact} updateCallback={onUpdate} />
        </div>
      </div>}
    </>
  );
}

export default App;
