import os
import json
import sqlite3
from pathlib import Path

class DocIngestor:
    def __init__(self, db_path="knowledge_vault.db", knowledge_dir="../knowledge_base"):
        self.db_path = db_path
        self.knowledge_dir = knowledge_dir
        self.init_db()

    def init_db(self):
        """Initialise une base SQLite simple pour simuler le vault de connaissances."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS docs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        filename TEXT,
                        content TEXT,
                        tags TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()
        conn.close()

    def ingest_text_file(self, file_path, tags=""):
        """Lit et indexe un fichier texte."""
        if not os.path.exists(file_path):
            print(f"Erreur : Le fichier {file_path} n'existe pas.")
            return False
            
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        filename = os.path.basename(file_path)
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("INSERT INTO docs (filename, content, tags) VALUES (?, ?, ?)", (filename, content, tags))
        conn.commit()
        conn.close()
        print(f"✅ Document '{filename}' indexé avec succès.")
        return True

    def query_knowledge(self, query):
        """Recherche simple par mots-clés (simulation de RAG)."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT content FROM docs WHERE content LIKE ? LIMIT 3", (f"%{query}%",))
        results = c.fetchall()
        conn.close()
        return [r[0] for r in results]

if __name__ == "__main__":
    # Test simple
    ingestor = DocIngestor(db_path="c:/Users/diffo_jb/OneDrive/Documents/WorkflowAntigravity/LD_Assurances_World_Platform/core/knowledge_vault.db")
    
    # Création d'un document de test
    test_doc = "c:/Users/diffo_jb/OneDrive/Documents/WorkflowAntigravity/LD_Assurances_World_Platform/knowledge_base/produits_auto.txt"
    with open(test_doc, "w", encoding="utf-8") as f:
        f.write("LD Assurances Automobile : Zone 1 (Douala/Yaoundé) - Tarif de base 50,000 FCFA. Garanties : RC, Vol, Incendie.")
    
    ingestor.ingest_text_file(test_doc, tags="automobile, tarifs")
    
    # Test de recherche
    print(f"Recherche 'Automobile' : {ingestor.query_knowledge('Automobile')}")
