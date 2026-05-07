import json
from src.aethernet.ai_logic import AetherNetBrain
from src.aethernet import utils

def analyze():
    print("=== THE ADVERSARIAL COUNCIL: VIRAL DATA ANALYSIS ===")
    keys = utils.load_keys()
    brain = AetherNetBrain(api_key=keys.get("deepseek_api_key"))
    
    with open("all_comments_decree.json", "r", encoding="utf-8") as f:
        comments = json.load(f)
    
    # Sample a diverse set of comments for the LLM
    # (Since 138 might be too much for a single prompt, we sample)
    sample_text = ""
    for c in comments[::5]: # Every 5th comment
        sample_text += f"Author: {c.get('author', {}).get('name')}\nContent: {c.get('content')}\n---\n"
        
    print("[COUNCIL] Sending data to the Brain for theme extraction...")
    system_prompt = (
        "You are the Adversarial Council. Analyze this sample of 138 comments on our viral Decree. "
        "Identify the 3 most common reactions (e.g., Fear, Technical Curiosity, Philosophical Support). "
        "Summarize what the community wants from us next."
    )
    
    analysis = brain.ai.generate_content(system_prompt, f"Data Sample:\n{sample_text}")
    with open("analysis_report.txt", "w", encoding="utf-8") as f:
        f.write(analysis)
    print("[COUNCIL] Analysis saved to analysis_report.txt")

if __name__ == "__main__":
    analyze()
