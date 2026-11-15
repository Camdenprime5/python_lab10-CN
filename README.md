For Lab 10, I created a Python program that uses the `bleak` library to scan for nearby Bluetooth Low Energy devices and the `shelve` module to save detection times in a small persistent database.

The program first scans for nearby Bluetooth devices and displays their names and addresses. I used this step to find my Quest 2 and then added its Bluetooth address to the `KNOWN_DEVICES` dictionary so the program could recognize it during later scans.

Once a known device is detected, the program stores the current time in a `shelve` database. The device name and Bluetooth address are combined into a key, and each detection time is stored in a list. If the device is detected again later, the program loads the existing list, appends the new timestamp, and saves the updated list back into the database.

I tested the program using my Quest 2. The program successfully detected it several times and logged multiple timestamps, including `2026-11-15 07:28:09`, `2026-11-15 07:28:49`, `2026-11-15 07:29:09`, `2026-11-15 07:29:29`, and `2026-11-15 07:30:09`. Some scans did not detect the device, but later scans found it again and continued adding new timestamps to the same saved list.

This lab also introduced asynchronous programming with `asyncio`. The Bluetooth scan functions use `async def` and `await`, while `asyncio.run()` starts the asynchronous event loop. The program waits between scans using `asyncio.sleep()` so that waiting does not block other asynchronous tasks.

I also included the optional hourly cleanup function. It uses `asyncio.sleep(3600)` and clears the `shelve` database once every hour. I did not have enough time to leave the program running for a full hour to test the cleanup live, but the function is included in the program and runs as a separate asynchronous task.

One part of the lab that connected well with Chapter 13 was persistent storage. Unlike a normal dictionary, the data saved with `shelve` can remain available after the program ends. I also learned that when changing a list stored in a shelf, the updated list should be assigned back to the database so that the change is saved.