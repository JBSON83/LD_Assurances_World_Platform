import os
import json
import time

class PaymentGateway:
    """
    Simulateur de passerelle de paiement réelle (Flutterwave).
    Optimisé pour le marché Africain (Cameroun - MoMo/Orange).
    """
    def __init__(self, provider="flutterwave"):
        self.provider = provider
        # Configuration Flutterwave
        self.secret_key = os.getenv("FLW_SECRET_KEY", "FLWSECK_TEST-xxxxxxxxxxxx-X")
        self.public_key = os.getenv("FLW_PUBLIC_KEY", "FLWPUBK_TEST-xxxxxxxxxxxx-X")

    def initiate_transaction(self, amount, currency, email, phone_number, name):
        """
        Initie une transaction Flutterwave.
        Dans un cas réel, appelle https://api.flutterwave.com/v3/payments
        """
        print(f"💰 [FLUTTERWAVE] Initialisation du paiement pour {name}...")
        tx_ref = f"LD-FLW-{int(time.time())}"
        
        # Structure de données Flutterwave
        payload = {
            "tx_ref": tx_ref,
            "amount": amount,
            "currency": currency,
            "payment_options": "card,mobilemoneycameroun",
            "customer": {
                "email": email,
                "phonenumber": phone_number,
                "name": name
            },
            "customizations": {
                "title": "LD Assurances",
                "description": "Paiement de prime d'assurance",
                "logo": "https://ld-assurances.cm/logo.png"
            }
        }
        
        print(f"💰 [FLUTTERWAVE] Payload généré: {json.dumps(payload, indent=2)}")
        
        return {
            "status": "success",
            "message": "Hosted Link Created",
            "link": f"https://checkout.flutterwave.com/v3/hosted/pay/{tx_ref}"
        }

    def check_status(self, reference):
        """
        Vérifie si le paiement a été validé.
        """
        # Dans un cas réel, on interrogerait l'API du provider
        return {"status": "SUCCESS", "reference": reference}

if __name__ == "__main__":
    gateway = PaymentGateway()
    # Test avec données Flutterwave
    res = gateway.initiate_transaction(80000, "XAF", "client@example.cm", "677123456", "Jean Dupont")
    print(f"Gateway Response: {json.dumps(res, indent=2)}")
