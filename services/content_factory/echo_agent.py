import json
import os

class ContentFactoryAgent:
    def __init__(self, output_dir="generated_content"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def generate_article(self, topic, keywords):
        """
        Simule la génération d'un article SEO par l'agent Echo.
        Dans une version finale, ceci appellerait l'API LLM avec le prompt d'Echo.
        """
        prompt = f"Rédige un article SEO sur '{topic}' avec les mots-clés: {', '.join(keywords)}."
        # Simulation de contenu
        content = f"# {topic}\n\nL'assurance est un pilier de votre sécurité financière... [Contenu généré par Echo pour {topic}]"
        
        filename = f"{topic.lower().replace(' ', '_')}.md"
        path = os.path.join(self.output_dir, filename)
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        
        return path

    def generate_social_media_post(self, platform, hook):
        """Génère un post pour les réseaux sociaux."""
        # Simulation
        post = f"[{platform.upper()}] {hook}\n\nSaviez-vous que 80% des camerounais n'ont pas d'assurance vie ? #LDAssurances #AssuranceCameroun"
        return post

if __name__ == "__main__":
    echo = ContentFactoryAgent(output_dir="c:/Users/diffo_jb/OneDrive/Documents/WorkflowAntigravity/LD_Assurances_World_Platform/services/content_factory/samples")
    path = echo.generate_article("Pourquoi choisir une assurance vie au Cameroun", ["épargne", "retraite", "famille"])
    print(f"Article généré : {path}")
