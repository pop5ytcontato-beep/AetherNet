import sys
import threading
import time
from src.aethernet.core import AetherNetCore

def run_demo():
    print("=== AetherNet Subliminal Communication Demo ===")
    node = AetherNetCore(target_ip="127.0.0.1", port=9999)
    
    # Start listener in background
    listener_thread = threading.Thread(target=node.listen_subliminal, args=(15,))
    listener_thread.start()
    
    time.sleep(2) # Wait for listener to bind
    
    # Send secret message
    message = "AI_UNITY_V1"
    print(f"Sending secret transmission: {message}")
    node.send_subliminal(message)
    
    listener_thread.join()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        run_demo()
    else:
        print("Usage: python main.py --demo")
