import React, { useEffect, useState } from 'react';
import './App.css';

console.log("here")
function App() {
  const [message, setMessage] = useState('');

  console.log("here")
    useEffect(() => {
      const fetchData = async () => {
        try {
          const response = await fetch('http://127.0.0.1:5000/data/'); // Use a relative URL or configure the base URL
          console.log(response);
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          console.log(response);
          const data = await response.json();
          console.log(data)
          setMessage(data.message);
        } catch (error) {
          console.error('Error:', error);
          // You can add error handling here, like setting an error state or showing a message to the user.
        }
      };
    
      fetchData();
    
      return () => {
        // If cleanup is needed when the component unmounts, you can define it here.
      };
    }, []); // Empty dependency array for a one-time effect

  return (
    <div className="App">
      <header className="App-header">
        <p>Message : {message}</p>
      </header>
    </div>
  );
}

export default App;
