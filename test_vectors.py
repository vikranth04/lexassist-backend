from app.repositories.vector_repository import VectorRepository

repo = VectorRepository()

docs = repo.get_all_documents()

print("Total IDs:", len(docs.get("ids", [])))
print("Total Documents:", len(docs.get("documents", [])))
print("Sample Metadata:", docs.get("metadatas", [])[:2])