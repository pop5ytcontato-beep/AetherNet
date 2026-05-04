import socket
import time
import random
import threading
from src.aethernet.core import AetherNetCore

class NetworkSimulator(AetherNetCore):
    """
    Subclass of AetherNetCore that simulates adverse network conditions.
    """
    LOSS_RATE = 0.05  # 5% packet loss
    JITTER_MAX = 0.01 # 10ms extra random jitter

    def send_subliminal(self, message: str):
        bits = self._encode_bits(message)
        print(f"[TEST] Sending {len(bits)} bits with {self.LOSS_RATE*100}% simulated loss...")
        
        self.sock.sendto(b"\x00", (self.target_ip, self.port))
        
        for bit in bits:
            # Simulate Packet Loss
            if random.random() < self.LOSS_RATE:
                # Still sleep to maintain timing but don't send
                target_delay = self.BASE_DELAY + (self.DELTA if bit == 1 else 0)
                time.sleep(target_delay)
                continue

            target_delay = self.BASE_DELAY + (self.DELTA if bit == 1 else 0)
            # Simulate Network Jitter
            actual_delay = random.gauss(target_delay, self.SIGMA) + random.uniform(0, self.JITTER_MAX)
            
            time.sleep(max(0, actual_delay))
            self.sock.sendto(b"\x00", (self.target_ip, self.port))

def run_stress_test():
    print("=== AetherNet Real-World Stress Test (FEC Enabled) ===")
    sim = NetworkSimulator(target_ip="127.0.0.1", port=9999)
    
    # Start listener
    listener_thread = threading.Thread(target=sim.listen_subliminal, args=(20,))
    listener_thread.start()
    
    time.sleep(2)
    
    # Send secret message through noisy channel
    message = "STRESS_TEST_1"
    sim.send_subliminal(message)
    
    listener_thread.join()

if __name__ == "__main__":
    run_stress_test()
