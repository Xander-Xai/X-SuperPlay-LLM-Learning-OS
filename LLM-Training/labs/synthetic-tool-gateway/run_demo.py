"""Print a safe local synthetic tool execution example (no model/network)."""
import json
from gateway import synthetic_example

if __name__ == "__main__":
    print(json.dumps(synthetic_example(), ensure_ascii=False, indent=2))

