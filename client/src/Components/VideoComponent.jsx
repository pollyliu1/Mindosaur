import React, { useState, useEffect } from 'react';
import './VideoComponent.css'; // Import the CSS file for styling
import Animation from '../Assets/Animation.mp4';

const VideoComponent = () => {
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    // set a timeout to change the state AFTER 3 SECONDS 
    const timer = setTimeout(() => setIsVisible(false), 6000);

    return () => clearTimeout(timer); 
  }, []);

  return (
    <div className={isVisible ? 'video-container' : 'video-container fade-out'}>
      <video width="1920" height="1080" autoPlay muted loop>
      <source src={Animation} type="video/mp4" />
      Your browser does not support the video tag.
    </video>
    </div>
  );
};

export default VideoComponent;
