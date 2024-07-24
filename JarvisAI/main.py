import speech_recognition as sr
import os
import webbrowser
import openai
import datetime
import pyttsx3
from config import apikey

# Initialize pyttsx3 for text-to-speech
engine = pyttsx3.init()

def speak(text):
    """Function to convert text to speech"""
    engine.say(text)
    engine.runAndWait()

def chat(query):
    """Function to interact with OpenAI for chatting"""
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"User: {query}\nJarvis: "
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=chatStr,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        response_text = response["choices"][0]["text"].strip()
        speak(response_text)
        chatStr += f"{response_text}\n"
        return response_text
    except openai.error.AuthenticationError:
        speak("Incorrect API key provided. Please check your API key.")
        return "Incorrect API key provided. Please check your API key."

def ai(prompt):
    """Function to interact with OpenAI for AI tasks"""
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        response_text = response["choices"][0]["text"].strip()
        text += response_text
        if not os.path.exists("Openai"):
            os.mkdir("Openai")
        filename = f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt"
        with open(filename, "w") as f:
            f.write(text)
    except openai.error.AuthenticationError:
        speak("Incorrect API key provided. Please check your API key.")

def takeCommand():
    """Function to capture audio input from the user and recognize speech"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            print(f"Error: {str(e)}")
            return "Some Error Occurred. Sorry from Jarvis"

if __name__ == '__main__':
    print('Welcome to Jarvis A.I')
    speak("Jarvis A.I")
    chatStr = ""

    while True:
        query = takeCommand().lower()
        if query == "some error occurred. sorry from jarvis":
            continue

        # List of sites to open
        sites = [
            ["youtube", "https://www.youtube.com"],
            ["wikipedia", "https://www.wikipedia.com"],
            ["google", "https://www.google.com"],
            ["spotify","https://open.spotify.com"]
        ]

        # Open specified sites
        for site in sites:
            if f"open {site[0]}".lower() in query:
                speak(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])

        # Play a specific song
        if "open music" in query:
            musicPath = "D:\\RoiNa.mp3"  # Replace with your music file path
            os.startfile(musicPath)

        # Tell the current time
        elif "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            minute = datetime.datetime.now().strftime("%M")
            speak(f"Sir, the time is {hour} hours and {minute} minutes")

        # Open specific applications
        elif "open python" in query:
            os.system("open /System/Applications/FaceTime.app")
        elif "open pass" in query:
            os.system("open /Applications/Passky.app")

        # Use OpenAI for AI tasks
        elif "using artificial intelligence" in query:
            ai(prompt=query)

        # Quit the program
        elif "jarvis quit" in query:
            exit()

        # Reset the chat history
        elif "reset chat" in query:
            chatStr = ""

        # General chat with OpenAI
        else:
            print("Chatting...")
            chat(query)
