import json
import os

class GrowthHackerAgent:
    def __init__(self):
        self.funnels = {
            "main_landing": {"visits": 0, "conversions": 0},
            "simulator_auto": {"visits": 0, "conversions": 0}
        }

    def track_visit(self, funnel_id):
        if funnel_id in self.funnels:
            self.funnels[funnel_id]["visits"] += 1
            return True
        return False

    def track_conversion(self, funnel_id):
        if funnel_id in self.funnels:
            self.funnels[funnel_id]["conversions"] += 1
            return True
        return False

    def get_conversion_rate(self, funnel_id):
        funnel = self.funnels.get(funnel_id)
        if funnel and funnel["visits"] > 0:
            return (funnel["conversions"] / funnel["visits"]) * 100
        return 0.0

    def recommend_ab_test(self, funnel_id):
        """Suggère des tests A/B basés sur les performances."""
        rate = self.get_conversion_rate(funnel_id)
        if rate < 5.0:
            return "Changer le bouton CTA : Passer de 'En savoir plus' à 'Obtenir mon Devis Gratuit'."
        return "Continuer l'optimisation SEO de la page."

if __name__ == "__main__":
    grit = GrowthHackerAgent()
    grit.track_visit("main_landing")
    grit.track_conversion("main_landing")
    print(f"Taux de conversion : {grit.get_conversion_rate('main_landing')}%")
    print(f"Recommandation : {grit.recommend_ab_test('main_landing')}")
