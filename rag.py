import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import login

HUGGINGFACE_TOKEN = os.getenv("HF_TOKEN")

if not HUGGINGFACE_TOKEN:
    raise ValueError("Hugging Face token is missing. Set it as an environment variable.")

login(HUGGINGFACE_TOKEN)

MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.1"

try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, token=HUGGINGFACE_TOKEN)
    llm_model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, token=HUGGINGFACE_TOKEN)
except Exception as e:
    raise ValueError(f"Failed to load LLM model: {e}. Ensure you have access to the model and a valid token.")

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def create_faiss_index(data):
    
    if data.isnull().any():
        data = data.dropna()
    
    data_list = data.astype(str).tolist()
    embeddings = embedding_model.encode(data_list, convert_to_numpy=True)
    
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    
    return index

index = None

def initialize_faiss_index(df):
    global index
    if 'reservation_status_date' not in df.columns:
        raise ValueError("Column 'reservation_status_date' not found in DataFrame.")
    
    index = create_faiss_index(df['reservation_status_date'])


def answer_question(question, df):
    
    if index is None:
        raise ValueError("FAISS index has not been initialized. Call `initialize_faiss_index(df)` first.")
    
    query_embedding = embedding_model.encode([question], convert_to_numpy=True)
    _, indices = index.search(query_embedding, k=1)
    
    if len(indices[0]) == 0:
        return "No relevant data found."
    
    relevant_data = df.iloc[indices[0]]
    context = relevant_data.to_string()
    input_text = f"Context: {context}\nQuestion: {question}"
    
    inputs = tokenizer(input_text, return_tensors="pt")
    outputs = llm_model.generate(**inputs, max_length=200)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return answer
