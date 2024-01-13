import React, { useState } from 'react'
import './ImageGenerator.css'
import default_image from './default_image.svg'

const ImageGenerator = () => {
    const [image_url, setImage_url] = useState("/")

    const imageGenerator = async () =>{
        // Fetch the prompt from your backend
        const promptResponse = await fetch('http://localhost:5000/generate-prompt'); // Adjust the URL as needed
        const promptData = await promptResponse.json();
        const prompt = promptData.prompt;


        // call OpenAI's API with the fetched prompt
        // https://www.youtube.com/watch?v=PZG2MvOjud0&t=2s for more info
        const response = await fetch(
            "https://api.openai.com/v1/images/generations",
            {
                method:"POST",
                headers:{
                    "Content-Type":"application/json",
                    Authorization:
                    `Bearer ${process.env.REACT_APP_OPENAI_API_KEY}`,
                    "User-Agent":"Chrome",
                },
                body:JSON.stringify({
                    prompt: prompt, //prompt should be coming from the backend depending on the person's emotion 
                    n:1,
                    size:"512x512",
                }), 
            }
        );
        const data = await response.json();
        console.log(data);

        // Assuming the API returns a direct link to the image
        // Update the following line according to the actual response structure from the API
        setImage_url(data.image_url); // Update this based on actual response property
        //setImage_url(data.data.images[0]);
    }


  return (
    <div className='ai-image-generator'>
        <div className="header">Emotion <span>Visualization</span></div>
        <div className="img-loading">
            <div className="image"><img src={image_url==="/"?default_image:image_url} alt="" /></div>
        </div>
        <div className="generate-btn" onClick={()=>{imageGenerator()}}>Generate</div>

    </div>
  )
}

export default ImageGenerator
