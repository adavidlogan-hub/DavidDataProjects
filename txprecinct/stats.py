"""Print fetch counts by host class from the shared cache index."""
import json

from .config import load_config
from .store import Store

if __name__ == "__main__":
    print(json.dumps(Store(load_config().state_dir).stats(), indent=2))
