import openai
from flask import Flask, request, jsonify, session, render_template
import os

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "default_secret_key")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chatbot', methods=['POST'])
def chatbot_endpoint():
    data = request.get_json()
    question = data.get("question")

    if not question:
        return jsonify({"error": "Please provide a question"}), 400

    if 'messages' not in session:
        session['messages'] = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]

    try:
        session['messages'].append({"role": "user", "content": question})

        openai.api_key = OPENAI_API_KEY
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use your desired model
            messages=session['messages'],
            max_tokens=100
        )

        answer = response['choices'][0]['message']['content']

        session['messages'].append({"role": "assistant", "content": answer})
        
        return jsonify({"answer": answer}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
