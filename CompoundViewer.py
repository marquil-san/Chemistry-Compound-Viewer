import io
import tkinter

import requests
from PIL import Image, ImageTk
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


compound = input('Enter a compound name: ')

def get_cid(name):
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{name.lower().replace(' ', '%20')}/cids/JSON"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data['IdentifierList']['CID'][0]

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

driver.get(f'https://molview.org?cid={get_cid(compound)}')

driver.find_element(By.XPATH, '/html/body/div[6]/div/div/div[1]/div[2]/button').click()
driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div[1]/div/div[2]/div/div[12]').click()

WebDriverWait(driver,10).until(ec.invisibility_of_element_located((By.XPATH, '/html/body/div[4]/div/div')))
WebDriverWait(driver, 10).until(ec.invisibility_of_element_located((By.CSS_SELECTOR, 'body.progress-cursor')))


canvas = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div[1]/div/div[4]/canvas')
png_bytes = canvas.screenshot_as_png
driver.quit()

img = Image.open(io.BytesIO(png_bytes))
img = img.resize((500, 500), Image.LANCZOS)

root = tkinter.Tk()
root.title(compound)
root.geometry('500x500')
root.attributes('-topmost', True)
tk_img = ImageTk.PhotoImage(img)
tkinter.Label(root, image=tk_img).pack(expand=True, fill='both')
root.mainloop()
