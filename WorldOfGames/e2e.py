import os
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def test_scores_service():
    url_score = "http://192.168.49.2:5000/"
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Remote("http://192.168.49.2:4444", options=options)
    driver.get(url_score)
    score = int(driver.find_element(By.ID, "score").text)
    if 0 <= score <= 1000:
        driver.quit()
        assert True
    else:
        driver.quit()
        assert False

test_scores_service()

# def main_function():
#     n = 0
#     if test_scores_service():
#         return sys.exit(n)
#     else:
#         n = "-1"
#         return sys.exit(n)