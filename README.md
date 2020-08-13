# joy2key

Map joystick buttons to keyboard keys, to steer in [GTBikeV](https://www.gta5-mods.com/scripts/gt-bike-v) with any (unsupported) joystick.

Uses [Python Windows joystick API](https://github.com/Rabbid76/python_windows_joystickapi) and sample code from [How to generate keyboard events in Python?](https://stackoverflow.com/questions/13564851/how-to-generate-keyboard-events-in-python)

If your joystick has an analog stick you may prefer using [x360ce](https://www.x360ce.com/) for steering. You can still use joy2key to enable/disable auto drive and change radio station, just leave buttons 3 and 4 unmapped in x360ce.

## Mapped buttons:

* D-pad left - Numpad 4 or A
* D-pad right - Numpad 6 or D
* D-pad up - W
* D-pad down - S
* Button 3 - Numpad 1 (auto drive)
* Button 4 - Numpad 7 (radio)
* Button 5 - Toggle smooth steering

Use -v argument to see the joystick buttons numbers.
