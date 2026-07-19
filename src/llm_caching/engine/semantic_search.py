import os 
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from src.llm_caching.constants import constants

class SemanticSearch:
    def __init__(self, sentence_transformer_model: SentenceTransformer):
        self.__sentence_transformer_model = sentence_transformer_model
        self.__faiss_index: faiss.IndexHNSWFlat = faiss.IndexHNSWFlat(384,32,faiss.METRIC_INNER_PRODUCT)

    def build_index(self, user_messages: list[str]):
        """ Method to buld index from user messages """

        # Batch encoding (fast)
        embeddings = self.__sentence_transformer_model.encode(user_messages, batch_size=32)
    
        embeddings = np.array(embeddings).astype("float32")
    
        # Normalize (IMPORTANT for cosine similarity)
        faiss.normalize_L2(embeddings)
    
        dimension = embeddings.shape[1]
    
        # HNSW index (fast for large data)
        index = faiss.IndexHNSWFlat(dimension, 32, faiss.METRIC_INNER_PRODUCT)
        index.hnsw.efConstruction = 40
        index.hnsw.efSearch = 16
    
        index.add(embeddings)
    
        return index
    
    def add_to_index(self, user_messages: list[str]):
        """Method to add message in existeing index"""
        embeddings = self.__sentence_transformer_model.encode(user_messages)
        embeddings = np.array(embeddings).astype("float32")

        faiss.normalize_L2(embeddings)

        self.__faiss_index.add(embeddings)
        self.save_index_into_file()

    
    def save_index_into_file(self):
        """ Method to save index into index file """
        faiss.write_index(self.__faiss_index, constants.INDEX_FILE_PATH)

    def load_index_from_file(self):
        """ Method to load index from index file """

        if os.path.exists(constants.INDEX_FILE_PATH):
            self.__faiss_index = faiss.read_index(constants.INDEX_FILE_PATH)
            return 
    
        # Create new HNSW index
        index =  faiss.IndexHNSWFlat(384,32,faiss.METRIC_INNER_PRODUCT)
        index.hnsw.efConstruction = 40
        index.hnsw.efSearch = 16
    
        # Save empty index
        faiss.write_index(index, constants.INDEX_FILE_PATH)
    
        self.__faiss_index =  index
    
    def search_index(self, query: str, no_of_result_to_fetch: int=constants.NO_OF_RESULTS_TO_FETCH) -> int | None:
        """ Method to search user message from index and return array chat context id and score """

        query_vec = self.__sentence_transformer_model.encode([query]).astype("float32")
    
        # Normalize query
        faiss.normalize_L2(query_vec)
    
        distances, indices = self.__faiss_index.search(query_vec, no_of_result_to_fetch)
    
        results = []
        print("Total vectors:",  self.__faiss_index.ntotal)
        for score, idx in zip(distances[0], indices[0]):
            
            if idx == -1:
                continue
            
            # Convert similarity (inner product)
            similarity = float(score)
            print("similarity", similarity)
            if similarity >= constants.SIMILARITY_THRESHOLD:
                results.append({
                    "id": idx,
                    "score": similarity #remove this if unused
                })
    
        return results[0]["id"] if results and "id" in results[0] else None

    
