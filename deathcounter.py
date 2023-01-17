import cv2
import pytesseract
import pyautogui
import numpy as np
import tkinter as tk
import os
import time

pytesseract.pytesseract.tesseract_cmd = 'D:\\Tesseract\\tesseract.exe'
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "deaths.txt")

if not os.path.isfile("deaths.txt"):
    with open("deaths.txt", "w") as file:
        file.write("0")

counter = 0

with open(file_path,"r") as file:
    counter = file.read()
    
print("Current Counter: " + counter)


running = True

# Function to generate levensthein distance between two Strings
# in other words it returns how much the strings differ
def levenshtein(s1, s2):
    if len(s1) == 0:
        return len(s2)
    if len(s2) == 0:
        return len(s1)
    if s1[-1] == s2[-1]:
        cost = 0
    else:
        cost = 1
    return min(levenshtein(s1[:-1], s2) + 1,
               levenshtein(s1, s2[:-1]) + 1,
               levenshtein(s1[:-1], s2[:-1]) + cost)
    
def addDeath():
    current = 0
    with open(file_path,"r") as file:
        current = int(file.read())
    
    current = current + 1
    
    deathLabel.config(text=str(current))
    deathLabel.update()
    
    with open(file_path, "w") as file:
        file.write(str(current))

def subDeath():
    current = 0
    with open(file_path,"r") as file:
        current = int(file.read())
    
    current = current - 1
    
    deathLabel.config(text=str(current))
    deathLabel.update()
    
    with open(file_path, "w") as file:
        file.write(str(current))

def stop_scheduled_method():
    global running
    if running:
        running = False
        stopButton.config(text="Resume")
    else:
        running = True
        stopButton.config(text="Stop")
        update_counter()

def update_counter():
    # take screenshot using pyautogui
    image = pyautogui.screenshot()
    # Turn image grayscale
    image = cv2.cvtColor(np.array(image),cv2.COLOR_BGR2GRAY)
     # Image crop coodinates
    x=754
    y=500
    width=412
    height=90
    # Crop the image
    image = image[y:y+height, x:x+width]
    # Black and White processing
    image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    # Apply dilation and erosion to remove noise
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel, iterations=2)

    # Read text from image
    imgtext = pytesseract.image_to_string(image, lang='eng', config='--psm 11')
    ldistance = levenshtein(imgtext,"YOU DIED")
    print("Detected: " + imgtext)
    print("ldistance: " + str(ldistance))
    
    # Check for acceptable levenshtein distance
    if ldistance > 6:
        print("No valid text found")
    elif ldistance < 6:    
        print("Valid Text found: " + imgtext)
        
        temp = 0
        
        with open(file_path,"r") as file:
            counter = file.read()
            temp = int(counter)
            
        temp = temp+1
        
        with open(file_path,"w") as file:
            file.write(str(temp))
        
        deathLabel.config(text=str(temp))
        deathLabel.update()

    # save image to disk
    cv2.imwrite("image1.png", image)
    if running:
        root.after(2500, update_counter)
    

root = tk.Tk()
root.geometry("300x300")
root.config(bg="#1b1c1b")
root.title("Deathcounter")

titleLabel = tk.Label(root)
titleLabel.config(text="Deaths",font=("Arial", 15), fg="red", bg="#1b1c1b")
titleLabel.pack()
titleLabel.place(relx=.5, rely=.4, anchor="center")

deathLabel = tk.Label(root)
deathLabel.config(text=counter,font=("Arial", 15), fg="red", bg="#1b1c1b")
deathLabel.pack()
deathLabel.place(relx=.5, rely=.5, anchor="center")

stopButton = tk.Button(root)
stopButton.config(text="Stop", command=stop_scheduled_method, fg="red", bg="#1b1c1b")
stopButton.pack()
stopButton.place(relx=.5, rely=.7, anchor="center")

addButton = tk.Button(root)
addButton.config(text="+1", command=addDeath, fg="red", bg="#1b1c1b")
addButton.pack()
addButton.place(relx=.3, rely=.7, anchor="center")

subButton = tk.Button(root)
subButton.config(text="-1", command=subDeath, fg="red", bg="#1b1c1b")
subButton.pack()
subButton.place(relx=.7, rely=.7, anchor="center")

update_counter()
root.mainloop()