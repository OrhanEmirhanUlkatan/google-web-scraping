from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
from bs4 import BeautifulSoup
import requests
import openpyxl

path = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(path)
url = "https://www.google.com"
driver.get(url)
keyword = "suitable fashion products"
searchBar = driver.find_element_by_name("q")
searchBar.send_keys(keyword)
searchBar.send_keys("\n")
import time

time.sleep(10)


def scrape():
    pageInfo = []
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "g"))
        )
    except Exception as e:
        print(e)
        driver.quit()
    searchResults = driver.find_elements_by_class_name("g")
    for result in searchResults:
        element = result.find_element_by_css_selector("a")
        link = element.get_attribute("href")
        pageInfo.append({"URL": link})
    return pageInfo


numPages = 5
infoAll = []
infoAll.extend(scrape())
for i in range(0, numPages - 1):
    nextButton = driver.find_element_by_link_text("Next")
    nextButton.click()
    infoAll.extend(scrape())
df = pd.DataFrame(infoAll)
df.to_excel("Search Results.xlsx", index=False)
driver.quit()

urls = []
wb = openpyxl.load_workbook("Search Results.xlsx")
ws = wb["Sheet1"]
for i in range(2, 54):
    urls.append(ws.cell(row=i, column=1).hyperlink.target)
count = 2
for url in urls:
    res = requests.get(url)
    html_page = res.content
    soup = BeautifulSoup(html_page, "html.parser")
    images = soup.find_all("img", src=True)
    print("%d. Scanned photos from the link with indis number " % (count))
    image_src = [x["src"] for x in images]
    image_src = [
        x
        for x in image_src
        if x.endswith(".jpg") & x.startswith("http")
        or x.endswith(".jpeg") & x.startswith("http")
        or x.endswith(".png") & x.startswith("http")
    ]
    image_count = 1
    os.mkdir(str(count))
    os.chdir("./" + str(count))
    count += 1
    for image in image_src:
        with open("image_" + str(image_count) + ".jpg", "wb") as f:
            res = requests.get(image)
            f.write(res.content)
        image_count = image_count + 1
    os.chdir("C:/Users/ULKATAN/Desktop/Final/Final")
print(
    "[INFO] Download Completed. Please note that some photos were not downloaded because they were not in the correct format."
)
