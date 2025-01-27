import random
import string

from playwright.sync_api import Page

class LoginPage:
    
    def __init__(self, page: Page):
        self.page = page
        
    def goto(self):
       self.page.goto("https://www.saucedemo.com/")
       
    def fill_username(self, username: str):
        self.page.fill("#user-name", username)
    
    def fill_password(self, password: str):
        self.page.fill("#password", password)            
        
    def click_on_login_button(self):
        self.page.click("#login-button")    
        
    def generate_random_username(self, length=8):
        characters = string.ascii_letters + string.digits + "_"
        username = random.choice(string.ascii_letters)
        username += ''.join(random.choice(characters) for _ in range(length - 1))
        
        return username