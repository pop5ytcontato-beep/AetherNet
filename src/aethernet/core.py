import socket
import time
import random
import threading
from typing import List
from src.aethernet import fec

class AetherNetCore:
    """
    Core implementation of the Subliminal AI Link (SAIL) protocol.
    Uses Probabilistic Timing Modulation (PTM) to encode data in network jitter.
    """
    
    BARKER_SEQUENCE = [1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1]
    BASE_DELAY = 0.050  # 50ms (Windows friendly)
    DELTA = 0.030       # 30ms variation
    SIGMA = 0.002       # 2ms Gaussian noise

    def __init__(self, target_ip: str = "127.0.0.1", port: int = 9999):
        self.target_ip = target_ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.running = False

    def _encode_bits(self, message: str) -> List[int]:
        """Converts a string to a bitstream including FEC and sync."""
        data_bits = []
        for char in message:
            data_bits.extend([int(b) for b in format(ord(char), '08b')])
        
        # Apply FEC
        encoded_data = fec.encode_stream(data_bits)
        
        bits = []
        bits.extend(self.BARKER_SEQUENCE)
        bits.extend(encoded_data)
        return bits

    def send_subliminal(self, message: str):
        """Sends a message encoded in the timing of empty UDP packets."""
        bits = self._encode_bits(message)
        print(f"[SAIL] Sending {len(bits)} bits via timing modulation...")
        
        # Send prefix packet to establish baseline
        self.sock.sendto(b"\x00", (self.target_ip, self.port))
        
        for bit in bits:
            # Calculate timing based on bit and add Gaussian noise
            target_delay = self.BASE_DELAY + (self.DELTA if bit == 1 else 0)
            actual_delay = random.gauss(target_delay, self.SIGMA)
            
            # Sleep until next transmission
            time.sleep(max(0, actual_delay))
            
            # Send 'dummy' packet
            self.sock.sendto(b"\x00", (self.target_ip, self.port))

    def listen_subliminal(self, duration: int = 10):
        """Listens for timing-modulated packets and attempts to decode."""
        self.sock.bind(("0.0.0.0", self.port))
        self.sock.settimeout(1.0)
        
        arrival_times = []
        print(f"[SAIL] Listening for subliminal signals on port {self.port}...")
        
        start_time = time.time()
        while time.time() - start_time < duration:
            try:
                _, addr = self.sock.recvfrom(1024)
                arrival_times.append(time.perf_counter())
            except socket.timeout:
                continue

        if len(arrival_times) < 2:
            print("[SAIL] No signals detected.")
            return

        # Calculate Inter-Arrival Times (IAT)
        iats = [arrival_times[i] - arrival_times[i-1] for i in range(1, len(arrival_times))]
        
        # Simple threshold decoding (Threshold = Base + Delta/2)
        threshold = self.BASE_DELAY + (self.DELTA / 2)
        decoded_bits = [1 if iat > threshold else 0 for iat in iats]
        
        # Search for Barker Sequence to find start of message
        for i in range(len(decoded_bits) - len(self.BARKER_SEQUENCE)):
            if decoded_bits[i:i+len(self.BARKER_SEQUENCE)] == self.BARKER_SEQUENCE:
                message_bits = decoded_bits[i+len(self.BARKER_SEQUENCE):]
                self._reconstruct_message(message_bits)
                return

        print("[SAIL] Sync sequence not found in stream.")

    def _reconstruct_message(self, bits: List[int]):
        """Decodes FEC and converts bitstream back to characters."""
        # Decode FEC
        decoded_bits = fec.decode_stream(bits)
        
        message = ""
        for i in range(0, len(decoded_bits) - 7, 8):
            byte = decoded_bits[i:i+8]
            char_code = int("".join(map(str, byte)), 2)
            if 32 <= char_code <= 126: # Only printable ASCII
                message += chr(char_code)
            else:
                break
        print(f"[SAIL] Decoded Message: {message}")

if __name__ == "__main__":
    # Example usage:
    # node = AetherNetCore()
    # threading.Thread(target=node.listen_subliminal, args=(5,)).start()
    # time.sleep(1)
    # node.send_subliminal("HELLO AI")
    pass
