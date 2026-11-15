import asyncio
import shelve
from time import strftime, gmtime

from bleak import BleakScanner


# Add the device names and addresses you want to monitor here.
# Example:
# KNOWN_DEVICES = {
#     "My Phone": "AA:BB:CC:DD:EE:FF",
# }
KNOWN_DEVICES = {
    "Quest 2": "B4:17:A8:AE:76:3B"
}

DATABASE_NAME = "device_log"
SCAN_INTERVAL = 15


async def scan_for_devices():
    """Scan once and print every Bluetooth LE device that Bleak discovers."""
    print("Scanning for Bluetooth devices...")
    devices = await BleakScanner.discover()

    for device in devices:
        print(f"Device Name: {device.name}, Address: {device.address}")

    return devices


async def check_for_known_devices():
    """Return any devices whose addresses appear in KNOWN_DEVICES."""
    devices = await BleakScanner.discover()
    nearby_known_devices = {}

    known_by_address = {
        address: name for name, address in KNOWN_DEVICES.items()
    }

    for device in devices:
        if device.address in known_by_address:
            device_name = known_by_address[device.address]
            print(f"{device_name} is nearby!")
            nearby_known_devices[device_name] = device.address

    return nearby_known_devices


def log_devices(devices):
    """Store the current UTC time for each detected known device."""
    with shelve.open(DATABASE_NAME) as db:
        for name, address in devices.items():
            key = name + "_" + address
            formatted_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

            if key in db:
                time_list = db[key]
                time_list.append(formatted_time)

                # With shelve, assign a modified list back to save the change.
                db[key] = time_list
            else:
                db[key] = [formatted_time]

    print("Logged devices in the shelf database.")


def verify_log():
    """Print everything currently stored in the shelf database."""
    print("Verifying log...")

    with shelve.open(DATABASE_NAME) as db:
        if not db:
            print("The device log is currently empty.")
            return

        for key, times in db.items():
            print(f"{key}: {times}")


async def scan():
    """Scan once for known devices and log any that are nearby."""
    nearby_devices = await check_for_known_devices()

    if nearby_devices:
        log_devices(nearby_devices)
    else:
        print("No known devices nearby.")


async def clear_logs_hourly():
    """OPTIONAL +10: clear the shelf database once every hour."""
    while True:
        await asyncio.sleep(3600)

        with shelve.open(DATABASE_NAME) as db:
            db.clear()

        print("Cleared the device log.")


async def main():
    # If no known devices have been entered yet, do one discovery scan.
    if not KNOWN_DEVICES:
        await scan_for_devices()
        print(
            "\nCopy the device address(es) you want into KNOWN_DEVICES, then run again."
        )
        return

    # OPTIONAL +10: run the hourly cleanup alongside the scanning loop.
    cleanup_task = asyncio.create_task(clear_logs_hourly())

    try:
        while True:
            print("\nScanning...")
            await scan()

            verify_log()

            print(f"Sleeping {SCAN_INTERVAL} seconds until next scan...")
            await asyncio.sleep(SCAN_INTERVAL)

    finally:
        cleanup_task.cancel()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram stopped.")