from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import sys
import os

# Adding root path for relative imports
# On pointe vers le dossier LD_Assurances_World_Platform car services est dedans
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

from services.front_desk.lola_agent import FrontDeskAgent
from services.payments.gateway import PaymentGateway
from services.copywriter.scribe_agent import ScribeAgent

app = FastAPI(title="LD Assurances Platform API")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

lola = FrontDeskAgent()
gateway = PaymentGateway()
scribe = ScribeAgent()

@app.get("/")
async def root():
    return {"status": "online", "message": "LD Assurances Backend is Running"}

@app.post("/chat")
async def chat_endpoint(request: Request):
    """
    Endpoint de tchat pour Lola.
    """
    data = await request.json()
    message = data.get("message", "")
    if not message:
        raise HTTPException(status_code=400, detail="Message is empty")
    
    response = lola.handle_message(message)
    return {"reply": response}

@app.post("/payments/webhook/flutterwave")
async def flutterwave_webhook(request: Request):
    """
    Webhook pour recevoir les confirmations de paiement de Flutterwave.
    """
    # En production, on vérifierait la signature 'verif-hash'
    data = await request.json()
    
    print(f"🔔 [WEBHOOK] Notification Flutterwave reçue: {data.get('event')}")
    
    if data.get("status") == "successful":
        tx_ref = data.get("tx_ref")
        amount = data.get("amount")
        customer = data.get("customer", {})
        
        # Déclenchement de la génération du contrat via Scribe
        user_data = {
            "name": customer.get("name", "Client"),
            "tx_ref": tx_ref,
            "email": customer.get("email")
        }
        
        # Simulation du type de produit (en réel, on le récupèrerait de la DB via tx_ref)
        product_type = "Automobile" 
        
        contract_path = scribe.generate_contract(user_data, product_type)
        
        print(f"✅ [SUCCÈS] Transaction {tx_ref} confirmée. Contrat généré : {contract_path}")
        return {"status": "acknowledged", "contract_generated": True}
    
    return {"status": "ignored"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
