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
        class="apple-input"
          type="text"
          placeholder="Computer Science"
          value={study_subject}
          onChange={(e) => set_study_subject(e.target.value)}
        />
        <button class="apple-button" onClick={handleSubmit}>Submit</button>

        <div className="box-container">
          {loading ? (
            <p>Loading...</p>
          ) : (
            subJsons.map((subJson) => (
              <div key={subJson.id} className="box">
                <div className="box-content">{subJson.code} <br></br>{subJson.description}</div>
              </div>
            ))
          )}
        </div>
      </header>
    </div>
  );
}

export default App;
