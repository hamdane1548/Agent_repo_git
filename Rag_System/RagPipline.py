from langchain_mistralai import ChatMistralAI
from langchain_core.documents import  Document
from loguru import logger
from Settings import Settings
from infrastructure.base import connection
from langchain_mistralai import MistralAIEmbeddings
from langchain_chroma import Chroma

from data_access.Profile_mongo import GitHubProfile
settings = Settings()
from langchain_text_splitters import RecursiveCharacterTextSplitter

class RagPipline:
    llm = ChatMistralAI(
        api_key=settings.MISTRAL_API_KEY,
        temperature=0.1,
        model="mistral-medium-latest"
    )
    db =  connection[settings.MONGO_DATABASE]
    collection = db[settings.MONGO_COLLECTION_JOB_DESCRIPTION]
    documents = list(collection.find())
    logger.info(f"{len(documents)} documents found")
    for document in documents:
        profiles = document["profile"]
    logger.info(f"{profiles} documents found")
    for profile in profiles:
        doc = [Document(
            page_content=profile,
            metadata={"source":"gihtub","user":profile["username"]},
        )]
        splitter = RecursiveCharacterTextSplitter(
            chunk_size = 500,
            chunk_overlap=50
        )
        chunks = splitter.split_documents(docs)

        embedding_model = MistralAIEmbeddings(
            model="mistral-embed",
            api_key=settings.MISTRAL_API_KEY,
        )
        vectordb = Chroma.from_documents(
            document=chunks,
            embedding=embedding_model,
        )



