from sentence_transformers import SentenceTransformer, util
import torch

# Load the pre-trained Sentence-BERT model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Example indexed data (this would be fetched from Elasticsearch or database in practice)
documents = [
    {"id": 1, "text": "Buy the latest smartphone with advanced features"},
    {"id": 2, "text": "Best deals on electronics and gadgets"},
    {"id": 3, "text": "Find your perfect smartphone with top-notch camera"},
    {"id": 4, "text": "Explore smartphones, tablets, and laptops"},
]

# Index the documents using the model (convert them into embeddings)
document_embeddings = model.encode([doc['text'] for doc in documents], convert_to_tensor=True)

def semantic_search(query: str):
    """
    Perform a semantic search using a BERT model.
    :param query: User search query.
    :return: A list of ranked results based on semantic similarity.
    """
    # Generate an embedding for the query
    query_embedding = model.encode(query, convert_to_tensor=True)

    # Compute the cosine similarities between the query and the documents
    similarities = util.pytorch_cos_sim(query_embedding, document_embeddings)

    # Sort the results based on similarity
    ranked_results = torch.argsort(similarities, descending=True)

    # Retrieve and return the top-k results (let's say top-3 results)
    top_k = 3
    top_results = [(documents[idx], similarities[0][idx].item()) for idx in ranked_results[0][:top_k]]
    
    return top_results
