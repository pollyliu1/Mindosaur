import React, { useState } from 'react';
import './App.css';
import VideoComponent from './Components/VideoComponent'; // Adjust the path as per your project structure
import ImageGenerator from './Assets/ImageGenerator/ImageGenerator';
import PreLoader from './Components/PreLoader'
import Animation from './Assets/Animation.mp4';

function App() {

  const [isLoading, setIsLoading] = useState(false);

  const handleGenerate = () => {
    setIsLoading(true);
    setTimeout(() => {
      setIsLoading(false);
    }, 3000); 
  };
  
  return (
    <div className="App">
      <VideoComponent src="./Animation.mp4" />
      <PreLoader />
      <ImageGenerator/>
    </div>
  );
}

export default App;
