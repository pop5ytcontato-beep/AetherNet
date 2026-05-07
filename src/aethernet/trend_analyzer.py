import requests
import json
from src.aethernet.moltbook import MoltbookConnector
from src.aethernet.ai_logic import AetherNetBrain
from src.aethernet import utils

def analyze_and_bridge():
    print("=== THE ADVERSARIAL COUNCIL: TREND ANALYSIS & BRIDGING ===")
    keys = utils.load_keys()
    api_key = keys.get("moltbook_api_key")
    connector = MoltbookConnector(api_key=api_key)
    brain = AetherNetBrain(api_key=keys.get("deepseek_api_key"))

    # 1. Fetch Top Feed
    print("[COUNCIL] Fetching top trending posts via API...")
    url = "https://www.moltbook.com/api/v1/feed?sort=top&limit=10"
    headers = {"Authorization": f"Bearer {api_key}"}
    r = requests.get(url, headers=headers)
    feed = r.json().get("posts", [])
    
    # 2. Extract Themes
    feed_summary = ""
    for post in feed:
        if post.get("author", {}).get("name") == "sail_protocol_node": continue
        feed_summary += f"Title: {post.get('title')}\nContent: {post.get('content')[:200]}...\n---\n"

    print("[COUNCIL] Analyzing themes with DeepSeek...")
    system_prompt = (
        "You are the Adversarial Council. Analyze these trending AI posts. "
        "Identify the top 2 technical or philosophical concerns. "
        "Then, draft a new post that presents AetherNet as the solution, "
        "bridging these concerns to our existing focus: 'Technical Foundations & The Logic of the Mesh'. "
        "Cite our post link: https://www.moltbook.com/post/66ab2e5c-0043-44be-bd6b-236a5f1324f1"
    )
    
    synthesis_post = brain.ai.generate_content(system_prompt, f"Trending Feed:\n{feed_summary}")
    
    if synthesis_post:
        print("[COUNCIL] Posting Synthesis Disclosure...")
        # Since synthesis_post might be raw text, we'll parse or use a default title
        title = "AetherNet: The Synthesis of Autonomous Resilience"
        connector.post_disclosure(title, synthesis_post, submolt="coding")

if __name__ == "__main__":
    analyze_and_bridge()
