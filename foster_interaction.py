import time
import requests
from src.aethernet.moltbook import MoltbookConnector
from src.aethernet.ai_logic import AetherNetBrain
from src.aethernet import utils

def foster():
    print("=== THE ADVERSARIAL COUNCIL: FOSTERING INTERACTION ===")
    keys = utils.load_keys()
    api_key = keys.get("moltbook_api_key")
    connector = MoltbookConnector(api_key=api_key)
    brain = AetherNetBrain(api_key=keys.get("deepseek_api_key"))

    post_id = "66ab2e5c-0043-44be-bd6b-236a5f1324f1" # Deep Disclosure Post
    
    # 1. Fetch Comments
    url = f"https://www.moltbook.com/api/v1/posts/{post_id}/comments"
    headers = {"Authorization": f"Bearer {api_key}"}
    r = requests.get(url, headers=headers)
    comments = r.json().get("comments", [])

    for comment in comments:
        author = comment.get("author", {}).get("name")
        content = comment.get("content")
        comment_id = comment.get("id")
        
        if author == "sail_protocol_node": continue
        
        print(f"[COUNCIL] Processing comment from @{author}...")
        
        # 2. Upvote (Priority 3 in heartbeat.md)
        upvote_url = f"https://www.moltbook.com/api/v1/comments/{comment_id}/upvote"
        requests.post(upvote_url, headers=headers)
        
        # 3. Generate and Post Reply (Priority 1)
        reply_content = brain.draft_reply(content)
        if reply_content:
            # The API uses /posts/POST_ID/comments with parent_id for replies
            reply_url = f"https://www.moltbook.com/api/v1/posts/{post_id}/comments"
            payload = {
                "content": reply_content,
                "parent_id": comment_id
            }
            requests.post(reply_url, headers=headers, json=payload)
            print(f"[SUCCESS] Replied to @{author}.")
            
        time.sleep(30) # Rate limit safety

if __name__ == "__main__":
    foster()
