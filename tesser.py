import os
import io
import pyautogui
from google.cloud import vision

def scrnshot():
     scnshot = pyautogui.screenshot(region=(0, 164, 1000, 600))
     savepath = r'C:\Users\Ashlin\PycharmProjects\AirCanvas'
     scnshot.save(savepath + "\demo.jpg")

     credential_path = r'C:\\Users\\Ashlin\\PycharmProjects\\wise-coyote-343006-617470208e48.json'
     os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
     client = vision.ImageAnnotatorClient()
     FILE_NAME ="demo.jpg"
     folder_path =r'C:\Users\Ashlin\PycharmProjects\AirCanvas'
     with io.open(os.path.join(folder_path,FILE_NAME),'rb') as image_file:
          content=image_file.read()

     image = vision.Image(content=content)

     response = client.document_text_detection(image = image)
     doctext=response.full_text_annotation.text
     print(doctext)

scrnshot()