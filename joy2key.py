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

pressed = []
left = key.VK_NUMPAD4
right = key.VK_NUMPAD6
smooth = True
select = False
verbose = False
if len(sys.argv) > 1:
    if sys.argv[1] == '-v': verbose = True

def axis(a, n, p):
    if a == -1:
        if not n in pressed:
            key.PressKey(n)
            pressed.append(n)
    elif n in pressed:
        key.ReleaseKey(n)
        pressed.remove(n)
    if a == 1:
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
            x = round((info.dwXpos - startinfo.dwXpos) / (startinfo.dwXpos + 1))
            y = round((info.dwYpos - startinfo.dwYpos) / (startinfo.dwYpos + 1))
            btns = [(1 << i) & info.dwButtons != 0 for i in range(caps.wNumButtons)]

            axis(x, left, right)
            axis(y, key.KEY_W, key.KEY_S)

            button(btns[0], key.VK_NUMPAD1) # button 1 = auto drive
            button(btns[3], key.VK_NUMPAD7) # button 4 = radio

            if btns[8]: # button SELECT = smooth steering
                select = True
            else:
                if select:
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
                select = False

            if verbose:
                for idx, val in enumerate(btns):
                    if val: print(f'Button {idx}')
                if x == -1: print('Left')
                elif x == 1: print('Right')
                if y == -1: print('Up')
                elif y == 1: print('Down')

    except (KeyboardInterrupt, SystemExit):
        break
