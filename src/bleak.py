import asyncio
from bleak import BleakScanner, BleakClient

# Hue BLE Light Control service/characteristic UUIDs (community reverse-engineered,
# not officially documented by Philips — verify against your bulb's actual GATT table
# if this doesn't work, see the inspection step below)
HUE_SERVICE_UUID = "932c32bd-0000-47a2-835a-a8d455b859dd"
POWER_CHAR_UUID = "932c32bd-0002-47a2-835a-a8d455b859dd"

async def turn_on_bulb(address, name):
    try:
        async with BleakClient(address, timeout=10.0) as client:
            if not client.is_connected:
                print(f"  ✗ Could not connect to {name} ({address})")
                return
            await client.write_gatt_char(POWER_CHAR_UUID, bytearray([0x01]))
            print(f"  ✓ Turned on {name} ({address})")
    except Exception as e:
        print(f"  ✗ Failed on {name} ({address}): {e}")

async def main():
    print("Scanning for BLE devices (15s)...")
    devices = await BleakScanner.discover(timeout=15.0)

    hue_bulbs = [d for d in devices if d.name and "hue" in d.name.lower()]

    if not hue_bulbs:
        print("No Hue bulbs found. Make sure they're powered and advertising (try a power cycle).")
        return

    print(f"Found {len(hue_bulbs)} bulb(s): {[d.name for d in hue_bulbs]}")
    print("Turning them on...")

    # Sequential, not parallel — BLE connections are fragile if you hammer
    # multiple simultaneous connects, especially on macOS
    for d in hue_bulbs:
        await turn_on_bulb(d.address, d.name)

asyncio.run(main())