import numpy as np


def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)

    dot_product = np.dot(vec1, vec2)
    norm_product = np.linalg.norm(vec1) * np.linalg.norm(vec2)
    if np.isclose(norm_product,  0.0):
        return 0.0
    return dot_product / norm_product


def retrieve_top_chunks(query_embedding, doc_chunks, chunk_embeddings, top_k=3, similarity_threshold=0.2):
    similarities = []

    print("Chunks:", len(doc_chunks))
    print("Embeddings:", len(chunk_embeddings))

    for chunk, emb in zip(doc_chunks, chunk_embeddings):
        sim = cosine_similarity(query_embedding, emb)
        similarities.append((chunk, sim))

    if not similarities:
        return [], 0

        # Find max similarity
    max_similarity = max(score for _, score in similarities)

    if max_similarity < similarity_threshold:
        print(f"No chunks exceeded the threshold ({similarity_threshold}). Max similarity: {max_similarity}")
        return [], max_similarity

    similarities.sort(key=lambda x: x[1], reverse=True)
    top_chunks = [chunk for chunk, _ in similarities[:top_k]]

    return top_chunks, max_similarity
