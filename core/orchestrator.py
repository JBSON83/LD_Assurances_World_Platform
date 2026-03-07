import json
import os
import logging

class LDOrchestrator:
    def __init__(self, registry_path="agent_registry.json"):
        self.registry_path = registry_path
        self.agents = {}
        self.logger = logging.getLogger("OrchID")
        logging.basicConfig(level=logging.INFO)
        self.load_registry()

    def load_registry(self):
        """Charge la configuration des agents depuis le fichier JSON."""
        try:
            with open(self.registry_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for agent in data["agents"]:
                    self.agents[agent["id"]] = agent
            self.logger.info(f"Registry chargé : {len(self.agents)} agents prêts.")
        except Exception as e:
            self.logger.error(f"Erreur lors du chargement du registry : {e}")

    def get_agent_prompt(self, agent_id):
        """Récupère le prompt système d'un agent spécifique."""
        agent = self.agents.get(agent_id)
        if agent:
            return agent["prompt"]
        return None

    def delegate_task(self, task_description, preferred_agent=None):
        """
        Logique de délégation simplifiée. 
        Dans une version avancée, cette méthode utiliserait un LLM pour décider à qui envoyer la tâche.
        """
        self.logger.info(f"Nouvelle tâche reçue : {task_description}")
        if preferred_agent and preferred_agent in self.agents:
            self.logger.info(f"Délégation à l'agent : {self.agents[preferred_agent]['name']}")
            return True, preferred_agent
        
        # Logique de routage basique par mots-clés
        if "site" in task_description or "code" in task_description:
            return True, "devo"
        elif "vendre" in task_description or "texte" in task_description:
            return True, "ink"
        elif "acquisition" in task_description or "trafic" in task_description:
            return True, "grit"
        
        return False, "orchid"

if __name__ == "__main__":
    # Test basique
    orchestrator = LDOrchestrator(registry_path="c:/Users/diffo_jb/OneDrive/Documents/WorkflowAntigravity/LD_Assurances_World_Platform/core/agent_registry.json")
    success, agent = orchestrator.delegate_task("Nous devons créer la structure du site Next.js")
    print(f"Agent assigné : {agent}")
