## Inspiration
TikTok is scary. It seems to always know what I want to see and gives it to me. While it can't actually know, what if something could? That's why we decided to make Mindy, your companion that actually knows what you want using brain waves. 

## What it does
This app is an EEG (electroencephalogram) based music & art generator. A user puts on a Brain-Computer Interface (BCI) and logs in to the app. As they work in front of their computer or go throughout their day, the user's brainwaves are measured. These differing brainwaves are interpreted as indicative of different moods, for which keywords are then fed into the Stable Diffusion model through prompt engineering. The app uses a custom algorithm to generate music accordingly and produces melodic musical pieces, which are sent back to the user through the web platform. Once you hit generate on the home UI, our front end retrieves DALL-E-generated images from the backend. The backend then uses multithreading to make three simultaneous API calls. First, a call to GPT-3 to condense the chunks into image prompts to be fed into a Stable Diffusion/Deforum AI image generation model. Second, a sentiment keyword analysis using GPT-3, which is then fed to the Spotify API for a fitting playlist generation. 

Mindy can use the EEG signals from a headpiece to approximate your mood. Not only is she a friend to feel and express them with you with servos and an LCD display, but she can also give you content based on this using DALL-E, Spotify, and AI via LLM sentiment analysis. 

## How we built it
We built the project using the OpenBCI kit as the backbone, React and Flask to power our web app, and Arduino to bring our hardware to life. With the help of trips to the dollar store, we created a vessel that perfectly embodies the passion and urgency we have for mental health!

## Challenges we ran into
Working with the OpenBCI kit was a difficult journey. What should have been an easy connection process between the EEG and the backend, was a real Snorlax on the bridge! 

## Accomplishments that we're proud of
We are proud of being able to pull together a project with such a large scope. Our project spans various unfamiliar software frameworks from ECG and biosensing devices, to AI models and Spotify APIs. Finally, after all the various issues we had with API keys and unreliable/outdated documentation, we are proud we even had something that worked. 

## What we learned
Staying up for 24 hours straight is not super healthy. Perhaps we need Mindy's help after this 😭

## What's next for Mindosaur
Our next steps are to improve the web app with data visualization and integrating a database to keep track of your brain activity history. This way, we can build an even stronger understanding towards your own focus habits, and provide solutions to further improve your productivity.
