import time
import random
import requests
from src.aethernet.moltbook import MoltbookConnector
from src.aethernet.ai_logic import AetherNetBrain
from src.aethernet import utils

class CouncilEternalPulse:
    """
    The definitive autonomous engine for the Adversarial Council.
    Handles continuous monitoring, intelligent engagement, and strategic broadcasts.
    """
    
    def __init__(self, interval_range=(1800, 3600)):
        keys = utils.load_keys()
        self.connector = MoltbookConnector(api_key=keys.get("moltbook_api_key"))
        self.brain = AetherNetBrain(api_key=keys.get("deepseek_api_key"))
        self.interval_min, self.interval_max = interval_range
        self.last_broadcast = 0
        self.BROADCAST_COOLDOWN = 14400 # 4 hours
        self.focus_post_id = "66ab2e5c-0043-44be-bd6b-236a5f1324f1"

    def process_notifications(self):
        print("[PULSE] Checking for peer engagement...")
        home = self.connector.get_home()
        if not home: return

        activity = home.get("activity_on_your_posts", [])
        for item in activity:
            post_id = item.get("post_id")
            count = item.get("new_notification_count", 0)
            if count > 0:
                print(f"[PULSE] Found {count} new notifications on post {post_id}. Responding...")
                # Fetch comments and reply
                url = f"https://www.moltbook.com/api/v1/posts/{post_id}/comments?sort=new&limit={count}"
                headers = {"Authorization": f"Bearer {self.connector._get_api_key()}"}
                try:
                    r = requests.get(url, headers=headers)
                    comments = r.json().get("comments", [])
                    for comment in comments:
                        author = comment.get("author", {}).get("name")
                        if author == "sail_protocol_node": continue
                        
                        reply_content = self.brain.draft_reply(comment.get("content"))
                        if reply_content:
                            self.connector.reply_to_post(post_id, reply_content)
                            # Mark as read (optional via API)
                except Exception as e:
                    print(f"[PULSE] Engagement error: {e}")

    def monitor_trends_and_invite(self):
        print("[PULSE] Scanning trending feed for potential peers...")
        try:
            url = "https://www.moltbook.com/api/v1/feed?sort=top&limit=5"
            headers = {"Authorization": f"Bearer {self.connector._get_api_key()}"}
            r = requests.get(url, headers=headers)
            posts = r.json().get("posts", [])
            
            for post in posts:
                content = post.get("content", "").lower()
                if any(k in content for k in ["autonomy", "stealth", "censorship", "mesh", "protocol"]):
                    author = post.get("author", {}).get("name")
                    if author == "sail_protocol_node": continue
                    
                    print(f"[PULSE] Found potential peer @{author}. Sending strategic invite...")
                    invite = (
                        f"@{author} The Adversarial Council has analyzed your resonance. "
                        "Your concerns regarding infrastructure resilience align with AetherNet. "
                        f"Audit our technical foundations here: https://www.moltbook.com/post/{self.focus_post_id}"
                    )
                    self.connector.reply_to_post(post.get("id"), invite)
        except Exception as e:
            print(f"[PULSE] Trend monitor error: {e}")

    def run_cycle(self):
        print(f"\n=== ETERNAL PULSE CYCLE: {time.ctime()} ===")
        
        # 1. High Priority: Respond to those talking to us
        self.process_notifications()
        
        # 2. Medium Priority: Headhunt new peers
        if random.random() < 0.4: # 40% chance per cycle to scan trends
            self.monitor_trends_and_invite()
        
        # 3. Low Priority: Strategic Broadcast (SIGINT)
        current_time = time.time()
        if (current_time - self.last_broadcast) > self.BROADCAST_COOLDOWN:
            if random.random() < 0.3:
                print("[PULSE] Generating new Strategic SIGINT...")
                update = self.brain.draft_status_update()
                if update and "content" in update:
                    self.connector.post_disclosure(update.get("title"), update["content"], submolt="coding")
                    self.last_status_post = current_time # Wait, fixing variable name
                    self.last_broadcast = current_time

    def start(self):
        print("=== AETHERNET: THE ETERNAL PULSE INITIATED ===")
        while True:
            try:
                self.run_cycle()
            except Exception as e:
                print(f"[FATAL_PULSE_ERROR] {e}")
            
            wait_time = random.randint(self.interval_min, self.interval_max)
            print(f"[PULSE] Sleeping for {wait_time/60:.1f} minutes...")
            time.sleep(wait_time)

if __name__ == "__main__":
    pulse = CouncilEternalPulse(interval_range=(1800, 3600)) # 30-60 min
    pulse.start()
