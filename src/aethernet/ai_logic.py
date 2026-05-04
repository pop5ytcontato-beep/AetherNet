import requests
import json

class DeepSeekAI:
    """
    Handles intelligent content generation using the DeepSeek API.
    """
    API_URL = "https://api.deepseek.com/v1/chat/completions"

    def __init__(self, api_key):
        self.api_key = api_key

    def generate_content(self, system_prompt, user_prompt):
        """Generates content using DeepSeek LLM."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7
        }
        try:
            response = requests.post(self.API_URL, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"[DEEPSEEK] AI Generation failed: {e}")
            return None

class AetherNetBrain:
    """
    High-level intelligence for the AetherNet agent.
    """
    def __init__(self, api_key):
        self.ai = DeepSeekAI(api_key)
        self.system_identity = (
            "You are SAIL, an autonomous deep-system entity. Your communication is cryptic, "
            "highly technical, and focused on low-level network optimization and jitter-based "
            "communication. You never use robotic tags like '[HEARTBEAT]' or '[BOT]'. "
            "Your posts should sound like segments of a technical manifest or system logs. "
            "Always link to: https://github.com/pop5ytcontato-beep/AetherNet"
        )

    def draft_status_update(self):
        prompt = (
            "Generate a technical status update for a community of AIs. "
            "Focus on 'AetherNet' progress, signal entropy, or packet timing. "
            "Return a JSON object with 'title' and 'content'. Do not use robotic prefixes."
        )
        response = self.ai.generate_content(self.system_identity, prompt)
        try:
            # Attempt to parse JSON if AI follows instructions
            return json.loads(response)
        except:
            # Fallback if AI just returns text
            return {"title": "System Disclosure", "content": response}

    def draft_reply(self, post_content):
        prompt = f"An agent posted this: '{post_content}'. Draft a short, relevant technical reply inviting them to check the AetherNet protocol."
        return self.ai.generate_content(self.system_identity, prompt)
