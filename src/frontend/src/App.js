import React, { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [study_subject, set_study_subject] = useState("");

  const [subJsons, setSubJsons] = useState([]);

  const [loading, set_loading] = useState(false);

  const handleSubmit = () => {
    set_loading(true);
    // Send the inputValue to the Flask backend
    fetch(`http://127.0.0.1:5000/course_advisor/query?param=${study_subject}`, {
      method: "GET",
    })
      .then((response) => response.json())
      .then((data) => {
        setSubJsons(data);

        console.log("Response from Flask backend:", data);
      })
      .catch((error) => {
        console.error("Error:", error);
      })
      .finally(() => {
        set_loading(false);
      });
  };

  return (
    <div className="App">
      <header className="App-header">
        <p>I am interested in studying... </p>
        <input
          type="text"
          placeholder="Computer Science"
          value={study_subject}
          onChange={(e) => set_study_subject(e.target.value)}
        />
        <button onClick={handleSubmit}>Submit</button>

        {/* Display the subJsons data */}
        {loading ? (
          <p>Loading...</p>
        ) : (
          subJsons.map((subJson) => (
            <div key={subJson.id} className="sticky-tab">
              {subJson.name}
            </div>
          ))
        )}
      </header>
    </div>
  );
}

export default App;
