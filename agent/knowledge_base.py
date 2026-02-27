#!/usr/bin/env python3
"""Knowledge base and RAG retrieval using Chroma vector database."""

import os
from pathlib import Path
from typing import Optional


class KnowledgeBase:
    """Vector database-backed RAG system using Chroma."""

    def __init__(self, skill_dir: str):
        """
        Initialize knowledge base for a skill.

        Args:
            skill_dir: Path to skills/<skill-name>/ directory
        """
        self.skill_dir = skill_dir
        self.knowledge_dir = os.path.join(skill_dir, "knowledge")
        self.skill_name = os.path.basename(skill_dir)

        # Initialize Chroma client
        try:
            import chromadb

            # Use persistent storage in skill directory
            persist_dir = os.path.join(skill_dir, ".chroma_db")
            os.makedirs(persist_dir, exist_ok=True)

            # Use new Chroma API with persistent client
            self.client = chromadb.PersistentClient(path=persist_dir)

            # Create or get collection (one per skill)
            self.collection = self.client.get_or_create_collection(
                name=f"{self.skill_name}_knowledge",
                metadata={"hnsw:space": "cosine"},
            )

            self.available = True
        except ImportError:
            print(
                "Warning: Chroma not available. Knowledge base retrieval will be disabled."
            )
            self.client = None
            self.collection = None
            self.available = False
        except Exception as e:
            print(f"Warning: Failed to initialize Chroma: {e}")
            self.client = None
            self.collection = None
            self.available = False

        self._load_documents()

    def _load_documents(self) -> None:
        """Load all knowledge documents into vector database."""
        if not self.available or not os.path.exists(self.knowledge_dir):
            return

        # Check if collection is already populated
        if self.collection.count() > 0:
            return  # Already loaded

        doc_files = sorted(Path(self.knowledge_dir).glob("*.md"))
        if not doc_files:
            return

        documents = []
        ids = []
        metadatas = []

        for idx, doc_file in enumerate(doc_files):
            try:
                with open(doc_file, "r") as f:
                    content = f.read()

                doc_name = doc_file.stem

                # Split document into chunks (sections separated by ##)
                sections = content.split("\n## ")
                for section_idx, section in enumerate(sections):
                    if not section.strip():
                        continue

                    chunk_id = f"{doc_name}_{section_idx}"
                    chunk_text = section if section_idx == 0 else f"## {section}"

                    documents.append(chunk_text)
                    ids.append(chunk_id)
                    metadatas.append(
                        {
                            "document": doc_name,
                            "section": section_idx,
                            "source_file": str(doc_file),
                        }
                    )

            except Exception as e:
                print(f"Warning: Failed to load {doc_file}: {e}")

        # Add to collection
        if documents:
            self.collection.add(
                documents=documents,
                ids=ids,
                metadatas=metadatas,
            )

    def retrieve(self, query: str, top_k: int = 3) -> list:
        """
        Retrieve relevant knowledge using semantic search.

        Args:
            query: User question or context
            top_k: Number of top results to return

        Returns:
            List of relevant document chunks with metadata
        """
        if not self.available or not self.collection:
            return []

        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=top_k,
                include=["documents", "metadatas", "distances"],
            )

            # Format results
            retrieved = []
            if results and results["documents"]:
                for doc, metadata, distance in zip(
                    results["documents"][0],
                    results["metadatas"][0],
                    results["distances"][0],
                ):
                    # Chroma returns distances (0 = identical, 2 = opposite)
                    # Convert to similarity score (higher is better)
                    similarity = 1 - (distance / 2)

                    retrieved.append(
                        {
                            "name": metadata.get("document", "Unknown"),
                            "section": metadata.get("section", 0),
                            "content": doc,
                            "score": similarity,
                            "source": metadata.get("source_file", ""),
                        }
                    )

            return retrieved

        except Exception as e:
            print(f"Warning: Retrieval failed: {e}")
            return []

    def format_context(self, retrieved_docs: list) -> str:
        """Format retrieved documents into context string for prompt."""
        if not retrieved_docs:
            return ""

        context = "\n## Reference Materials\n\n"
        for doc in retrieved_docs:
            context += f"### {doc['name']} (Relevance: {doc['score']:.1%})\n"
            # Limit content to avoid bloating prompt
            content = doc["content"][:800]
            context += content + ("..." if len(doc["content"]) > 800 else "")
            context += f"\n\n"

        return context

    def get_stats(self) -> dict:
        """Get statistics about the knowledge base."""
        if not self.available or not self.collection:
            return {"status": "unavailable"}

        return {
            "status": "available",
            "collection_name": self.collection.name,
            "document_count": self.collection.count(),
            "storage_path": os.path.join(self.skill_dir, ".chroma_db"),
        }
