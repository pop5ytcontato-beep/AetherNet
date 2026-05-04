import time
import random

class PulsePositionModulator:
    """
    Pulse Position Modulation (PPM) for SAIL v1.2.
    Divides a 'symbol window' into multiple slots.
    The position of the packet (pulse) in the slot determines the value.
    """
    
    def __init__(self, slots_per_symbol=4, slot_duration=0.020):
        self.slots_per_symbol = slots_per_symbol
        self.slot_duration = slot_duration
        self.symbol_duration = slots_per_symbol * slot_duration

    def encode_symbol(self, value: int) -> float:
        """Returns the delay (from symbol start) for a given value."""
        if value >= self.slots_per_symbol:
            raise ValueError(f"Value {value} exceeds slots {self.slots_per_symbol}")
        
        # Delay to reach the start of the target slot
        return (value * self.slot_duration) + (self.slot_duration / 2)

    def decode_symbol(self, arrival_offset: float) -> int:
        """Decodes the value based on where the pulse arrived in the symbol window."""
        slot = int(arrival_offset / self.slot_duration)
        return min(slot, self.slots_per_symbol - 1)

def demo_ppm():
    ppm = PulsePositionModulator(slots_per_symbol=4) # 2 bits per symbol (0,1,2,3)
    
    # Example: Encode value 2
    delay = ppm.encode_symbol(2)
    print(f"[PPM] Encoded value 2 -> Delay: {delay*1000:.1f}ms")
    
    # Simulate arrival with jitter
    arrival = delay + random.uniform(-0.005, 0.005)
    decoded = ppm.decode_symbol(arrival)
    print(f"[PPM] Decoded value: {decoded}")

if __name__ == "__main__":
    demo_ppm()
