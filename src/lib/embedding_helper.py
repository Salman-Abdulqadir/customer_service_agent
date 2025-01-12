from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import os
from lib.helpers import get_products_df, logger

# Initialize the model
model = SentenceTransformer('all-MiniLM-L6-v2')
faiss_index = f"{os.getcwd()}/src/faiss_index/product_index.index"

def combine_columns(row):
    return f"ID: {row['product_id']} Name:{row['name']} category:{row['category']} description: {row['description']} Stock: {row['stock']} Seasons: {row['seasons']} Price: {row['price']}"

def embed_products():
    try:
        logger("Embedding products in progress...")
        products_df = get_products_df()
        products_df['combined_text'] = products_df.apply(combine_columns, axis=1)

        # Generate embeddings for the combined text
        combined_texts = products_df['combined_text'].tolist()
        embeddings = model.encode(combined_texts, convert_to_tensor=False)

       # Convert embeddings to a NumPy array for FAISS
        embedding_matrix = np.array(embeddings).astype('float32')

        # Create the FAISS index
        index = faiss.IndexFlatL2(embedding_matrix.shape[1])  # Using L2 distance (Euclidean distance)
        index.add(embedding_matrix)  # Add embeddings to the index

        # Save the FAISS index if needed
        faiss.write_index(index, faiss_index)

        # Verify embeddings
        logger("Embedding products finished successfully!")
    except Exception as e:
        logger(f"Something went wrong while embedding products, Error: {e}", "ERROR")

def search_embeded_product(query, top_k=1, include_desc = False):
    try:
        try:
            # Load the FAISS index (or create it if not saved)
            index = faiss.read_index(faiss_index)
        except Exception as e:
            logger(f"FAISS index not found. Embedding Products, Error: {e}", "WARN")
            embed_products()
            index = faiss.read_index(faiss_index)
        
        # Generate the embedding for the query
        query_embedding = model.encode([query], convert_to_tensor=False)
        query_embedding = np.array(query_embedding).astype('float32')

        # Perform the search in the FAISS index
        _, indices = index.search(query_embedding, top_k)  # Return top_k results

        # Retrieve the top k products based on indices
        products_df = get_products_df()
        search_results = products_df.iloc[indices[0]]
        
        # Display the top k matching products
        cols_to_include = ['product_id', 'name', 'category', 'stock']
        
        if include_desc:
            cols_to_include.append('description')

        return search_results[cols_to_include]
    
    except Exception as e:
        logger(f"Error while searching: {e}", "ERROR")
        return []

