from flask import Flask, render_template, request, jsonify
from azure_chat import ask_azure
from recorder import listen_and_transcribe, speak

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json['message']
    response = ask_azure(user_message)
    speak(f"Question or task you said is {user_message}. Answer is {response}.")
    return jsonify({'reply': response})

@app.route('/voice', methods=['GET'])
def voice():
    text = listen_and_transcribe()
    response = ask_azure(text)
    speak(f"Question or task you said is {text}. Answer is {response}.")
    return jsonify({'input': text, 'reply': response})

if __name__ == '__main__':
    app.run(debug=True)
