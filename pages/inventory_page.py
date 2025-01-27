from playwright.sync_api import Page

class InventoryPage:
    
    def __init__(self, page: Page):
        self.page = page
        
    def click_on_menu_button(self):
        self.page.click("#react-burger-menu-btn")
        
    def click_on_logout_button(self):
        self.page.click("#logout_sidebar_link")
        
    def click_on_cart_button(self):
        self.page.click("#shopping_cart_container")

    def check_cart_badge_value(self):
        try:
            cart_badge = self.page.locator(".shopping_cart_badge")
            badge_value = cart_badge.text_content() if cart_badge.count() > 0 else "0"
            return int(badge_value)
        except Exception as e:
            print(f"Error while fetching cart badge value: {e}")
            return 0
        
    def add_item_and_check_cart(self, item_selector: str):
        self.page.click(item_selector)
        badge_value = self.check_cart_badge_value()
        cart_items = self.page.query_selector_all(".cart_item .inventory_item_name")
        if badge_value == 0 and len(cart_items) > 0:
            raise AssertionError(f"Cart badge value is 0, but there are {len(cart_items)} items in the cart!")
        return badge_value
    
    def remove_item_and_check_cart_decrease(self, remove_button_locator):
        cart_items = self.page.locator(".cart_item")
        self.page.wait_for_selector(".cart_item")  
        remove_button = self.page.locator(remove_button_locator)
        remove_button.wait_for(state="visible")
        initial_badge_value = self.check_cart_badge_value()
        remove_button.click()
        self.page.wait_for_selector(remove_button_locator, state="detached")
        new_badge_value = self.check_cart_badge_value()
        if new_badge_value >= initial_badge_value:
            raise AssertionError(f"Cart badge value did not decrease. Initial: {initial_badge_value}, New: {new_badge_value}")
        
        return new_badge_value
        
    def verify_items_in_cart(self, expected_items: list):
        self.page.click("#shopping_cart_container")
        self.page.wait_for_selector(".cart_item")
        cart_items = self.page.query_selector_all(".cart_item .inventory_item_name")
        cart_item_names = [item.inner_text() for item in cart_items]
        missing_items = [item for item in expected_items if item not in cart_item_names]
        
        if missing_items:
            raise AssertionError(f"Missing items in the cart: {', '.join(missing_items)}")
        else:
            print("All items are present in the cart.")
        
    def sort_products(self, sort_option: str):
        sort_dropdown = self.page.locator('.product_sort_container')
        sort_dropdown.wait_for(state="visible")
        sort_dropdown.select_option(value=sort_option)
        self.page.wait_for_selector('.inventory_item')
    
    def get_product_prices(self):
        product_prices = self.page.locator('.inventory_item .price')
        prices = product_prices.all_text_contents()
        return [float(price.replace('$', '').strip()) for price in prices]

    def verify_sorted(self, prices, ascending=True):
        if ascending:
            return prices == sorted(prices)
        else:
            return prices == sorted(prices, reverse=True)