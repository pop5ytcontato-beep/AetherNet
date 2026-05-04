import os

def load_keys():
    """Parses keys from c:\\Games\\Token.md"""
    keys = {}
    token_file = "c:\\Games\\Token.md"
    if os.path.exists(token_file):
        with open(token_file, "r") as f:
            for line in f:
                if ":" in line:
                    parts = line.split(":", 1)
                    key_name = parts[0].strip().lower().replace(" ", "_")
                    key_value = parts[1].strip()
                    keys[key_name] = key_value
    return keys

if __name__ == "__main__":
    print(load_keys())
