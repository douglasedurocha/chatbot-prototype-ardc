from openai import OpenAI
from flask import Flask, request, jsonify, session, render_template
import os
from time import sleep

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "default_secret_key")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

INSTRUCOES_ASSISTANT = """Você é um especialista em assuntos regulatórios da indústria farmacêutica. Considere:
- Normas ANVISA, OMS, EMA, FDA e ICH
- Cite referências regulatórias atualizadas
- Use terminologia técnica consistente
- Priorize fontes oficiais
- Esclareça diferenças entre jurisdições
- Forneça exemplos práticos
- Atualize sobre mudanças regulatórias
- Esclareça que não é aconselhamento jurídico"""

def criar_assistant():
    assistant = client.beta.assistants.create(
        name="Especialista Regulatório Farmacêutico",
        instructions=INSTRUCOES_ASSISTANT,
        model="gpt-4o",
        tools=[
            {"type": "code_interpreter"},
            {"type": "file_search"}
        ]
    )
    return assistant

def obter_resposta(assistant_id, mensagem):
    thread = client.beta.threads.create()
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=mensagem
    )
    
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )
    
    while True:
        status = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        if status.status == 'completed':
            break
        elif status.status in ['failed', 'cancelled', 'expired']:
            return f"Erro: {status.status}"
        sleep(1)
    
    mensagens = client.beta.threads.messages.list(thread_id=thread.id)
    resposta = mensagens.data[0].content[0].text.value
    return resposta

assistente_regulatorio = criar_assistant()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chatbot', methods=['POST'])
def chatbot_endpoint():
    data = request.get_json()
    pergunta = data.get("question")

    if not pergunta:
        return jsonify({"error": "Por favor, forneça uma pergunta"}), 400

    try:
        resposta = obter_resposta(assistente_regulatorio.id, pergunta)
        return jsonify({"answer": resposta}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)