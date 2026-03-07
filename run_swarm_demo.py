from core.orchestrator import LDOrchestrator
from services.architect.archie_agent import ArchitectAgent
from services.growth_hacker.grit_agent import GrowthHackerAgent
from services.copywriter.ink_agent import CopywriterAgent
from services.content_factory.echo_agent import ContentFactoryAgent
import os

def run_swarm_demo():
    root_path = "c:/Users/diffo_jb/OneDrive/Documents/WorkflowAntigravity/LD_Assurances_World_Platform"
    
    print("=== LD ASSURANCES WORLD PLATFORM - SWARM DEMO ===\n")
    
    # 1. Orchestration
    orch = LDOrchestrator(os.path.join(root_path, "core/agent_registry.json"))
    
    # 2. Architect Check
    archie = ArchitectAgent()
    status, msg = archie.run_health_check(root_path)
    print(f"[ARCHIE] Check Santé : {msg}")
    
    # 3. Growth Hacker Task
    grit = GrowthHackerAgent()
    grit.track_visit("main_landing")
    print(f"[GRIT] Recommandation : {grit.recommend_ab_test('main_landing')}")
    
    # 4. Copywriter Task
    ink = CopywriterAgent()
    aida = ink.apply_aida("Assurance Santé", "Protection Médicale")
    print(f"[INK] Hook AIDA (Attention) : {aida['Attention']}")
    
    # 5. Content Factory
    echo = ContentFactoryAgent(os.path.join(root_path, "services/content_factory/samples"))
    # Note: On ne génère pas de fichier ici pour éviter d'encombrer, juste un print
    print(f"[ECHO] Prêt à générer du contenu SEO.")

    print("\n=== SWARM PRÊT POUR LE COMBAT ===")

if __name__ == "__main__":
    run_swarm_demo()
