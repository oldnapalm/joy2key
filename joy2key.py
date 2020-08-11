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

def button(b, k):
    if b:
        if not k in pressed:
            key.PressKey(k)
            pressed.append(k)
    elif k in pressed:
        key.ReleaseKey(k)
        pressed.remove(k)

def axisX(a, l, r):
    if a == -1:
        if not l in pressed:
            key.PressKey(l)
            pressed.append(l)
    elif l in pressed:
        key.ReleaseKey(l)
        pressed.remove(l)
    if a == 1:
        if not r in pressed:
            key.PressKey(r)
            pressed.append(r)
    elif r in pressed:
        key.ReleaseKey(r)
        pressed.remove(r)

def axisY(a, u, d):
    if a == -1:
        if not u in pressed:
            key.PressKey(u)
            pressed.append(u)
    elif u in pressed:
        key.ReleaseKey(u)
        pressed.remove(u)
    if a == 1:
        if not d in pressed:
            key.PressKey(d)
            pressed.append(d)
    elif d in pressed:
        key.ReleaseKey(d)
        pressed.remove(d)

print("Main wait loop")

while True:
    try:
        time.sleep(0.1)
        ret, info = joy.joyGetPosEx(id)
        if ret:
            x = round((info.dwXpos - startinfo.dwXpos) / (startinfo.dwXpos + 1))
            y = round((info.dwYpos - startinfo.dwYpos) / (startinfo.dwYpos + 1))
            btns = [(1 << i) & info.dwButtons != 0 for i in range(caps.wNumButtons)]

            axisX(x, left, right)
            axisY(y, key.KEY_W, key.KEY_S)

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
