import json
import os

class CopywriterAgent:
    def __init__(self):
        pass

    def apply_aida(self, product, mission):
        """Applique la méthode AIDA : Attention, Intérêt, Désir, Action."""
        return {
            "Attention": f"🛡️ Votre famille mérite-t-elle le meilleur ? Découvrez LD Assurances.",
            "Intérêt": f"Plus qu'une simple {product}, une tranquillité d'esprit sur-mesure au Cameroun.",
            "Désir": f"Rejoignez 10,000+ clients qui nous font confiance pour leur {mission}.",
            "Action": f"👉 Obtenez votre devis gratuit en 2 minutes ici."
        }

    def apply_pas(self, problem, agitation, solution):
        """Applique la méthode PAS : Problème, Agitation, Solution."""
        return {
            "Problème": f"Un accident peut arriver à tout moment.",
            "Agitation": f"Imaginez les factures médicales s'accumulant sans aucune couverture...",
            "Solution": f"LD Assurances règle vos frais d'hospitalisation directement. Respirez."
        }

if __name__ == "__main__":
    ink = CopywriterAgent()
    print(json.dumps(ink.apply_aida("Assurance Vie", "Sécurité financière"), indent=2, ensure_ascii=False))
