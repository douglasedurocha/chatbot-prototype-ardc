import os
from dotenv import load_dotenv
import warnings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import CSVLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate

# Load environment variables
load_dotenv()
warnings.filterwarnings("ignore", category=DeprecationWarning)

class ChatBotLLM:
    def __init__(self, data):
        self.data = data
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
        self.chain = self.initialize_chain()

    def embedding(self):
        loader = CSVLoader(file_path=self.data, source_column="question")
        self.data = loader.load()
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=os.getenv('API_KEY'))
        return embeddings
    
    def vector_db(self, embeddings):
        vectordb = FAISS.from_documents(documents=self.data, embedding=embeddings)
        retriever = vectordb.as_retriever(score_threshold=0.75)
        return retriever
    
    def initialize_chain(self):
        embeddings = self.embedding()
        retriever = self.vector_db(embeddings)
        llm = ChatGoogleGenerativeAI(
            api_key=os.getenv('API_KEY'),
            model="gemini-1.5-flash",
            temperature=0.4,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )
        PROMPT = PromptTemplate(template=self.prompt_template, input_variables=["context", "question"])
        chain_type_kwargs = {"prompt": PROMPT}
        chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            input_key="query",
            return_source_documents=True,
            chain_type_kwargs=chain_type_kwargs
        )
        return chain

    def get_response(self, question):
        response = self.chain.invoke(question)
        return {
            "query": response['query'],
            "result": response['result']
        }
