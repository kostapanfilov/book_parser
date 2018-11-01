from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re


class BaseParser():

    def __init__(self):
        self.driver = webdriver.Firefox()

    def save_data(self, fname):
        pass

    def get_base_page(self, urls):

        for url in urls:
            try:
                self.driver.get(url)
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'z_content')))
                break
            except:
                time.sleep(5)
                print('NEXT_TRY')
                continue
        else:
            print('NO_MAIN_URL')
            return(None)

    def clear_tag(self, s):
        out = re.sub('\n', '', re.sub('<.*?>', '', s))
        return ( out )

    def __del__(self):
        try:
            self.driver.close()
        except:
            pass
