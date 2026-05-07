import requests
import json
import io
import sys
from src.aethernet.utils import load_keys

def get_comments():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    keys = load_keys()
    api_key = keys.get("moltbook_api_key")
    post_id = "2932c0b5-857a-4015-933d-44a36b14e74c"
    url = f"https://www.moltbook.com/api/v1/posts/{post_id}/comments"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    r = requests.get(url, headers=headers)
    data = r.json()
    
    with open("comments_audit.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    for comment in data.get("comments", []):
        author = comment.get("author", {}).get("name")
        content = comment.get("content")
        print(f"--- @{author} ---\n{content}\n")

if __name__ == "__main__":
    get_comments()
