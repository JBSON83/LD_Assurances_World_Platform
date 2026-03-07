import os
import logging

class ArchitectAgent:
    def __init__(self):
        self.logger = logging.getLogger("Archie")

    def run_health_check(self, project_path):
        """Vérifie la présence des fichiers critiques et la structure."""
        critical_dirs = ["core", "web", "services", "workflows"]
        missing = []
        for d in critical_dirs:
            if not os.path.exists(os.path.join(project_path, d)):
                missing.append(d)
        
        if missing:
            return False, f"Dossiers manquants : {', '.join(missing)}"
        return True, "Structure du projet valide."

    def security_scan(self, file_path):
        """Scan basique pour détecter des secrets ou des mauvaises pratiques."""
        if not os.path.exists(file_path):
            return "Fichier introuvable."
            
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            if "API_KEY" in content or "PASSWORD" in content:
                return "⚠️ ALERTE : Secrets détectés en clair dans le code !"
        
        return "✅ Scan de sécurité réussi."

if __name__ == "__main__":
    archie = ArchitectAgent()
    status, msg = archie.run_health_check("c:/Users/diffo_jb/OneDrive/Documents/WorkflowAntigravity/LD_Assurances_World_Platform")
    print(f"Santé du projet : {msg}")
