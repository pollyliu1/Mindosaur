import React, { useState, useEffect } from 'react'
import './ImageGenerator.css'

const ImageGenerator = () => {
    const [image_url, setImage_url] = useState(null);

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
    };

    // fetch default image on component mount 
    useEffect(() => {
        imageGenerator();
    }, []);


  return (
    <div className='ai-image-generator'>
        <div className="header">Emotion AI <span>Visualization</span></div>
        <div className="img-loading">
            <div className="image">
                <img src={image_url} alt="Click generate to see your Spotify playlist!" /></div>
        </div>
        <div className="generate-btn" onClick={()=>{imageGenerator()}}>Generate</div>
        This artwork is generated from your brainwave signals.
        </div>
  )
}

export default ImageGenerator
