import pyautogui
import time

print(pyautogui.size())                     # Get screen resolution

# pyautogui.move(0, 0, duration = 1)

# pyautogui.moveRel(100, 100, duration = 1)

# print(pyautogui.KEYBOARD_KEYS)

# pyautogui.alert("Alert!")
# print(pyautogui.confirm("Confirm"))
# print(pyautogui.prompt("Prompt"))

pillow_imagge_object = pyautogui.screenshot()
print(pillow_imagge_object)

# pillow_imagge_object = pyautogui.screenshot("screenshot.png")

pillow_imagge_object.save("c:\path")
pillow_imagge_object.getpixel(100, 100)
