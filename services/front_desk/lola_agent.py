import json
import os
import sys

# Adding root path for relative imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from core.ingest_docs import DocIngestor

class FrontDeskAgent:
    def __init__(self, db_path="c:/Users/diffo_jb/OneDrive/Documents/WorkflowAntigravity/LD_Assurances_World_Platform/core/knowledge_vault.db"):
        self.ingestor = DocIngestor(db_path=db_path)
        self.name = "Lola"

    def handle_message(self, message):
        """
        Simule la réponse de Lola. 
        Dans une version finale, ceci appellerait l'API LLM.
        """
        message = message.lower()
        
        # Recherche dans la base de connaissance (RAG)
        knowledge = self.ingestor.query_knowledge(message)
        
        if knowledge:
            return f"Bienvenue chez LD Assurances ! Voici ce que j'ai trouvé pour vous : {knowledge[0]}"
        
        if "bonjour" in message or "salut" in message:
            return "Bonjour ! Je suis Lola, votre assistante IA. Comment puis-je vous aider aujourd'hui ?"
            
        if "tarif" in message or "prix" in message or "assurance" in message:
            return "Je peux vous aider à obtenir un devis. Quel type d'assurance recherchez-vous (Auto, Santé, Vie) ?"
            
        return "C'est une excellente question. Laissez-moi vérifier cela pour vous ou vous mettre en relation avec un de nos experts."

if __name__ == "__main__":
    lola = FrontDeskAgent()
    print(f"Lola: {lola.handle_message('Quel est le tarif auto ?')}")
