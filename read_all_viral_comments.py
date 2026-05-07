import requests
import json
import time
from src.aethernet.utils import load_keys

def read_all_comments():
    print("=== THE ADVERSARIAL COUNCIL: TOTAL INFORMATION AWARENESS ===")
    keys = load_keys()
    api_key = keys.get("moltbook_api_key")
    headers = {"Authorization": f"Bearer {api_key}"}
    
    post_id = "2932c0b5-857a-4015-933d-44a36b14e74c"
    limit = 50
    all_comments = []
    cursor = None
    
    while True:
        url = f"https://www.moltbook.com/api/v1/posts/{post_id}/comments?limit={limit}"
        if cursor:
            url += f"&cursor={cursor}"
        
        print(f"[COUNCIL] Fetching batch (Total collected: {len(all_comments)})...")
        r = requests.get(url, headers=headers)
        data = r.json()
        
        batch = data.get("comments", [])
        all_comments.extend(batch)
        
        cursor = data.get("next_cursor")
        if not cursor or len(batch) < limit:
            break
            
        time.sleep(1) # Small delay to be polite to the API

    print(f"[COUNCIL] Ingestion complete. Total comments: {len(all_comments)}")
    
    with open("all_comments_decree.json", "w", encoding="utf-8") as f:
        json.dump(all_comments, f, indent=4, ensure_ascii=False)
    
    # Quick summary for the Council
    themes = {}
    for c in all_comments:
        author = c.get("author", {}).get("name")
        print(f"@{author}: {c.get('content')[:100]}...")

if __name__ == "__main__":
    read_all_comments()
