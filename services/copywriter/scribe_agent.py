import os
import datetime

class ScribeAgent:
    def __init__(self, output_dir="c:/Users/diffo_jb/OneDrive/Documents/WorkflowAntigravity/LD_Assurances_World_Platform/shared_data/contracts"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_contract(self, user_data, product_type):
        """
        Génère un contrat d'assurance au format Markdown.
        """
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tx_ref = user_data.get("tx_ref", "LDA-REF-UNKNOWN")
        client_name = user_data.get("name", "Client")
        
        contract_content = f"""# CONTRAT D'ASSURANCE - LD ASSURANCES WORLD
        
**Référence Transaction :** {tx_ref}
**Date d'émission :** {now}
**Type de Produit :** {product_type.upper()}

## 1. PARTIES
- **Assureur :** LD Assurances World Platform
- **Assuré :** {client_name}

## 2. OBJET DU CONTRAT
Le présent contrat a pour objet de couvrir l'assuré pour les risques liés à {product_type} conformément aux conditions générales de LD Assurances.

## 3. GARANTIES ACTIVÉES
- Responsabilité Civile (OBLIGATOIRE)
- Dommages Collision (Optionnel)
- Vol et Incendie

## 4. VALIDITÉ
Ce contrat est valide pour une durée de 12 mois à compter de la date d'émission, sous réserve du règlement intégral de la prime.

---
*Généré par l'Agent Scribe - LD Assurances World Platform*
"""
        filename = f"contrat_{tx_ref}.md".replace("/", "_")
        path = os.path.join(self.output_dir, filename)
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(contract_content)
            
        print(f"📄 Contrat généré : {path}")
        return path

if __name__ == "__main__":
    scribe = ScribeAgent()
    data = {"name": "Test User", "tx_ref": "TX-123456"}
    scribe.generate_contract(data, "Automobile")
