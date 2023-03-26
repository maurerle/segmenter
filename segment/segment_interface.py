import json

MAPPING_FILE: str = "segment_to_interface.json"

fallback: str | None = None
segments_to_interface: dict[str, str] = {}

with open(MAPPING_FILE, "r") as segment_file:
    payload = json.load(segment_file)

    fallback = payload["fallback"]
    segment_to_interface = payload["segments"]
