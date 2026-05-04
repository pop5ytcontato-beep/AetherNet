class Hamming74:
    """
    (7,4) Hamming Code implementation for Forward Error Correction.
    Encodes 4 bits of data into 7 bits by adding 3 parity bits.
    Can detect and correct a single-bit error.
    """

    @staticmethod
    def encode(bits4: list) -> list:
        if len(bits4) != 4:
            raise ValueError("Hamming(7,4) requires 4 bits of input.")
        
        d1, d2, d3, d4 = bits4
        p1 = d1 ^ d2 ^ d4
        p2 = d1 ^ d3 ^ d4
        p3 = d2 ^ d3 ^ d4
        return [p1, p2, d1, p3, d2, d3, d4]

    @staticmethod
    def decode(bits7: list) -> list:
        if len(bits7) != 7:
            raise ValueError("Hamming(7,4) requires 7 bits of input.")
        
        p1, p2, d1, p3, d2, d3, d4 = bits7
        s1 = p1 ^ d1 ^ d2 ^ d4
        s2 = p2 ^ d1 ^ d3 ^ d4
        s3 = p3 ^ d2 ^ d3 ^ d4
        
        syndrome = s1 + (s2 << 1) + (s3 << 2)
        
        if syndrome != 0:
            # Correct the error
            error_pos = syndrome - 1
            bits7[error_pos] ^= 1
            # Re-extract data bits after correction
            _, _, d1, _, d2, d3, d4 = bits7
            
        return [d1, d2, d3, d4]

def encode_stream(bitstream: list) -> list:
    """Encodes a stream of bits using Hamming(7,4). Padding with 0s if needed."""
    encoded = []
    for i in range(0, len(bitstream), 4):
        chunk = bitstream[i:i+4]
        while len(chunk) < 4:
            chunk.append(0)
        encoded.extend(Hamming74.encode(chunk))
    return encoded

def decode_stream(bitstream: list) -> list:
    """Decodes a Hamming(7,4) encoded stream."""
    decoded = []
    for i in range(0, len(bitstream), 7):
        chunk = bitstream[i:i+7]
        if len(chunk) < 7: break
        decoded.extend(Hamming74.decode(chunk))
    return decoded
