from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from user_data import USERNAME, PASSWORD, EXPECTED_ITEMS

def test_checkout():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        login_page = LoginPage(page)
        login_page.goto()
        
        login_page.fill_username(USERNAME)
        login_page.fill_password(PASSWORD)
        login_page.click_on_login_button()
        
        inventory_page = InventoryPage(page)
        inventory_page.add_item_and_check_cart("#add-to-cart-sauce-labs-backpack")
        inventory_page.add_item_and_check_cart("#add-to-cart-sauce-labs-bike-light")
        inventory_page.add_item_and_check_cart("#add-to-cart-sauce-labs-bolt-t-shirt")
        inventory_page.click_on_cart_button()
        
        cart_page = CartPage(page)
        cart_page.click_on_checkout_button()
        
        checkout_page = CheckoutPage(page)
        checkout_page.fill_firstname("Tarik")
        checkout_page.fill_lastname("Hadzikic")
        checkout_page.fill_zipcode("75270")
        checkout_page.click_on_continue_button()
        
        checkout_page.verify_items_on_checkout(EXPECTED_ITEMS)
        checkout_page.verify_cart_total()
        checkout_page.click_on_finish_button()
        assert page.inner_text('h2') == "Thank you for your order!"
        checkout_page.click_on_back_home_button()
        
        inventory_page.click_on_menu_button()
        inventory_page.click_on_logout_button()
        assert page.inner_text('h4') == "Accepted usernames are:", "Did not log out properly."
        
        browser.close()