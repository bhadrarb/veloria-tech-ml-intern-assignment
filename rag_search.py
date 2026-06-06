import pandas as pd
from sentence_transformers import SentenceTransformer
import chromadb

df=pd.read_csv("match_data.csv")
sentences=[]
for _, row in df.iterrows():
    sentence=(f"{row['team1']} vs {row['team2']} at {row['venue']} on {row['date']}. "f"{row['result']}. "f"Top scorer: {row['top_scorer']} with {row['score']} runs.")
    sentences.append(sentence)
model=SentenceTransformer("all-MiniLM-L6-v2")
embeddings=model.encode(sentences)

client=chromadb.Client()
collection=client.create_collection("matches")
collection.add(documents=sentences,
    embeddings=embeddings.tolist(),
    ids=[str(i) for i in range(len(sentences))])

def search(query,n=3):
    n = min(n, collection.count()) 
    query_embedding=model.encode([query])
    results=collection.query(query_embeddings=query_embedding.tolist(),n_results=n)
    return results["documents"][0]
while True:
    query=input("\nenter your query or 'exit':")

    if query.lower()=="exit":
        break
    results=search(query)
    if not results:
        print("No results found.")
    else:
        for i,match in enumerate(results,1):
            print(f"{i}.{match}")
