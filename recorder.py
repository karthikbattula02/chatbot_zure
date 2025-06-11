import speech_recognition as sr
import pyttsx3
import threading

stop_flag = False
recorded_text = ""

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def stop_on_signal():
    global stop_flag
    input("Type 'stop' to end voice recording: ")
    stop_flag = True

def listen_and_transcribe():
    global stop_flag, recorded_text
    stop_flag = False
    recorded_text = ""

    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("Speak now. Type 'stop' to stop recording...")

    thread = threading.Thread(target=stop_on_signal)
    thread.daemon = True
    thread.start()

    audio_data = []

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")

        while not stop_flag:
            try:
                chunk = recognizer.listen(source, timeout=1, phrase_time_limit=3)
                audio_data.append(chunk)
            except sr.WaitTimeoutError:
                continue

    if not audio_data:
        return "No speech detected."

    combined_audio = sr.AudioData(
        b''.join([a.get_raw_data() for a in audio_data]),
        audio_data[0].sample_rate,
        audio_data[0].sample_width
    )

    try:
        recorded_text = recognizer.recognize_google(combined_audio)
        print(f"You said: {recorded_text}")
        return recorded_text
    except sr.UnknownValueError:
        return "Could not understand audio."
    except sr.RequestError as e:
        return f"Speech recognition error: {e}"
