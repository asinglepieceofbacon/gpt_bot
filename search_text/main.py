import pytesseract
import cv2

def search_text(img, lang1='eng', lang2='rus'):
    image_path = img
    image = cv2.imread(image_path)
    grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    pytesseract.pytesseract.tesseract_cmd = r'C:/program files/Tesseract-OCR/tesseract.exe'
    text = pytesseract.image_to_string(image, lang=f'{lang1}+{lang2}')

    return text
