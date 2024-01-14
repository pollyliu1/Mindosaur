import React, { useState } from 'react';
import './ImageGenerator.css';
import artImage from './art.jpg';
import image1 from './image1.png';
import image2 from './image2.jpg';

const ImageGenerator = () => {
    const [showImage, setShowImage] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [imageIndex, setImageIndex] = useState(0);
    

    // Define the URL for the image you want to display
    const images = [
        artImage, image1, image2
    ];
    
    const imageGenerator = () => {
        setIsLoading(true);

        // Simulate a loading delay (if necessary)
        setTimeout(() => {
            setImageIndex((ind) => (ind + 1) % images.length);
            setIsLoading(false);
            // setImageIndex((prevIndex) => (prevIndex + 1) % images.length);
        }, 500); // Adjust the delay time as needed
    };

    return (
        <div className='ai-image-generator'>
            <div className="header">Emotion AI <span>Visualization</span></div>
            <div className="img-loading">
                {isLoading ? <p>Loading...</p> :
                    <div className="image">
                        <img src={images[imageIndex]} alt='Random'/>
                        {/* <img src={images[imageIndex]} /> */}
                   </div>
                }
            </div>
            <p>This artwork is generated from your brainwave signals:</p>
            <div className="generate-btn" onClick={imageGenerator}>Request Image</div>
            <iframe src="https://open.spotify.com/embed/playlist/37i9dQZF1EIgG2NEOhqsD7?utm_source=generator" width="100%" height="352" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
        </div>
    );
};

export default ImageGenerator;
