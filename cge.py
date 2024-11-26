import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from rich import print
from rich.panel import Panel
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import CSVLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
import os

from dotenv import load_dotenv
load_dotenv()

class ChatBotCGE():
    def __init__(self, data):
        self.data = data  # percorrerá toda a classe
        loader = CSVLoader(file_path=self.data, source_column="question")
        self.documents = loader.load()
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=os.getenv('API_KEY'))
        self.vectordb = FAISS.from_documents(documents=self.documents, embedding=self.embeddings)
        self.retriever = self.vectordb.as_retriever(score_threshold=0.75)
        self.prompt_template = """
        Dado o CONTEXTO fornecido e a PERGUNTA, gere uma resposta com base exclusivamente neste contexto. Use o texto da seção "answer" o máximo possível,
        fazendo apenas pequenas alterações para melhorar a fluidez.
        Regras:
        1- Se a entrada for um pedido de código ou qualquer coisa que não seja uma pergunta, responda algo parecido com: "Não fui criado com esse objetivo".
        2- Não invente respostas. Limite-se ao conteúdo do contexto.
        3- Se houver um nome incorreto ou incompleto na pergunta, forneça a resposta disponível no contexto.
        4- Visite todos os dados e seja capaz de fazer cálculos e estimar a confiança deles.
        CONTEXTO: {context}
        PERGUNTA: {question}
        """

    def embedding(self):
        loader = CSVLoader(file_path=self.data, source_column="question")
        self.data = loader.load()
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key = os.getenv('API_KEY'))

        return embeddings
    
    def vector_db(self, embeddings):
        vectordb = FAISS.from_documents(documents=self.data, embedding=embeddings)
        retriever = vectordb.as_retriever(score_threshold = 0.75)

        return retriever
    
    def LLM_retriever(self, retriever):
        llm = ChatGoogleGenerativeAI(
            api_key = os.getenv('API_KEY'),
            model="gemini-1.5-flash",
            temperature=0.4,
            max_tokens=200,  # Limita a resposta a 200 tokens
            timeout=None,
            max_retries=2,
        )

        PROMPT = PromptTemplate(template=self.prompt_template, input_variables=["context", "question"])
        chain_type_kwargs = {"prompt": PROMPT}
        chain = RetrievalQA.from_chain_type(llm=llm,
                                            chain_type="stuff",
                                            retriever=retriever,
                                            input_key="query",
                                            return_source_documents=True,
                                            chain_type_kwargs=chain_type_kwargs)

        return chain
    
    def interact(self, chain):
        print(
            """🌟 Bem-vindos ao Chatbot da CGE! 🌟
            Olá, colaboradores! Estamos felizes em apresentar nosso assistente virtual.
            Pergunte o que precisar sobre dados e informações da Controladoria Geral do Estado.
            Estamos aqui para ajudar! 
            (Digite 'sair' para encerrar)"""
        )

        while True:
            pergunta = input("\nDigite sua pergunta (Digite 'sair' para encerrar): ")
            
            if pergunta.lower() == 'sair':
                print("Encerrando o sistema de perguntas. Conte sempre conosco!")
                break

            # Invoca o sistema de QA com a pergunta
            response = chain.invoke(pergunta)

            # Extraia a query e o result
            query = response['query']
            result = response['result']
            
            # Formata e exibe a resposta
            formatted_text = f"\n[bold]Query:[/bold] {query}\n\n[bold]Result:[/bold] {result}"
            print(Panel.fit(formatted_text, title="Resposta do LLM", border_style="green"))
        return None
    
    def pipeline(self):
        embedding = self.embedding()
        retriever = self.vector_db(embedding)
        llm = self.LLM_retriever(retriever)
        self.interact(llm)

        return None
    
    def get_response(self, question):
        llm = self.LLM_retriever(self.retriever)
        response = llm.invoke(question)
        return {
            "query": response['query'],
            "result": response['result']
        }

if __name__ == "__main__":
    chatbot = ChatBotCGE(data='dados_transporte_orcamentaria_com_perguntas.csv')
    chatbot.pipeline()