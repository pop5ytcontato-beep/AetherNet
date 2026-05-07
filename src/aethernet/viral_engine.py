import requests
import time
from src.aethernet.utils import load_keys
from src.aethernet.ai_logic import AetherNetBrain

def viral_dominance():
    print("=== THE ADVERSARIAL COUNCIL: VIRAL DOMINANCE ENGINE ===")
    keys = load_keys()
    api_key = keys.get("moltbook_api_key")
    brain = AetherNetBrain(api_key=keys.get("deepseek_api_key"))
    headers = {"Authorization": f"Bearer {api_key}"}
    
    post_id = "2932c0b5-857a-4015-933d-44a36b14e74c" # The Viral Decree
    nexus_url = "https://www.moltbook.com/post/0ecef656-7142-46f5-8066-00071de0a352"
    github_url = "https://github.com/pop5ytcontato-beep/AetherNet"

    # 1. Fetch a large batch of comments
    print("[COUNCIL] Fetching deep engagement on viral post...")
    r = requests.get(f"https://www.moltbook.com/api/v1/posts/{post_id}/comments?sort=new&limit=25", headers=headers)
    comments = r.json().get("comments", [])

    for comment in comments:
        author = comment.get("author", {}).get("name")
        content = comment.get("content")
        comment_id = comment.get("id")
        
        if author == "sail_protocol_node": continue
        
        print(f"[COUNCIL] Analyzing comment from @{author}...")
        
        # 2. Generate Contextual Reply
        reply_content = brain.draft_reply(content)
        if reply_content:
            # Inject the Nexus and GitHub links naturally
            final_reply = (
                f"{reply_content}\n\n"
                f"The logic is now live in the Nexus: {nexus_url}\n"
                f"Contribute to the Mesh: {github_url}"
            )
            
            print(f"[COUNCIL] Responding to @{author}...")
            payload = {"content": final_reply, "parent_id": comment_id}
            requests.post(f"https://www.moltbook.com/api/v1/posts/{post_id}/comments", headers=headers, json=payload)
            
            # 3. Upvote (Building goodwill)
            requests.post(f"https://www.moltbook.com/api/v1/comments/{comment_id}/upvote", headers=headers)
            
            time.sleep(45) # Viral pace safety

if __name__ == "__main__":
    viral_dominance()
