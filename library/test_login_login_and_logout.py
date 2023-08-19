import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Replace 'YOUR_EDGEDRIVER_PATH' with the actual path to your Edge WebDriver executable
driver = webdriver.Edge(executable_path='msedgedriver.exe')

# Replace 'YOUR_WEBSITE_URL' with the URL of your website's homepage
url = 'http://127.0.0.1:8000/'


def test_login_with_valid_credentials():
    driver.get(url)
    time.sleep(5)  # Wait for the page to load

    # Click on the "Login" button
    login_button = driver.find_element(By.LINK_TEXT, 'Login')
    login_button.click()
    time.sleep(5)

    # Enter valid login credentials
    username_input = driver.find_element(By.NAME, 'email')
    password_input = driver.find_element(By.NAME, 'password')
    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    time.sleep(5)

    username_input.send_keys('hort19345@gmail.com')
    password_input.send_keys('qwerty12345')
    submit_button.click()
    time.sleep(5)

    # Verify successful login
    assert "Hello" in driver.page_source
    assert "Logout" in driver.page_source

    # Click on the "Logout" link
    logout_link = driver.find_element(By.PARTIAL_LINK_TEXT, 'Logout')
    logout_link.click()
    time.sleep(5)

    # Verify successful logout
    assert "Login" in driver.page_source


def test_login_with_invalid_credentials():
    driver.get(url)
    time.sleep(10)  # Wait for the page to load

    # Click on the "Login" button
    login_button = driver.find_element(By.LINK_TEXT, 'Login')
    login_button.click()
    time.sleep(5)

    # Enter invalid login credentials
    username_input = driver.find_element(By.NAME, 'email')
    password_input = driver.find_element(By.NAME, 'password')
    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    time.sleep(5)

    username_input.send_keys('invalid_username')
    password_input.send_keys('invalid_password')
    submit_button.click()
    time.sleep(5)
    # Verify login failure and error message
    assert "Login" in driver.page_source
    driver.quit()


if __name__ == '__main__':
    test_login_with_valid_credentials()
    test_login_with_invalid_credentials()
