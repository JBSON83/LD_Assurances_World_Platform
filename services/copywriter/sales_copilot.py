import sqlite3
import json
import sys
import os

# Ajout du chemin racine pour permettre les imports relatifs
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from services.copywriter.ink_agent import CopywriterAgent

class SalesCopilot:
    def __init__(self, db_path="core/knowledge_vault.db"):
        self.db_path = db_path
        self.ink = CopywriterAgent()

    def get_product_data(self, product_name):
        """Récupère les faits réels via Scribe (simulation RAG)."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT content FROM docs WHERE content LIKE ? LIMIT 1", (f"%{product_name}%",))
        result = c.fetchone()
        conn.close()
        return result[0] if result else "Aucune donnée trouvée."

    def generate_email_sequence(self, product_name):
        """Génère une séquence de 3 emails persuasifs."""
        raw_data = self.get_product_data(product_name)
        
        # Email 1: Attention (AIDA)
        aida = self.ink.apply_aida(product_name, "sécurité de votre famille")
        email1 = f"Sujet : {aida['Attention']}\n\nBonjour,\n\n{aida['Intérêt']}\n\nSaviez-vous que : {raw_data}\n\n{aida['Désir']}\n\n{aida['Action']}"

        # Email 2: Problème (PAS)
        pas = self.ink.apply_pas(f"Risque {product_name}", "Stress financier", "LD Assurances")
        email2 = f"Sujet : Panne d'inspiration ou panne de moteur ?\n\n{pas['Problème']}\n\n{pas['Agitation']}\n\n{pas['Solution']}\n\nContactez-nous pour en parler."

        return [email1, email2]

if __name__ == "__main__":
    copilot = SalesCopilot(db_path="c:/Users/diffo_jb/OneDrive/Documents/WorkflowAntigravity/LD_Assurances_World_Platform/core/knowledge_vault.db")
    sequence = copilot.generate_email_sequence("Automobile")
    
    print("=== SÉQUENCE EMAIL GÉNÉRÉE (INK + SCRIBE) ===\n")
    for i, email in enumerate(sequence, 1):
        print(f"--- EMAIL {i} ---\n{email}\n")
