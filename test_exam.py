import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import HtmlTestRunner


class OrderTest(unittest.TestCase):
    USERNAME = (By.NAME, "email")
    PASSWORD = (By.NAME, "password")
    LOGIN_BUTTON = (By.ID, "my_account")
    SUPPORT_BUTTON = (By.CLASS_NAME, "navbar-aux-help-link")
    SHOPPING_CART_BUTTON = (By.ID, "my_cart")
    SEARCH_FORM = (By.ID,"searchboxTrigger")
    SEARCH_BUTTON = (By.CLASS_NAME,"searchbox-submit-button")
    SEARCH_KEYWORD = "iphone 14"
    SORT_DROPDOWN_BUTTON = (By.CSS_SELECTOR, ".sort-control-btn-dropdown .sort-control-btn")
    SORT_BY_DESCENDING_PRICE_OPTION = (By.XPATH, "//a[contains(text(), 'Pret descrescator')]")

    SORT_BY_DESCENDING_DISCOUNT_OPTION = (By.XPATH, "//a[contains(text(), 'Discount %')]")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, ".btn.btn-sm.btn-primary.btn-emag.btn-block.yeahIWantThisProduct:first-of-type")

    CART_ITEM = (By.CSS_SELECTOR, ".cart-widget.cart-line")
    GO_TO_CART_BUTTON = (By.XPATH, "//a[contains(text(), 'Vezi detalii cos')]")

    def setUp(self) -> None:
        chrome_options = webdriver.ChromeOptions()
        self.chrome = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.chrome.get('https://www.emag.ro/')
        self.chrome.maximize_window()
        self.chrome.implicitly_wait(2)
        self.soup = BeautifulSoup(self.chrome.page_source, 'html.parser')

    def tearDown(self) -> None:
        self.chrome.quit()

    def test_url(self):
        current_url = self.chrome.current_url
        expected_url = "https://www.emag.ro/"
        self.assertEqual(expected_url, current_url, f"ERROR.expected: {expected_url}, actual: {current_url}")

    def test_on_site_button(self):
        on_site_button = WebDriverWait(self.chrome, 5).until(EC.visibility_of_element_located(self.SUPPORT_BUTTON))
        self.assertTrue(on_site_button.is_displayed(), 'ERROR.Support button is not displayed')

    def test_login_button(self):
        logout_button = WebDriverWait(self.chrome, 5).until(EC.visibility_of_element_located(self.LOGIN_BUTTON))
        self.assertTrue(logout_button.is_displayed(), 'ERROR.Logout button is not displayed')

    def test_shopping_cart_button(self):
        shopping_cart_button = WebDriverWait(self.chrome, 5).until(EC.visibility_of_element_located(self.SHOPPING_CART_BUTTON))
        self.assertTrue(shopping_cart_button.is_displayed(), 'ERROR.Shopping cart button is not displayed')

    # test if search form exist
    def test_search_form(self):
        wait = WebDriverWait(self.chrome, 10)
        search_form = wait.until(EC.presence_of_element_located((self.SEARCH_FORM)))
        self.assertTrue(search_form.is_displayed(), 'ERROR.Search form is not displayed')

    # find the search button after is located, send the search keyword to the search box and submit the form
    def test_search_button(self):
        search_input = WebDriverWait(self.chrome, 3).until(EC.visibility_of_element_located((self.SEARCH_BUTTON)))
        self.assertTrue(search_input.is_displayed(), 'ERROR.Search button is not displayed')

    # wait for the sort dropdown button to be present and the find it, click the sort dropdown button to make the list of options visible and click the sort option
    def test_search_functionality_and_sort(self):
        wait = WebDriverWait(self.chrome, 40)
        search_input = wait.until(EC.visibility_of_element_located((self.SEARCH_FORM)))
        search_input.send_keys(self.SEARCH_KEYWORD)
        search_input.submit()
        sort_dropdown_button = wait.until(EC.element_to_be_clickable((self.SORT_DROPDOWN_BUTTON)))
        sort_dropdown_button.click()
        sort_option = wait.until(EC.presence_of_element_located((self.SORT_BY_DESCENDING_PRICE_OPTION)))
        sort_option.click()
        self.assertTrue(sort_option.is_displayed(), 'ERROR.Sort option is not displayed')

    # search for item, order by price, add the first to cart
    def test_search_discount_and_add_to_cart(self):
        wait = WebDriverWait(self.chrome, 30)
        search_input = wait.until(EC.visibility_of_element_located((self.SEARCH_FORM)))
        search_input.send_keys(self.SEARCH_KEYWORD)
        search_input.submit()
        sort_dropdown_button = wait.until(EC.element_to_be_clickable((self.SORT_DROPDOWN_BUTTON)))
        sort_dropdown_button.click()
        sort_option = wait.until(EC.presence_of_element_located((self.SORT_BY_DESCENDING_DISCOUNT_OPTION)))
        sort_option.click()
        time.sleep(5)
        add_to_cart_button = wait.until(EC.element_to_be_clickable((self.ADD_TO_CART_BUTTON)))
        add_to_cart_button.click()
        self.assertTrue(add_to_cart_button.is_displayed(), 'ERROR.Add to cart button is not displayed')

    # search for item, order by discount, add the first to cart, check the cart
    def test_item_added_to_cart(self):
        wait = WebDriverWait(self.chrome, 30)
        search_input = wait.until(EC.visibility_of_element_located((self.SEARCH_FORM)))
        search_input.send_keys(self.SEARCH_KEYWORD)
        search_input.submit()
        sort_dropdown_button = wait.until(EC.element_to_be_clickable((self.SORT_DROPDOWN_BUTTON)))
        sort_dropdown_button.click()
        sort_option = wait.until(EC.presence_of_element_located((self.SORT_BY_DESCENDING_DISCOUNT_OPTION)))
        sort_option.click()
        time.sleep(5)
        add_to_cart_button = wait.until(EC.element_to_be_clickable((self.ADD_TO_CART_BUTTON)))
        add_to_cart_button.click()
        go_to_cart_button = WebDriverWait(self.chrome, 10).until(EC.visibility_of_element_located(self.GO_TO_CART_BUTTON))
        go_to_cart_button.click()
        time.sleep(10)
        cart_item = WebDriverWait(self.chrome, 10).until(EC.visibility_of_element_located(self.CART_ITEM))
        self.assertTrue(cart_item.is_displayed(), 'ERROR.Cart item is not displayed')

    # search by a product, sort it by the Discount and add it to cart, then delete it and check the cart
    def test_item_added_to_cart_then_delete(self):
        wait = WebDriverWait(self.chrome, 30)
        search_input = wait.until(EC.presence_of_element_located((self.SEARCH_FORM)))
        search_input.send_keys(self.SEARCH_KEYWORD)
        search_input.submit()
        sort_dropdown_button = wait.until(EC.element_to_be_clickable((self.SORT_DROPDOWN_BUTTON)))
        sort_dropdown_button.click()
        sort_option = wait.until(EC.presence_of_element_located((self.SORT_BY_DESCENDING_DISCOUNT_OPTION)))
        sort_option.click()
        time.sleep(5)
        add_to_cart_button = wait.until(EC.element_to_be_clickable((self.ADD_TO_CART_BUTTON)))
        add_to_cart_button.click()
        go_to_cart_button = WebDriverWait(self.chrome, 10).until(EC.visibility_of_element_located(self.GO_TO_CART_BUTTON))
        go_to_cart_button.click()
        time.sleep(10)
        cart_items = WebDriverWait(self.chrome, 10).until(EC.presence_of_all_elements_located(self.CART_ITEM))
        self.assertGreater(len(cart_items), 0, "No items found in the cart")


