from selenium import webdriver
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import logging
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException

class bot:

    def __init__(self, username, password, audience, message):
      
        # initializing the username
        self.username = username
        
        # initializing the password
        self.password = password
        
        # passing the list of user or initializing
        self.user = user
        
        # passing the message of user or initializing
        self.message = message
        
        # initializing the base url.
        self.base_url = 'https://www.instagram.com/'
        
        # here it calls the driver to open chrome web browser.
        self.bot = driver
        
        # Set up logging for pop-up handling
        logging.basicConfig(
            filename='popup_handling.log',
            level=logging.INFO,
            format='%(asctime)s %(levelname)s:%(message)s'
        )
        # initializing the login function we will create
        self.login()
        # Handle all pop-ups after login
        self.handle_all_popups(max_popups=10, max_failures=3)
        # initializing the send message function we will create
        self.send_message()
    def handle_all_popups(self, max_popups=10, max_failures=3):
        """
        Handles a sequence of Instagram pop-ups by clicking the 'Not Now' or similar button.
        Tracks which pop-ups were closed, retries on failure, and logs each attempt.
        Stops after max_popups or if too many failures occur.
        """
        popup_xpath = '/html/body/div[4]/div/div/div/div[3]/button[2]'
        closed_popups = 0
        failures = 0
        for i in range(max_popups):
            try:
                # Wait up to 6 seconds for the pop-up to appear
                WebDriverWait(self.bot, 6).until(
                    expected_conditions.element_to_be_clickable((By.XPATH, popup_xpath))
                )
                try:
                    self.bot.find_element(By.XPATH, popup_xpath).click()
                    closed_popups += 1
                    logging.info(f"Pop-up {i+1} closed successfully.")
                except (ElementClickInterceptedException, NoSuchElementException) as e:
                    # Retry once if click fails
                    time.sleep(1)
                    try:
                        self.bot.find_element(By.XPATH, popup_xpath).click()
                        closed_popups += 1
                        logging.info(f"Pop-up {i+1} closed on retry.")
                    except Exception as retry_e:
                        failures += 1
                        logging.warning(f"Pop-up {i+1} failed to close after retry: {retry_e}")
                        if failures >= max_failures:
                            logging.error("Too many pop-up handling failures. Stopping pop-up handler.")
                            break
                # Add a small delay to allow next pop-up to load
                time.sleep(1.2)
            except TimeoutException:
                # No more pop-ups detected
                logging.info(f"No more pop-ups detected after {closed_popups} closed.")
                break
        logging.info(f"Pop-up handling complete. Total closed: {closed_popups}, Failures: {failures}")
    def login(self):
        # opening the base url
        self.bot.get(self.base_url)
        
        # waiting for the username field to be present
        WebDriverWait(self.bot, 10).until(expected_conditions.presence_of_element_located((By.NAME, 'username')))
        
        # finding the username field and sending the username
        self.bot.find_element(By.NAME, 'username').send_keys(self.username)
        
        # finding the password field and sending the password
        self.bot.find_element(By.NAME, 'password').send_keys(self.password)
        
        # finding the login button and clicking it
        self.bot.find_element(By.XPATH, '//button[@type="submit"]').click()
        
        # waiting for the home page to load
        time.sleep(5)
    def send_message(self):
        # iterating through the list of users
        for user in self.user:
            # opening the user's profile
            self.bot.get(self.base_url + user)
            
            # waiting for the message button to be present
            WebDriverWait(self.bot, 10).until(expected_conditions.presence_of_element_located((By.XPATH, '//button[text()="Message"]')))
            
            # finding the message button and clicking it
            self.bot.find_element(By.XPATH, '//button[text()="Message"]').click()
            
            # waiting for the message input field to be present
            time.sleep(2)
            
            # finding the message input field and sending the message
            self.bot.find_element(By.XPATH, '//textarea').send_keys(self.message + Keys.ENTER)
            
            # waiting for a while before sending the next message
            time.sleep(2)
if __name__ == "__main__":
    # initializing the username, password, audience and message
    username = 'your_username'
    password = 'your_password'
    audience = ['user1', 'user2']  # List of usernames to send messages to
    message = 'Hello! This is an automated message.'
    
    # initializing the Chrome driver
    driver = webdriver.Chrome(ChromeDriverManager().install())
    
    # creating an instance of the bot class
    insta_bot = bot(username, password, audience, message)
    
    # closing the driver after sending messages
    driver.quit()
    print("Messages sent successfully!")
# Note: Make sure to replace 'your_username', 'your_password', and the audience list with actual values.
# Also, ensure that you have the necessary permissions to send messages to the users in the audience list.
# This script uses Selenium to automate the process of logging into Instagram and sending messages to a list of users.
# Ensure you have the required packages installed: `selenium`,      
# `webdriver_manager`, and a compatible version of ChromeDriver for your Chrome browser.
def login(self):

    self.bot.get(self.base_url)
    
    # ENTERING THE USERNAME FOR LOGIN INTO INSTAGRAM
    enter_username = WebDriverWait(self.bot, 20).until(
        expected_conditions.presence_of_element_located((By.NAME, 'username')))

    enter_username.send_keys(self.username)
    
    # ENTERING THE PASSWORD FOR LOGIN INTO INSTAGRAM
    enter_password = WebDriverWait(self.bot, 20).until(
        expected_conditions.presence_of_element_located((By.NAME, 'password')))
    enter_password.send_keys(self.password)

    # RETURNING THE PASSWORD and login into the account
    enter_password.send_keys(Keys.RETURN)
    time.sleep(5)
def send_message(self):
    # ITERATING THROUGH THE LIST OF USERS TO SEND MESSAGES
    for user in self.user:
        # OPENING THE USER'S PROFILE
        self.bot.get(self.base_url + user)
        
        # WAITING FOR THE MESSAGE BUTTON TO BE PRESENT
        message_button = WebDriverWait(self.bot, 20).until(
            expected_conditions.presence_of_element_located((By.XPATH, '//button[text()="Message"]')))
        
        # CLICKING THE MESSAGE BUTTON
        message_button.click()
        
        # WAITING FOR THE MESSAGE INPUT FIELD TO BE PRESENT
        time.sleep(2)
        
        # FINDING THE MESSAGE INPUT FIELD AND SENDING THE MESSAGE
        message_input = self.bot.find_element(By.XPATH, '//textarea')
        message_input.send_keys(self.message + Keys.ENTER)
        
        # WAITING FOR A WHILE BEFORE SENDING THE NEXT MESSAGE
        time.sleep(2)
if __name__ == "__main__":
    # INITIALIZING THE USERNAME, PASSWORD, AUDIENCE AND MESSAGE
    username = 'your_username'
    password = 'your_password'
    audience = ['user1', 'user2']  # List of usernames to send messages to
    message = 'Hello! This is an automated message.'
    
    # INITIALIZING THE CHROME DRIVER
    driver = webdriver.Chrome(ChromeDriverManager().install())
    
    # CREATING AN INSTANCE OF THE BOT CLASS
    insta_bot = bot(username, password, audience, message)
    
    # CLOSING THE DRIVER AFTER SENDING MESSAGES
    driver.quit()
    print("Messages sent successfully!")
# NOTE: Make sure to replace 'your_username', 'your_password', and the audience list
# with actual values. Also, ensure that you have the necessary permissions to send messages
# to the users in the audience list. This script uses Selenium to automate the process of logging
# into Instagram and sending messages to a list of users. Ensure you have the required packages installed:
# `selenium`, `webdriver_manager`, and a compatible version of ChromeDriver for your Chrome browser.
# This script uses Selenium to automate the process of logging into Instagram and sending messages to a
# list of users. Ensure you have the required packages installed: `selenium`, `webdriver_manager`, and a compatible version of ChromeDriver for your Chrome browser.
# first pop-up box
self.bot.find_element_by_xpath(
    '//*[@id="react-root"]/section/main/div/div/div/div/button').click()
time.sleep(3)

# 2nd pop-up box
self.bot.find_element_by_xpath(
    '/html/body/div[4]/div/div/div/div[3]/button[2]').click()

time.sleep(4)
# 3rd pop-up box
self.bot.find_element_by_xpath(
    '/html/body/div[4]/div/div/div/div[3]/button[2]').click()
# time.sleep(4)
# 4th pop-up box
self.bot.find_element_by_xpath(
    '/html/body/div[4]/div/div/div/div[3]/button[2]').
click()
# time.sleep(4)
# 5th pop-up box
self.bot.find_element_by_xpath(
    '/html/body/div[4]/div/div/div/div[3]/button[2]').click()
# time.sleep(4)
# 6th pop-up box
self.bot.find_element_by_xpath(
    '/html/body/div[4]/div/div/div/div[3]/button[2]').
click()
# time.sleep(4)
# 7th pop-up box
self.bot.find_element_by_xpath(
    '/html/body/div[4]/div/div/div/div[3]/button[2]').click()
# time.sleep(4)
# 8th pop-up box
self.bot.find_element_by_xpath(
    '/html/body/div[4]/div/div/div/div[3]/button[2]').click()
# time.sleep(4)
# 9th pop-up box
self.bot.find_element_by_xpath(