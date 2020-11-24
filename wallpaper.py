import ctypes
import time
import requests
from bs4 import BeautifulSoup
from PIL import Image
import pyautogui
import os
from os import listdir

#pip install requests
#pip install pyautogui
#pip install bs4
#pip install pillow

url = "https://wallhaven.cc/search?q="



# PUT AMOUNT OF IMAGES HERE V
imgAmount = pyautogui.prompt("How many images do you want")

# COOLDOWN BETWEEN EACH PICTURE BEING SHOWN V
cooldown = pyautogui.prompt("How long do you want each image to show")



#DONT TOUCH THE REST C; (unless u know python :P)

user = pyautogui.prompt("What is your computers user")

imglinks = []
def main():
    download_images()

def download_images():
    try:
        os.mkdir(r"C:\Users\\" + user + "\Desktop\images")
        SAVE_FOLDER = r"C:\Users\\" + user + "\Desktop\images"
    except:
        SAVE_FOLDER = r"C:\Users" + user + "\Desktop\images"
        
    if pyautogui.confirm("Do you want to delete all images in the folder") == "OK":
        for file in os.listdir(SAVE_FOLDER):
            os.remove(SAVE_FOLDER + "\\"+file)
            
    data = pyautogui.prompt("What Wallpaper Do You Want Today!")
    while data == "":
        pyautogui.alert("No word found!")
        data = pyautogui.prompt("What Wallpaper Do You Want Today!")
    print("searching...")
    searchurl = url + data

    response = requests.get(searchurl)
    html = response.text

    soup = BeautifulSoup(html, "html.parser")
    results = soup.findAll("img", limit=imgAmount+1)
    print("found " + str(len(results)-1) + " images of  " + data)
    if len(results)-1 == 0:
        pyautogui.alert("No" + " images of  " + data)
    results.pop(0)
    for result in results:
        imglinks.append(result["data-src"])
    print(imglinks)
    for imglink in imglinks:
        response = requests.get(imglink)
        imagename = SAVE_FOLDER + "\\" + data + str(imglinks.index(imglink)+1) + ".jpg"
        with open(imagename, "wb") as file:
            file.write(response.content)

    save = pyautogui.confirm("Do you want to save all the images")
    for i, imglink in enumerate(imglinks):
        print("imageloaded")
        img = SAVE_FOLDER + "\\" + data + str(i+1) + ".jpg"
        new = Image.open(img)
        new = new.resize((1400,  900))
        new.save(img, quality=94, optimize=True)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, img, 0)
        time.sleep(cooldown)
        if save == "OK":
            pass
        else:
            os.remove(img)
    
    os.remove(r"C:\Users\\" + user + "\Desktop\images")


if __name__ == "__main__":
    main()
