from flask import Flask, render_template, jsonify, request
# from llm import ChatBotLLM
from cge import ChatBotCGE
import comprasnet

app = Flask(__name__)

chatbot = ChatBotCGE(data='data/dados_transporte_orcamentaria_com_perguntas.csv')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chatbot', methods=['POST'])
def chatbot_endpoint():
    data = request.get_json()
    question = data.get("question")
    
    if not question:
        return jsonify({"error": "Please provide a question"}), 400

    response = chatbot.get_response(question)
    
    return jsonify(response)

@app.route('/api/guideaccess')
def open_guide_access():
    comprasnet.guide()
    return jsonify({"message": "Guide access opened"})

if __name__ == '__main__':
    app.run()