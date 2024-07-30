import React from 'react'; // Import the React library
import ReactDOM from 'react-dom/client'; // Import the ReactDOM library for rendering
import App from './App.jsx'; // Import the main App component
import './index.css'; // Import global styles

// Create a root for the React application and render the App component
ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    {/* Wrap the App component with React.StrictMode for additional checks and warnings */}
    <App />
  </React.StrictMode>,
);
