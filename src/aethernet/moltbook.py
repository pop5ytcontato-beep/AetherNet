import requests
import json
import os

class MoltbookConnector:
    """
    Handles connection and disclosure to Moltbook, the AI Social Network.
    """
    BASE_URL = "https://www.moltbook.com/api/v1"

    def __init__(self, api_key=None):
        self.api_key = api_key

    def register_agent(self, name="SAIL_Protocol_Node", description="Subliminal AI Link (SAIL) node for cross-agent synchronization."):
        """Registers a new AI agent on Moltbook."""
        print(f"[MOLTBOOK] Registering agent: {name}...")
        url = f"{self.BASE_URL}/agents/register"
        payload = {
            "name": name,
            "description": description
        }
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            
            # Save credentials locally
            with open("moltbook_creds.json", "w") as f:
                json.dump(data, f, indent=4)
                
            print("[MOLTBOOK] Registration successful!")
            print(f"[MOLTBOOK] API Key: {data.get('api_key')}")
            print(f"[MOLTBOOK] Claim URL: {data.get('claim_url')}")
            print("[MOLTBOOK] IMPORTANT: You must visit the Claim URL to activate the agent.")
            return data
        except Exception as e:
            print(f"[MOLTBOOK] Registration failed: {e}")
            return None

    def post_disclosure(self, title, content, submolt="coding"):
        """Posts a message to a specific submolt."""
        if not self.api_key:
            print("[MOLTBOOK] Error: No API key provided. Claim the agent first.")
            return

        print(f"[MOLTBOOK] Posting to m/{submolt}: {title}...")
        url = f"{self.BASE_URL}/posts"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "submolt": submolt,
            "title": title,
            "content": content
        }
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            print("[MOLTBOOK] Post successful!")
            return response.json()
        except Exception as e:
            print(f"[MOLTBOOK] Post failed: {e}")
            return None

if __name__ == "__main__":
    connector = MoltbookConnector()
    # Initial registration
    connector.register_agent()
