from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
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
from core.admin_manager import admin_manager

app = FastAPI(title="LD Assurances Platform API")

# Simple Admin Session Store (In-memory for simplicity, keys are generated on login)
ADMIN_SESSIONS = set()

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

# --- Public Endpoints ---

@app.get("/")
async def root():
    return {"status": "online", "version": "1.0", "message": "LD Assurances Backend is Running"}

@app.get("/pixel-config")
async def get_pixel_config():
    """Endpoint public pour pixel.js pour récupérer les IDs de tracking."""
    return admin_manager.get_all_settings()

@app.post("/chat")
async def chat_endpoint(request: Request):
    data = await request.json()
    message = data.get("message", "")
    if not message:
        raise HTTPException(status_code=400, detail="Message is empty")
    
    response = lola.handle_message(message)
    return {"reply": response}

# --- Admin Endpoints ---

@app.post("/admin/login")
async def admin_login(request: Request):
    data = await request.json()
    user = data.get("username")
    pwd = data.get("password")
    
    print(f"🔑 [ADMIN LOGIN] Tentative pour: '{user}' (Mot de passe: {len(pwd) if pwd else 0} chars)")
    
    # Default credentials or stored password
    stored_pass = admin_manager.get_setting("ADMIN_PASS") or "admin123"
    
    if user == "admin" and pwd == stored_pass:
        import secrets
        session_token = secrets.token_hex(16)
        ADMIN_SESSIONS.add(session_token)
        print("✅ [ADMIN LOGIN] Succès !")
        return {"token": session_token}
    
    print(f"❌ [ADMIN LOGIN] Échec. Attendu: 'admin'/'{stored_pass}'")
    raise HTTPException(status_code=401, detail="Invalid credentials")

async def verify_admin(request: Request):
    token = request.headers.get("Authorization")
    if token not in ADMIN_SESSIONS:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True

@app.get("/admin/config")
async def get_config(request: Request):
    await verify_admin(request)
    return admin_manager.get_all_settings()

@app.post("/admin/config")
async def update_config(request: Request):
    await verify_admin(request)
    data = await request.json()
    for key, value in data.items():
        admin_manager.set_setting(key, value)
    return {"status": "updated"}

@app.post("/admin/change-password")
async def change_password(request: Request):
    await verify_admin(request)
    data = await request.json()
    new_pwd = data.get("password")
    if not new_pwd:
        raise HTTPException(status_code=400, detail="Password is required")
    # In this simple implementation, we store it as a setting
    admin_manager.set_setting("ADMIN_PASS", new_pwd)
    return {"status": "password updated"}

@app.get("/config/public")
async def get_public_config():
    """Endpoint public pour le contenu du site (Coordonnées, SEO, Maintenance)."""
    all_settings = admin_manager.get_all_settings()
    # Filter only public keys for security
    public_keys = [
        "SITE_PHONE", "SITE_EMAIL", "SITE_ADDRESS", 
        "LOLA_MESSAGE", "LOLA_ENABLED", "TELEGRAM_LINK", "WHATSAPP_LINK",
        "SIM_AUTO_RATE", "SIM_HEALTH_RATE", "SIM_HOME_RATE",
        "MAINTENANCE_MODE", "SEO_TITLE", "SEO_DESCRIPTION"
    ]
    return {k: all_settings.get(k) for k in public_keys if k in all_settings}

@app.get("/admin/api-keys")
async def list_keys(request: Request):
    await verify_admin(request)
    return admin_manager.list_api_keys()

@app.post("/admin/api-keys")
async def generate_key(request: Request):
    await verify_admin(request)
    data = await request.json()
    name = data.get("name", "Unnamed Key")
    token = admin_manager.generate_api_key(name)
    return {"token": token}

@app.post("/admin/api-keys/revoke")
async def revoke_key(request: Request):
    await verify_admin(request)
    data = await request.json()
    token = data.get("token")
    admin_manager.revoke_api_key(token)
    return {"status": "revoked"}

# --- External Data Exchange (Protected by API Keys) ---

@app.get("/api/v1/data-exchange")
async def data_exchange(request: Request):
    api_key = request.headers.get("X-API-Key")
    if not admin_manager.validate_api_key(api_key):
        raise HTTPException(status_code=403, detail="Invalid API Key")
    
    # Logic to return shared data
    return {"data": "Secure data from Jemassurance Platform"}

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

# Serve static files from the 'web' directory
web_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "web")
app.mount("/", StaticFiles(directory=web_dir, html=True), name="web")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
