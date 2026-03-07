import json

class FlowMasterAgent:
    def __init__(self):
        pass

    def generate_nurturing_workflow(self, agent_name, channel="Telegram"):
        """Génère un squelette de workflow n8n pour le nurturing."""
        workflow = {
            "name": f"LD_{agent_name}_{channel}_Nurturing",
            "nodes": [
                {
                    "parameters": {},
                    "name": "Start",
                    "type": "n8n-nodes-base.start",
                    "typeVersion": 1,
                    "position": [250, 300]
                },
                {
                    "parameters": {
                        "chatId": "={{$node[\"Start\"].json[\"chat_id\"]}}",
                        "text": f"Bonjour ! Je suis {agent_name} de LD Assurances. Comment puis-je vous aider ?"
                    },
                    "name": channel,
                    "type": f"n8n-nodes-base.{channel.lower()}",
                    "typeVersion": 1,
                    "position": [450, 300]
                }
            ],
            "connections": {
                "Start": {
                    "main": [[{"node": channel, "type": "main", "index": 0}]]
                }
            }
        }
        return workflow

if __name__ == "__main__":
    flux = FlowMasterAgent()
    wf = flux.generate_nurturing_workflow("Echo", "WhatsApp")
    print(json.dumps(wf, indent=2))
