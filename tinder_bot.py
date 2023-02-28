import undetected_chromedriver as uc
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from time import sleep
import datetime
import random

# MacOS workaround to use Default Profile; Must already be authenticated in Tinder & Bumble
os.system("open /Applications/ChromeSelenium.app --args https://www.bumble.com --new-window --remote-debugging-port=9222")

class TinderBot():
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
        self.driver = webdriver.Chrome(executable_path=r'/Applications/chromedriver.exe', options=options)

    def enter_bumble(self):
        wait = WebDriverWait(self.driver, 20) 
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="page"]/div/div/div[1]/div/div[2]/div/div[2]/div/div[2]/div[1]/div/div[2]/a'))).click()
        sleep(10)

    def open_tinder(self):
        self.driver.get('https://tinder.onelink.me/9K8a/3d4abb81')
        sleep(10)
        print("Successfully logged into Tinder!")

    def right_swipe(self):
        doc = self.driver.find_element('xpath', '/html')
        doc.send_keys(Keys.ARROW_RIGHT)

    def auto_swipe(self):
        stop_time = datetime.datetime.now() + datetime.timedelta(minutes=4)
        while True:
            sleep(2)
            if datetime.datetime.now() > stop_time:
                return False
            try:
                if self.driver.find_element('xpath', '//*[@id="main"]/div/div[1]/main/div[2]/article/div'):
                    self.close_bumble_match()
                else:
                    self.right_swipe()
            except:
                try:
                    self.right_swipe()
                except:
                    print("Can't swipe or close")

    def close_bumble_match(self):
        match_popup = self.driver.find_element('xpath', '//*[@id="main"]/div/div[1]/main/div[2]/article/div/footer/div[2]/div[2]/div/span/span/span/span')
        match_popup.click()

    def get_matches(self):
        print("Getting matches..")
        match_profiles = self.driver.find_elements('class name', 'matchListItem')
        message_links = []
        for profile in match_profiles:
            if profile.get_attribute('href') == 'https://tinder.com/app/my-likes' or profile.get_attribute('href') == 'https://tinder.com/app/likes-you':
                continue
            message_links.append(profile.get_attribute('href'))
        return message_links

    def send_messages_to_matches(self):
        links = self.get_matches()
        message_list = ["Hi", "Hey what's up?", "Hey :)", "How's it going?"]
        for link in links:
            print("Original list is : " + str(message_list))
            rand_idx = random.randrange(len(message_list))
            random_message = message_list[rand_idx]
            print("First message is: " + str(random_message))
            self.send_message(link, random_message)

    def send_message(self, link, random_message):
        self.driver.get(link)
        sleep(3)
        text_area = self.driver.find_element('xpath', '/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div/div/div[3]/form/textarea')
        text_area.send_keys(random_message)
        text_area.send_keys(Keys.ENTER)

    def quit_session(self):
        print("quitting...")
        self.driver.close()
        self.driver.quit()

bot = TinderBot()
bot.enter_bumble()
bot.auto_swipe()
sleep(30)
bot.open_tinder()
bot.auto_swipe()
bot.send_messages_to_matches()
bot.quit_session()