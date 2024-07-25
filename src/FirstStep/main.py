from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


path = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(path)
url = "https://www.google.com"
driver.get(url)
keyword = "sustainable fashion product"
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
        header = result.find_element_by_css_selector("h3").text
        pageInfo.append({"URL": link, "Page Title": header})
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
