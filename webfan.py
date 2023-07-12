from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common import keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
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

        self.actions = ActionChains(self.driver)

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
                    time.sleep(2)
                    print(f'Element not found: {args}')
                    print(e)
        return element
    
    def maximize(self):
        self.driver.maximize_window()
            
    @tryGeneral
    def clickElement(self, elementXpath):
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, elementXpath))).click()

    @tryGeneral
    def sendKeys(self, elementXpath, text):
        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, elementXpath))).send_keys(text)

    @tryGeneral
    def clearField(self, elementXpath):
        WebDriverWait(self.driver, 20).until(EC.element_to_be_selected((By.XPATH, elementXpath))).clear()

    @tryGeneral
    def getValue(self, elementXpath):
        element = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, elementXpath)))
        return element.get_attribute('value')
    
    @tryGeneral
    def pressEnter(self, elementXpath):
        WebDriverWait(self.driver, 20).until(EC.element_to_be_selected((By.XPATH, elementXpath))).send_keys(keys.Keys.ENTER)

    @tryGeneral
    def clearText(self, elementXpath):
        self.driver.find_element(By.XPATH, elementXpath).click()
        self.actions.key_down(keys.Keys.CONTROL).send_keys('a').key_up(keys.Keys.CONTROL).perform()
        self.driver.find_element(By.XPATH, elementXpath).send_keys(keys.Keys.BACKSPACE)

    @tryGeneral
    def sendKeysName(self, elementName, text):
        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.NAME, elementName))).send_keys(text)
