#Retrival augmentation generation (Rag)

import asyncio

import chromadb
from langchain_core.documents import Document
import numpy as np
import pandas as pd
from pydantic import TypeAdapter
from yarl import Query
from zenml import metadata, pipeline, step
from loguru import logger
from Settings import Settings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
import faiss

from infrastructure.base import connectiondbmongo
settings = Settings()
from langchain_mistralai import MistralAIEmbeddings
embeddings = MistralAIEmbeddings(
            model="mistral-embed",
            api_key=settings.MISTRAL_API_KEY,
    )

async def search(query, texts):

    query_embedding = await embeddings.aembed_query(query)

    # Create embeddings for your documents
    document_embeddings = await embeddings.aembed_documents(texts)

    document_embeddings = np.array(
        document_embeddings,
        dtype="float32"
    )

    query_embedding = np.array(
        query_embedding,
        dtype="float32"
    ).reshape(1, -1)

    dimension = document_embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(document_embeddings)

    distances, indices = index.search(
        query_embedding,
        k=5
    )

    results = [
        texts[i]
        for i in indices[0]
    ]

    return results
@step
def EmbeddingsRag(value):
    if value:
            try:
                db = connectiondbmongo[settings.MONGO_DATABASE]
                collection = db[settings.MONGO_COLLECTION_JOB_DESCRIPTION]
                context = list(collection.find({}))
                text = str(context)
                texts = text.split('.')
                texts = [t.strip(' \n') for t in texts]
                [logger.info(f"the new value of the doucment {i}") for i in texts]
              
                documents = [Document(page_content=text,metadata={"source": "test embedding"}) for text in texts]
               
                splitter = RecursiveCharacterTextSplitter(
                     chunk_size=500,
                chunk_overlap=50
                )
                chunks = splitter.split_documents(documents)
                vector_store = Chroma(
                collection_name="github_profiles",
                embedding_function=embeddings,
                host="localhost",
                port=8000,
                )
                vector_store.add_documents(chunks)
                result = asyncio.run(
                     search(
                 "The summary of the project that the profiles works one",
                 texts 
                 )
                )
                logger.info(f"the context is {result}")
            except Exception as e:
                logger.exception(f"Exception while accessing MongoDB: {e}")
    else:
        logger.exception(f"Exception while accessing MongoDB: {e}")
        raise
