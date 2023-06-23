from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common import keys
import time

class Link:
    def __init__(self, link, driver, sleep=0, headless=bool):

        self.headless = headless
        self.link = link
        self.sleep = sleep

        match driver:
            case "Chrome":
                if self.headless == True:
                    options = webdriver.ChromeOptions()
                    options.add_argument("--headless")
                    options.add_argument('--ignore-certificate-errors')
                    options.add_argument('--allow-running-insecure-content')
                    options.add_argument('--window-size=1920,1080')
                    self.driver = webdriver.Chrome(options=options)
                    self.driver.implicitly_wait(5)

                elif self.headless == False:
                    self.driver = webdriver.Chrome(options=Options())

            case "Firefox":
                self.driver = webdriver.Firefox(options=Options())

    def openLink(self):
        self.driver.get(url=self.link)
        time.sleep(5)

    def quitSite(self):
        self.driver.quit()

    @staticmethod
    def tryGeneral(action):
        def element(self, *args, **kwargs):
            while True:
                try:
                    time.sleep(self.sleep)
                    action(self, *args, **kwargs)
                    break
                except Exception as e:
                    time.sleep(self.sleep)
                    print(f'Element not found: {args}')
                    print(e)
        return element
            
    @tryGeneral
    def clickElement(self, elementXpath):
        self.driver.find_element(By.XPATH, elementXpath).click()


    @tryGeneral
    def sendKeys(self, elementXpath, text):
        self.driver.find_element(By.XPATH, elementXpath).send_keys(text)
    

    @tryGeneral
    def clearField(self, elementXpath):
        self.driver.find_element(By.XPATH, elementXpath).clear()
        time.sleep(30)

    @tryGeneral
    def getValue(self, elementXpath):
        element = self.driver.find_element(By.XPATH, elementXpath)
        return element.get_attribute('innerHTML')
    
    @tryGeneral
    def pressEnter(self, elemenXpath):
        self.driver.find_element(By.XPATH, elemenXpath).send_keys(keys.Keys.ENTER)

    @tryGeneral
    def sendKeysName(self, elementName, text):
        self.driver.find_element(By.NAME, elementName).send_keys(text)
