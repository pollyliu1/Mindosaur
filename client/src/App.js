import React from 'react';
import './App.css';
// Import ImageGenerator component
import ImageGenerator from './ImageGenerator'; // Adjust the path as per your project structure

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Welcome to the EEG Art Generator</h1>
        <p>Experience the fusion of technology and art</p>
      </header>
      <ImageGenerator />
      {/* You can add additional components or content here */}
    </div>
  );
}

export default App;