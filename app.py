from openai import OpenAI
from flask import Flask, request, jsonify, session, render_template
import os
from time import sleep
from io import BytesIO
from PyPDF2 import PdfReader
from docx import Document

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "default_secret_key")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
assistant_id = os.getenv("ASSISTANT_ID")

def obter_resposta(mensagem):
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

def processar_pdf(file):
    reader = PdfReader(file)
    texto = ""
    for page in reader.pages:
        texto += page.extract_text()
    return texto

def processar_docx(file):
    doc = Document(file)
    texto = ""
    for para in doc.paragraphs:
        texto += para.text + "\n"
    return texto

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
        resposta = obter_resposta(pergunta)
        return jsonify({"answer": resposta}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

@app.route('/api/compare_documents', methods=['POST'])
def compare_documents():
    if 'document_1' not in request.files or 'document_2' not in request.files:
        return jsonify({"error": "Por favor, forneça ambos os documentos"}), 400

    doc1 = request.files['document_1']
    doc2 = request.files['document_2']

    # Determinar tipo de documento e processar
    if doc1.filename.endswith('.pdf'):
        documento_1 = processar_pdf(doc1)
    elif doc1.filename.endswith('.docx'):
        documento_1 = processar_docx(doc1)
    else:
        return jsonify({"error": "Tipo de arquivo do documento 1 não suportado"}), 400

    if doc2.filename.endswith('.pdf'):
        documento_2 = processar_pdf(doc2)
    elif doc2.filename.endswith('.docx'):
        documento_2 = processar_docx(doc2)
    else:
        return jsonify({"error": "Tipo de arquivo do documento 2 não suportado"}), 400

    # Criando uma mensagem para o assistente comparar os dois documentos
    mensagem = f"Compare os seguintes documentos:\n\nDocumento 1:\n{documento_1}\n\nDocumento 2:\n{documento_2}\n\nQual é a diferença entre os dois documentos?"

    try:
        resposta = obter_resposta(mensagem)
        return jsonify({"comparison": resposta}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

@app.route('/api/analyse_document', methods=['POST'])
def analyse_document():
    if 'document' not in request.files:
        return jsonify({"error": "Por favor, forneça um documento"}), 400

    doc = request.files['document']

    # Determinar tipo de documento e processar
    if doc.filename.endswith('.pdf'):
        document = processar_pdf(doc)
    elif doc.filename.endswith('.docx'):
        document = processar_docx(doc)
    else:
        return jsonify({"error": "Tipo de arquivo do documento 1 não suportado"}), 400

    # Criando uma mensagem para o assistente analisar o documento
    mensagem = f"Forneça uma análise detalhada do seguinte documento:\n\n{document}\n\nInclua os principais pontos abordados, qualquer informação crítica e um resumo geral."

    try:
        resposta = obter_resposta(mensagem)
        return jsonify({"analysis": resposta}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
