from playwright.sync_api import Page

class CheckoutPage:
    
    def __init__(self, page: Page):
        self.page = page
        
    def click_on_continue_button(self):
        self.page.click("#continue")
        
    def click_on_finish_button(self):
        self.page.click("#finish")
        
    def click_on_back_home_button(self):
        self.page.click("#back-to-products")

    def fill_firstname(self, username: str):
        self.page.fill("#first-name", username)
        
    def fill_lastname(self, username: str):
        self.page.fill("#last-name", username)
        
    def fill_zipcode(self, zipcode: str):
        # Only allow numeric characters (no letters, symbols, or spaces)
        if zipcode.isdigit():
            self.page.fill("#postal-code", zipcode)
        else:
            raise ValueError("Zipcode must contain only numeric characters.")
        
    def verify_items_on_checkout(self, expected_items: list):
        self.page.wait_for_selector(".cart_item")
        cart_items = self.page.query_selector_all(".cart_item .inventory_item_name") # Get the names of the items in the cart
        cart_item_names = [item.inner_text() for item in cart_items]
        missing_items = [item for item in expected_items if item not in cart_item_names] # Verify if all expected items are present in the cart
        
        if missing_items:
            raise AssertionError(f"Missing items in the cart: {', '.join(missing_items)}")
        else:
            print("All items are present in the cart.")
            
    def verify_cart_total(self):
        item_prices = self.page.locator('.inventory_item_price')
        # Wait for the prices to be visible (ensure they are loaded)
        item_prices.first.wait_for(state='visible')  # Ensure at least the first price is visible (to avoid waiting on all)
        # Retrieve the text contents of all item prices
        prices = item_prices.all_text_contents()
        if not prices:
            raise AssertionError("No prices found on the page.")
        # Clean the prices and convert them to float
        item_total = sum([float(price.replace('$', '').strip()) for price in prices])
        # Get the displayed subtotal (item total) from the page
        displayed_total = self.page.locator('.summary_subtotal_label').text_content()
        if not displayed_total:
            raise AssertionError("Displayed total is missing on the page.")
        # Clean the displayed total and convert it to float
        displayed_total_value = float(displayed_total.replace('Item total: $', '').strip())
        # Compare the calculated item total with the displayed total
        if abs(item_total - displayed_total_value) > 0.01:
            raise AssertionError(f"Total price mismatch: Calculated total is {item_total}, but displayed total is {displayed_total_value}.")
        else:
            print(f"Total price is correct: ${item_total}")