from playwright.sync_api import Page

class CartPage:
    
    def __init__(self, page: Page):
        self.page = page
    
    def click_on_checkout_button(self):
        self.page.click("#checkout")