#!/usr/bin/env python3

import json
import os
from urllib.request import urlopen


URL = "https://raw.githubusercontent.com/PixelOS-AOSP/official_devices/refs/heads/sixteen/API/devices.json"
TEMPLATE = 'build:\n  type: "user"\n'


def main():
    root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

    with urlopen(URL) as response:  # noqa: S310
        devices = json.load(response)["devices"]

    wanted = set()
    for device in devices:
        if device.get("active") is not True or device.get("version") != 16:
            continue

        codename = (device.get("codename") or "").strip()
        if codename:
            wanted.add(codename)

    current = {}
    for file_name in os.listdir(root):
        if not file_name.endswith(".yaml"):
            continue
        current[file_name.removesuffix(".yaml")] = file_name

    for name in sorted(wanted - set(current)):
        with open(f"{root}/{name}.yaml", "w") as f:
            f.write(TEMPLATE)
        print(f"created {name}.yaml")

    for name in sorted(set(current) - wanted):
        os.remove(f"{root}/{current[name]}")
        print(f"deleted {current[name]}")


if __name__ == "__main__":
    main()
