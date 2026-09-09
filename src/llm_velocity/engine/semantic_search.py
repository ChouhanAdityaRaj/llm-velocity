import os 
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from src.llm_velocity.constants import constants
from src.llm_velocity.models import models

class SemanticSearch:
    def __init__(self, sentence_transformer_model: SentenceTransformer, index_file_path: str):
        self.__sentence_transformer_model = sentence_transformer_model
        self.__faiss_index: faiss.IndexHNSWFlat = faiss.IndexHNSWFlat(384,32,faiss.METRIC_INNER_PRODUCT)
        self.__index_file_path: str = index_file_path

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
        faiss.write_index(self.__faiss_index, str(self.__index_file_path))

    def load_index_from_file(self):
        """ Method to load index from index file """

        if os.path.exists(self.__index_file_path):
            self.__faiss_index = faiss.read_index(str(self.__index_file_path))
            return 
    
        # Create new HNSW index
        index =  faiss.IndexHNSWFlat(384,32,faiss.METRIC_INNER_PRODUCT)
        index.hnsw.efConstruction = 40
        index.hnsw.efSearch = 16
    
        # Save empty index
        faiss.write_index(index, str(self.__index_file_path))
    
        self.__faiss_index =  index
    
    def search_index(self, query: str, no_of_result_to_fetch: int=constants.NO_OF_RESULTS_TO_FETCH) -> int | None:
        """ Method to search user message from index and return array chat context id and score """

        query_vec = self.__sentence_transformer_model.encode([query]).astype("float32")
    
        # Normalize query
        faiss.normalize_L2(query_vec)
    
        distances, indices = self.__faiss_index.search(query_vec, no_of_result_to_fetch)
    
        results = []
        # print("Total vectors:",  self.__faiss_index.ntotal)
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


    def match_best_method(
        self,
        user_messages: list[str],
        method_descriptions: dict[str, str],
        min_similarity: float = 0.15,
    ) -> models.MethodMatch | None:
        """Copyright (c) 2026 Aditya Raj Singh Chouhan. All rights reserved."""
        if not user_messages or not method_descriptions:
            return None

        method_names = list(method_descriptions.keys())
        method_texts = list(method_descriptions.values())

        # Encode & normalize method descriptions
        method_embeddings = np.array(
            self.__sentence_transformer_model.encode(method_texts)
        ).astype("float32")
        faiss.normalize_L2(method_embeddings)

        # Encode & normalize user messages
        message_embeddings = np.array(
            self.__sentence_transformer_model.encode(user_messages)
        ).astype("float32")
        faiss.normalize_L2(message_embeddings)

        n = len(user_messages)
        matches: list[models.MethodMatch] = []

        for i, (msg, msg_vec) in enumerate(zip(user_messages, message_embeddings)):
            # cosine similarity == dot product, since both sides are L2-normalized
            similarities = method_embeddings @ msg_vec
            best_idx = int(np.argmax(similarities))
            best_score = float(similarities[best_idx])  # -1..1

            # Skip junk/irrelevant messages that don't clear the threshold
            if best_score < min_similarity:
                continue

            weight = i + 1  # later message in the list => higher weight

            matches.append(
                models.MethodMatch(
                    method_name=method_names[best_idx],
                    match_percent=round(best_score * 100, 2),
                    user_message=msg,
                    weight=weight,
                    weighted_score=best_score * weight,
                )
            )

        return max(matches, key=lambda m: m.weighted_score) if matches else None

    
