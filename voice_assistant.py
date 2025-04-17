import ollama
import speech_recognition as sr
import pyttsx3
import time

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 180)  # Adjust speaking speed

# Initialize Speech Recognition
recognizer = sr.Recognizer()
recognizer.dynamic_energy_threshold = True  # Adjusts to background noise

def speak(text):
    """Convert text to speech"""
    if text.strip():  # Only speak if text is not empty
        engine.say(text)
        engine.runAndWait()
        time.sleep(0.3)  # Small delay to ensure audio completes

def listen():
    """Captures and recognizes speech"""
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Reduce background noise
        try:
            audio = recognizer.listen(source, timeout=5)  # 5s timeout for efficiency
            text = recognizer.recognize_google(audio)
            return text.strip() if text else "No input detected."
        except sr.UnknownValueError:
            return "Sorry, I didn't catch that."
        except sr.RequestError:
            return "Network error."
        except sr.WaitTimeoutError:
            return "No input detected."

def ask_ollama(query):
    """Process user input and respond using TinyLLaMA"""
    # Custom responses
    query_lower = query.lower()
    if "your name" in query_lower:
        return "My name is Athulya."
    if "who created you" in query_lower:
        return "My creators are Karthik and Gokhul from Chennai Institute of Technology."

    # Generate AI response with optimized settings
    response = ollama.chat(
        model='tinyllama',
        messages=[{"role": "user", "content": query}],
        options={"num_predict": 150}  # Slightly increased tokens to prevent cutoffs
    )

    # Handle possible empty responses
    return response['message']['content'] if response['message']['content'].strip() else "I couldn't generate a response."

# Main loop
if __name__ == "__main__":
    speak("Hello! How can I help you today?")
    while True:
        user_input = listen()
        print(f"You said: {user_input}")
        
        if "exit" in user_input.lower() or "stop" in user_input.lower():
            speak("Goodbye!")
            break
        
        if user_input in ["No input detected.", "Sorry, I didn't catch that.", "Network error."]:
            speak(user_input)
            continue  # Skip AI processing for invalid inputs
        
        # Get response from TinyLLaMA
        response = ask_ollama(user_input)
        print(f"Athulya says: {response}")
        speak(response)
