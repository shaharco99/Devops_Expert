from selenium import webdriver
from selenium.webdriver.common.by import By
my_drive = webdriver.Chrome(executable_path="/home/shahar/Downloads/chromedriver_linux64/chromedriver")
# open ynet
# my_drive.get("http://ynet.co.il")
# open index html and input
find_element = my_drive.find_element
my_drive.get("file:/home/shahar/Desktop/devops_expert/lesson_4/tip_calc/index.html")
find_element(By.ID, "billamt").send_keys("100")
find_element(By.ID, "serviceQual").send_keys("30% - Outstanding")
find_element(By.ID, "music").send_keys("rock")
find_element(By.ID, "peopleamt").send_keys("2")
find_element(By.ID, "calculate").click()
tip_text = find_element(By.XPATH, "/html/body/div/div[1]/button").text
assert tip_text == "15.00"
