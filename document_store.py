import chromadb
from ollama import embeddings


CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "business_faq"


def get_collection():
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    return collection


def create_embedding(text):
    response = embeddings(
        model="nomic-embed-text",
        prompt=text
    )

    return response["embedding"]


def load_business_information():
    with open("business_info.txt", "r", encoding="utf-8") as file:
        return file.read()


def split_text(text, chunk_size=500):
    words = text.split()

    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


def store_documents():

    collection = get_collection()

    business_text = load_business_information()

    chunks = split_text(business_text)

    for index, chunk in enumerate(chunks):

        vector = create_embedding(chunk)

        collection.upsert(
            ids=[f"business_{index}"],
            documents=[chunk],
            embeddings=[vector],
            metadatas=[
                {
                    "source": "business_info.txt"
                }
            ]
        )

    print("Business information stored successfully.")