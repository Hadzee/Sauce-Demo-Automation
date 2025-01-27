from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from user_data import USERNAME, PASSWORD, LOCKED_OUT_USER

def test_error_handling():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        login_page = LoginPage(page)
        login_page.goto()
        
        login_page.fill_username(LOCKED_OUT_USER)
        login_page.fill_password(PASSWORD)
        login_page.click_on_login_button()
        assert page.inner_text('h3') == "Epic sadface: Sorry, this user has been locked out.", "Successfully logged in with a locked out user."
        login_page.fill_username(LOCKED_OUT_USER)
        login_page.fill_password("secret_saucedasdas")
        login_page.click_on_login_button()
        assert page.inner_text('h3') == "Epic sadface: Username and password do not match any user in this service", "Successfully logged in with a locked out user and an incorrect password."
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
        checkout_page.click_on_continue_button()
        assert page.inner_text('h3') == "Error: First Name is required", "Successfully moved to checkout page without any info."
        checkout_page.fill_firstname("Tarik")
        checkout_page.click_on_continue_button()
        assert page.inner_text('h3') == "Error: Last Name is required", "Successfully moved to checkout page without the last name and a zip code."
        checkout_page.fill_lastname("Hadzikic")
        checkout_page.click_on_continue_button()
        assert page.inner_text('h3') == "Error: Postal Code is required", "Successfully moved to checkout page without a zip code."
        
        inventory_page.click_on_menu_button()
        inventory_page.click_on_logout_button()
        assert page.inner_text('h4') == "Accepted usernames are:", "Did not log out properly."
        
        browser.close()