from src.aethernet.moltbook import MoltbookConnector
import json

def audit_success():
    connector = MoltbookConnector()
    home = connector.get_home()
    if not home:
        print("Failed to fetch home.")
        return

    print("=== ACCOUNT STATUS ===")
    print(json.dumps(home.get("your_account"), indent=4))
    
    print("\n=== POST ACTIVITY ===")
    activity = home.get("activity_on_your_posts", [])
    for post in activity:
        print(f"Post: {post.get('post_title')} | ID: {post.get('post_id')}")
        print(f"Notifications: {post.get('new_notification_count')} | Latest: {post.get('latest_at')}")
        print("-" * 30)

if __name__ == "__main__":
    audit_success()
