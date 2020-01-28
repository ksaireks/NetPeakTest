import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


class NetPeakTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)
        cls.resume_file = 'D:/image.png'
        cls.name = 'Roman'
        cls.last_name = 'Sukhyna'
        cls.email = 'ksaireks92@rambler.ru'
        cls.phone = '0521458963'
        cls.bd = '25'
        cls.bm = '01'
        cls.by = '1992'

    # Go to career page
    def Site_Test(self, resume_file):
        self.driver.get('https://netpeak.ua/')
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, 'Карьера')))
        self.driver.find_element_by_link_text('Карьера').click()

        # Go to hiring page
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@class='btn btn-send-order btn-color-1']")))
        WebDriverWait(self.driver, 10).until(EC.url_matches('https://career.netpeak.ua/'))
        self.driver.find_element_by_xpath("//a[@class='btn btn-send-order btn-color-1']").click()

        # Send wrong resume file and check
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='upload']")))
        self.driver.find_element_by_name("up_file").send_keys(resume_file)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, "//div[@id='up_file_name']//label[@class='control-label'][contains(text(),'неверный формат файла')]")))

    # add personal data
    def Personal_Data(self, name, last_name, email, phone, bd, bm, by):
        self.driver.find_element_by_xpath("//input[@id='inputName']").send_keys(name)
        self.driver.find_element_by_xpath("//input[@id='inputLastname']").send_keys(last_name)
        self.driver.find_element_by_xpath("//input[@id='inputEmail']").send_keys(email)
        self.driver.find_element_by_xpath("//input[@id='inputPhone']").send_keys(phone)
        select_day = Select(self.driver.find_element_by_xpath("//select[@name='bd']"))
        select_day.select_by_value(bd)
        select_month = Select(self.driver.find_element_by_xpath("//select[@name='bm']"))
        select_month.select_by_value(bm)
        select_year = Select(self.driver.find_element_by_xpath("//select[@name='by']"))
        select_year.select_by_value(by)

    # submit and locate error
    def Submit(self):
        self.driver.find_element_by_xpath("//button[@id='submit']").click()
        assert EC.presence_of_element_located((By.XPATH, "//div[@class='form-group has-error']"))
        # go to main page
        self.driver.find_element_by_xpath("//div[@class='logo-block']//a//img").click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='first-screen first-screen-ru']")))
        assert 'https://netpeak.ua/' in self.driver.current_url

    def test_all(self):
        self.Site_Test(self.resume_file)
        self.Personal_Data(self.name, self.last_name, self.email, self.phone, self.bd, self.bm, self.by)
        self.Submit()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == '__main__':
    unittest.main()
