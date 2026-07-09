from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import FAISS
from langchain_anthropic import ChatAnthropic
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os
from anthropic import Anthropic


load_dotenv()

# Charger le PDF
loader = PyPDFLoader("docs/20260624_Rapport_annuel_2025_Pôle_commun_ACPR_AMF_pdf.pdf")
documents = loader.load()

print(f"Nombre de pages chargées : {len(documents)}")

# Découper en chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = splitter.split_documents(documents)

print(f"Nombre de chunks créés : {len(chunks)}")
print("\n--- Les 3 premiers chunks ---")
for i, chunk in enumerate(chunks[:3]):
    print(f"\nChunk {i+1} :")
    print(chunk.page_content[:300])
    print("...")

# Créer les embeddings et la base vectorielle
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)
vectorstore = FAISS.from_documents(chunks, embeddings)

print(f"\nBase vectorielle créée avec {vectorstore.index.ntotal} vecteurs")

# Test de recherche sémantique
question = "Combien de sites non autorisés ont été ajoutés aux listes noires en 2025 ?"
docs_proches = vectorstore.similarity_search(question, k=3)

print(f"\n--- Chunks les plus proches pour la question ---")
print(f"Question : {question}")
for i, doc in enumerate(docs_proches):
    print(f"\nRésultat {i+1} :")
    print(doc.page_content[:300])


client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Construire le contexte à partir des chunks retrouvés
contexte = "\n\n".join([doc.page_content for doc in docs_proches])

# Envoyer au LLM avec le contexte
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1000,
    system="Tu es un assistant qui répond aux questions en te basant uniquement sur le contexte fourni. Si la réponse n'est pas dans le contexte, dis-le clairement.",
    messages=[
        {"role": "user", "content": f"Contexte :\n{contexte}\n\nQuestion : {question}"}
    ]
)

print("\n--- Réponse du LLM ---")
print(response.content[0].text)