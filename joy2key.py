import sys
import time
import joystickapi as joy
import keyboardapi as key

num = joy.joyGetNumDevs()
ret, caps, startinfo = False, None, None
for id in range(num):
    ret, caps = joy.joyGetDevCaps(id)
    if ret:
        print("Gamepad detected: " + caps.szPname)
        ret, startinfo = joy.joyGetPosEx(id)
        break
else:
    print("No gamepad detected.")
    if getattr(sys, 'frozen', False): input()
    sys.exit()

sensitivity = 0.1
pressed = []
left = key.VK_NUMPAD4
right = key.VK_NUMPAD6
smooth = True
toggle_pressed = False
verbose = False
if len(sys.argv) > 1:
    if sys.argv[1] == '-v': verbose = True

def axis(a, n, p):
    if a < -sensitivity:
        if not n in pressed:
            key.PressKey(n)
            pressed.append(n)
    elif n in pressed:
        key.ReleaseKey(n)
        pressed.remove(n)
    if a > sensitivity:
        if not p in pressed:
            key.PressKey(p)
            pressed.append(p)
    elif p in pressed:
        key.ReleaseKey(p)
        pressed.remove(p)

def button(b, k):
    if b:
        if not k in pressed:
            key.PressKey(k)
            pressed.append(k)
    elif k in pressed:
        key.ReleaseKey(k)
        pressed.remove(k)

print("Main wait loop")

while True:
    try:
        time.sleep(0.1)
        ret, info = joy.joyGetPosEx(id)
        if ret:
            x = (info.dwXpos - startinfo.dwXpos) / (startinfo.dwXpos + 1)
            y = (info.dwYpos - startinfo.dwYpos) / (startinfo.dwYpos + 1)
            btns = [(1 << i) & info.dwButtons != 0 for i in range(caps.wNumButtons)]

            axis(x, left, right)
            axis(y, key.KEY_W, key.KEY_S)

            button(btns[2], key.VK_NUMPAD1) # button 3 = auto drive
            button(btns[3], key.VK_NUMPAD7) # button 4 = radio
            if btns[4]:                     # button 5 = smooth steering
                toggle_pressed = True
            elif toggle_pressed:
                if left in pressed:
                    key.ReleaseKey(left)
                    pressed.remove(left)
                if right in pressed:
                    key.ReleaseKey(right)
                    pressed.remove(right)
                if smooth:
                    left = key.KEY_A
                    right = key.KEY_D
                    smooth = False
                else:
                    left = key.VK_NUMPAD4
                    right = key.VK_NUMPAD6
                    smooth = True
                toggle_pressed = False

            if verbose:
                for idx, val in enumerate(btns):
                    if val: print(f'Button {idx}')
                if x < -sensitivity: print('Left')
                elif x > sensitivity: print('Right')
                if y < -sensitivity: print('Up')
                elif y > sensitivity: print('Down')

    except (KeyboardInterrupt, SystemExit):
        break
