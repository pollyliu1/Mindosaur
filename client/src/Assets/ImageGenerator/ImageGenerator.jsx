import React, { useState, useEffect } from 'react'
import './ImageGenerator.css'
import OpenAI from "openai";
const openai = new OpenAI({ apiKey: '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', dangerouslyAllowBrowser: true });
// const openai = new OpenAI();

const ImageGenerator = () => {
    const [image_url, setImage_url] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    
    const createSpotifyPlaylist = async () => {
        const accessToken = localStorage.getItem('accessToken');
        const response = await fetch('https://api.spotify.com/v1/users/user_id/playlists', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${accessToken}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: 'Your Brainwave Playlist',
                description: 'A playlist generated from your brainwave signals',
                public: false, // or true, based on your requirement
            }),
        });

        const data = await response.json();
        console.log(data);

    };
    

    console.log(process.env.REACT_APP_API_KEY);
    const imageGenerator = async () =>{
        setIsLoading(true);
        try {
        // Fetch the prompt from your backend
        const promptResponse = await fetch('http://localhost:5000/generate-prompt'); // Adjust the URL as needed
        if (!promptResponse.ok) {
            throw new Error('Network response was not ok.');
        }
        
        const promptData = await promptResponse.json();
        const prompt = promptData.prompt;

        // const image = await openai.images.generate({ model: "dall-e-3", prompt });
        const image = {data: [{url: "https://oaidalleapiprodscus.blob.core.windows.net/private/org-pT7nPmAkjnDXak3j0HveBGgU/user-V0W153PV7N2G4EIQdGlKK1ZK/img-0KF5SEycnsImifp5c1HEj5la.png?st=2024-01-14T02%3A36%3A54Z&se=2024-01-14T04%3A36%3A54Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-01-13T04%3A39%3A51Z&ske=2024-01-14T04%3A39%3A51Z&sks=b&skv=2021-08-06&sig=t9sZYYXsx0YJQ8GFRWEQ/GbB%2BkyrB%2B5NPZd%2B8jcU7sM%3D"}]}

        console.log(image.data[0].url);
        setImage_url(image.data[0].url); // Update this based on actual response property
        setIsLoading(false);

        // call OpenAI's API with the fetched prompt
        // https://www.youtube.com/watch?v=PZG2MvOjud0&t=2s for more info
        // const response = await fetch(
        //     "https://api.openai.com/v1/images/generations",
        //     {
        //         method:"POST",
        //         headers:{
        //             "Content-Type":"application/json",
        //             Authorization: `Bearer ${process.env.REACT_APP_OPENAI_API_KEY}`
        //         },
        //         body:JSON.stringify({
        //             prompt: prompt, //prompt should be coming from the backend depending on the person's emotion 
        //             n:1,
        //             size:"512x512",
        //         }), 
        //     });
        //     if (!response.ok) {
        //         throw new Error('Network response was not ok.');
        //     }
        // const data = await response.json();
        // console.log(data);
        


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
}

export default ImageGenerator
