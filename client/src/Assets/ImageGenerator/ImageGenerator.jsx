import React, { useState, useEffect } from 'react'
import './ImageGenerator.css'
import OpenAI from "openai";
const openai = new OpenAI({ apiKey: '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', dangerouslyAllowBrowser: true });
// const openai = new OpenAI();

const ImageGenerator = () => {
    const [image_url, setImage_url] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
   
    console.log(process.env.REACT_APP_API_KEY);
    
    
    const imageGenerator = async () =>{
        setIsLoading(true);
        try {
        // Fetch the prompt from your backend
        const promptResponse = await fetch('http://localhost:5000/g-prompt'); // Adjust the URL as needed
        if (!promptResponse.ok) {
            throw new Error('Network response was not ok.');
        }
        
        const promptData = await promptResponse.json();
        const prompt = promptData.prompt;

        const image = await openai.images.generate({ model: "dall-e-3", prompt });
        
        console.log(image.data[0].url);
        setImage_url(image.data[0].url); // Update this based on actual response property
        setIsLoading(false);

        // call OpenAI's API with the fetched prompt
        
        const response = await fetch(
             "https://api.openai.com/v1/images/generations",
             {
                 method:"POST",
                 headers:{
                     "Content-Type":"application/json",
                     Authorization: `Bearer ${process.env.REACT_APP_OPENAI_API_KEY}`
                 },
                 body:JSON.stringify({
                     prompt: prompt, //prompt should be coming from the backend depending on the person's emotion 
                     n:1,
                     size:"512x512",
                 }), 
             });
             if (!response.ok) {
                 throw new Error('Network response was not ok.');
             }
         const data = await response.json();
         console.log(data);
        


        // Assuming the API returns a direct link to the image
        // Update the following line according to the actual response structure from the API
        // setImage_url(data.data.images[0].url); // Update this based on actual response property
        //setImage_url(data.data.images[0]);
    } catch (error) {
        console.error('There was an error!', error);
    } finally {
        setIsLoading(false);
    }
};


    return (
        <div className='ai-image-generator'>
            <div className="header">Emotion AI <span>Visualization</span></div>
            <div className="img-loading">
                {isLoading ? <p>Loading...</p> :
                    <div className="image">
                        <img src={image_url}/>
                    </div>
                }
            </div>
            <p>This artwork is generated from your brainwave signals:</p>
            <div className="generate-btn" onClick={imageGenerator}>Request Image</div>
            {/* <div className="generate-btn" onClick={imageGenerator}>Generate</div> */}
        </div>
    );
};

export default ImageGenerator
