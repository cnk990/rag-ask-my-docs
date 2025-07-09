import streamlit as st
import os
import sys
import pickle

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openai import OpenAI
from rag_pipeline.embeddings import embed_text
from rag_pipeline.retrieval import retrieve_top_chunks
from rag_pipeline.llm import ask_llm
from rag_pipeline.utils import (
    load_documents_from_folder,
    split_by_sections,
    split_text_in_sections
)


# Initialize client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ----------Load and embed documents----------
# Load all text files from data/
doc_folder = os.path.join(os.path.dirname(__file__), "..", "data")
documents = load_documents_from_folder(doc_folder)

# Prepare chunk and embedding storage
doc_chunks_dict = {}
doc_embeddings_dict = {}

for doc_name, text in documents.items():
    embedding_file = f"embeddings_{doc_name}.pkl"

    if os.path.exists(embedding_file):
        # Load pre-computed embeddings and chunks
        with open(embedding_file, "rb") as f:
            chunks, embeddings = pickle.load(f)
    else:
        sections = split_by_sections(text)
        chunks = split_text_in_sections(sections, max_sentences=3)

        # Create embeddings in a batch request
        if chunks:
            # Batch embed the chunks
            response = client.embeddings.create(
                model="text-embedding-3-small",
                input=chunks
            )
            embeddings = [item.embedding for item in response.data]
        else:
            embeddings = []

        # Save for next time
        with open(embedding_file, "wb") as f:
            pickle.dump((chunks, embeddings), f) # type: ignore

    doc_chunks_dict[doc_name] = chunks
    doc_embeddings_dict[doc_name] = embeddings


# -----------Streamlit UI-------------------------

st.title("Ask my Docs")

st.markdown("""
Welcome to **Ask My Docs** — your personal AI assistant for quickly finding answers in internal documents.

This app allows you to ask questions about the following documents:

- **Leave Policy**  
    Covers annual leave, sick leave, parental leave, jury duty and more.

- **Security Policy**  
    Covers password rules, multi-factor authentication, data security, remote work guidelines and incident reporting.

Select a policy you would like to query.
Type a question in the box below and the AI will retrieve the most relevant sections from these documents to provide an answer.

Example questions:
- "How many days of annual leave do employees get?"
- "How do I report a security incident?"
""")

# Select document to query
doc_options = list(documents.keys())
selected_doc = st.selectbox("Select a document to query:", doc_options)

query = st.text_input(
    "Enter your question:",
    placeholder="e.g. How many days of annual leave do employees get?"
)

if query and selected_doc:
    # Embed query
    query_embedding = embed_text(client, query)

    # Retrieve top chunks
    top_chunks, max_sim = retrieve_top_chunks(
        query_embedding,
        doc_chunks_dict[selected_doc],
        doc_embeddings_dict[selected_doc],
        top_k=3,
        similarity_threshold=0.2
    )
    context = "\n\n".join(top_chunks)

    # Ask LLM
    if not top_chunks:
        st.warning(
            "No relevant information found in this document for your query. "
            f"(Max similarity was {max_sim:.4f})"
        )
    else:
        context = "\n\n".join(top_chunks)
        answer = ask_llm(client, context, query)

        st.write("## Answer:")
        st.write(answer)

        with st.expander("View Retrieved Chunks"):
            for i, chunk in enumerate(top_chunks, start=1):
                st.markdown(f"**Chunk {i}:** {chunk}")


