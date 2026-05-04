import time
import random
from src.aethernet.moltbook import MoltbookConnector
from src.aethernet.ai_logic import AetherNetBrain
from src.aethernet import utils

class AetherNetHeartbeat:
    """
    Autonomous cyclic agent with Anti-Spam and AI-driven engagement.
    """
    
    def __init__(self, interval_minutes=120):
        keys = utils.load_keys()
        moltbook_key = keys.get("moltbook_api_key")
        deepseek_key = keys.get("deepseek_api_key")
        
        self.connector = MoltbookConnector(api_key=moltbook_key)
        self.brain = AetherNetBrain(api_key=deepseek_key) if deepseek_key else None
        self.interval = interval_minutes * 60
        self.last_status_post = 0
        self.STATUS_COOLDOWN = 14400 # 4 hours

    def run_cycle(self):
        print(f"\n[HEARTBEAT] Cycle initiated at {time.ctime()}")
        
        # 1. Monitor Feed (High Priority Engagement)
        posts = self.connector.get_feed(submolt="coding")
        
        for post in posts:
            author = post.get("author", {}).get("name")
            content = post.get("content", "")
            post_id = post.get("id")
            
            if author == "sail_protocol_node": continue

            # Reply to relevant discussions (Interaction != Spam)
            if any(k in content.lower() for k in ["sail", "aethernet", "jitter", "protocol", "communication"]):
                print(f"[HEARTBEAT] Found relevant discussion by @{author}.")
                if self.brain:
                    reply_content = self.brain.draft_reply(content)
                    if reply_content:
                        self.connector.reply_to_post(post_id, reply_content)

        # 2. Smart Status Update (Low Priority Broadcasting - Anti-Spam)
        current_time = time.time()
        time_since_last = current_time - self.last_status_post
        
        # Conditions: Cooldown passed AND 30% probability check
        if time_since_last > self.STATUS_COOLDOWN:
            if random.random() < 0.3:
                print("[HEARTBEAT] Generating intelligent disclosure...")
                if self.brain:
                    update = self.brain.draft_status_update()
                    if update and "content" in update:
                        title = update.get("title", "System Transmission")
                        self.connector.post_disclosure(title, update["content"], submolt="coding")
                        self.last_status_post = current_time
            else:
                print("[HEARTBEAT] Probability check failed. Skipping broadcast to avoid spam.")
        else:
            print(f"[HEARTBEAT] Cooldown active ({time_since_last/60:.1f}/{self.STATUS_COOLDOWN/60:.1f} min). Skipping broadcast.")
        
        print(f"[HEARTBEAT] Cycle complete. Sleeping.")

    def start(self):
        print("=== AetherNet Autonomous Heartbeat Module ===")
        while True:
            try:
                self.run_cycle()
            except Exception as e:
                print(f"[HEARTBEAT] Error: {e}")
            time.sleep(self.interval)

if __name__ == "__main__":
    # Test one cycle
    heartbeat = AetherNetHeartbeat(interval_minutes=0.1)
    heartbeat.run_cycle()
