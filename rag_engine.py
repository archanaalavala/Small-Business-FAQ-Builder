import chromadb
from ollama import embeddings, chat


CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "business_faq"


def get_collection():

    client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )

    collection = client.get_collection(
        name=COLLECTION_NAME
    )

    return collection


def create_embedding(text):

    response = embeddings(
        model="nomic-embed-text",
        prompt=text
    )

    return response["embedding"]


def retrieve_information(question, top_k=3):

    collection = get_collection()

    question_embedding = create_embedding(question)

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k
    )

    documents = results["documents"][0]

    return documents


def generate_answer(question):

    documents = retrieve_information(question)

    context = "\n\n".join(documents)

    prompt = f"""
You are a helpful customer support assistant for a small business.

Answer the customer's question using ONLY the information
provided in the context below.

If the answer cannot be found in the context, say:

"I don't have that information in the business FAQ."

Do not invent prices, policies, opening hours, locations,
products or other business information.

Business Context:
{context}

Customer Question:
{question}

Answer:
"""

    response = chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"], documents