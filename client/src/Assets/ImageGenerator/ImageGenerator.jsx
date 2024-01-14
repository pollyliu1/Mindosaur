import React, { useState, useEffect } from 'react'
import './ImageGenerator.css'

// const openai = new OpenAI();

const ImageGenerator = () => {
    const [imageIndex, setImageIndex] = useState(0);
    const [image_url, setImage_url] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    // define image urls 
    const images = [
        './image1.png', // replace with actual URL for image1
        './image2.png',  // replace with actual URL for image2
    ];

    const imageGenerator = () => {
        setIsLoading(true);
        // Update the image URL based on the imageIndex
        setImage_url(images[imageIndex]);

        // Toggle between 0 and 1 for subsequent clicks
        setImageIndex((prevIndex) => (prevIndex === 0 ? 1 : 0));

        // Simulate a loading delay (if necessary)
        setTimeout(() => {
            setIsLoading(false);
        }, 500); // Adjust the delay time as needed
    };

    return (
        <div className='ai-image-generator'>
            <div className="header">Emotion AI <span>Visualization</span></div>
            <div className="img-loading">
                {isLoading ? <p>Loading...</p> :
                    <div className="image">
                        {image_url && <img src={image_url} alt="Generated Artwork" />}
                    </div>
                }
            </div>
            <p>This artwork is generated from your brainwave signals:</p>
            <div className="generate-btn" onClick={imageGenerator}>Request Image</div>
        </div>
    );
};

export default ImageGenerator
