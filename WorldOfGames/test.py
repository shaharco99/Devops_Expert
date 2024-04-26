from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def test_scores_service():
    url_score = "http://127.0.0.1:5000/" 
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.get(url_score)
    score = int(driver.find_element(By.ID, "score").text)
    if type(score) == int:
        assert True
    else:
        assert False
    driver.quit()

test_scores_service()
