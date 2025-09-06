import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME")
EMBEDDING_MODEL = os.getenv("GOOGLE_EMBEDDING_MODEL", "models/embedding-001")
LLM_MODEL = os.getenv("GOOGLE_LLM_MODEL", "gemini-2.5-flash-lite")

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def search_similar_documents(query, k=10):
    """
    Search for similar documents in the vector database.
    
    Args:
        query (str): The search query
        k (int): Number of results to return
        
    Returns:
        list: List of documents with similarity scores
    """
    if not DATABASE_URL:
        print("Error: DATABASE_URL not set in environment variables")
        return []
    
    # Create embeddings
    embeddings = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Create vector store
    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=COLLECTION_NAME,
        connection=DATABASE_URL,
    )
    
    # Search for similar documents
    results = vector_store.similarity_search_with_score(query, k=k)
    
    return results

def format_search_results(results):
    """
    Format search results for LLM consumption.
    
    Args:
        results (list): List of documents with similarity scores
        
    Returns:
        str: Formatted context string
    """
    if not results:
        return "Nenhum documento relevante encontrado."
    
    formatted_context = ""
    for i, (doc, score) in enumerate(results, 1):
        formatted_context += f"Documento {i} (Similaridade: {score:.4f}):\n{doc.page_content}\n\n"
    
    return formatted_context

def search_prompt(question=None):
    """
    Create a search prompt chain for answering questions.
    
    Args:
        question (str): The question to answer
        
    Returns:
        LLMChain: Configured LLM chain for question answering
    """
    if not question:
        return None
    
    # Search for similar documents
    search_results = search_similar_documents(question)
    
    if not search_results:
        print("No relevant documents found for the question.")
        return None
    
    # Format search results
    formatted_context = format_search_results(search_results)
    
    # Create prompt template
    prompt = PromptTemplate(
        template=PROMPT_TEMPLATE,
        input_variables=["contexto", "pergunta"]
    )
    
    # Initialize LLM
    llm = ChatGoogleGenerativeAI(
        model=LLM_MODEL,
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.1
    )
    
    # Create chain using modern RunnableSequence approach
    chain = (
        RunnablePassthrough.assign(context=lambda x: x["contexto"])
        | prompt
        | llm
        | StrOutputParser()
    )
    
    # Return chain with formatted context
    return chain, formatted_context, question

def answer_question(question):
    """
    Answer a question using the search and LLM.
    
    Args:
        question (str): The question to answer
        
    Returns:
        str: The answer to the question
    """
    chain_result = search_prompt(question)
    
    if not chain_result:
        return "Não foi possível encontrar informações relevantes para responder sua pergunta."
    
    chain, formatted_context, question = chain_result
    
    try:
        # Get answer from LLM using invoke instead of deprecated run method
        response = chain.invoke({
            "contexto": formatted_context,
            "pergunta": question
        })
        return response.get('text', str(response)) if isinstance(response, dict) else str(response)
    except Exception as e:
        print(f"Error getting answer: {e}")
        return "Ocorreu um erro ao processar sua pergunta."
