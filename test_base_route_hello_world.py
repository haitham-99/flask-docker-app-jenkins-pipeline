import pytest
import sys
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FireFoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions


@pytest.fixture()
def driver():
    firefox_driver_binary = "./drivers/geckodriver"
    ser_firefox = FirefoxService(firefox_driver_binary)
    firefox_options = FireFoxOptions()

    chrome_options = webdriver.ChromeOptions()

    edge_driver_binary = "msedgedriver.exe"
    edge_options = EdgeOptions()

    browser_name = 'firefox'
    # if isinstance(browserName,list):
    #     for browser_name in browserName:
    if browser_name == "firefox-webdriver":
        driver = webdriver.Firefox(service=ser_firefox)
    elif browser_name == "firefox":
        dc = {
            "browserName": "firefox",
            # "browserVersion": "101.0.1(x64)",
            "platformName": ""
        }
        driver = webdriver.Remote("http://localhost:4444", desired_capabilities=dc, options=firefox_options)
    elif browser_name == "chrome":
        dc = {
            "browserName": "chrome",
            "platformName": "Windows 11"
        }
        driver = webdriver.Remote("http://localhost:4444", desired_capabilities=dc, options=chrome_options)

    elif browser_name == "Edge":

        dc = {
            "browserName": "Microsoft Edge",
            "platformName": "Windows 11"
        }
        driver = webdriver.Remote("http://localhost:4444", desired_capabilities=dc, options=edge_options)

    elif browser_name == "firefox-mobile":
        firefox_options = FireFoxOptions()
        firefox_options.add_argument("--width=375")
        firefox_options.add_argument("--height=812")
        firefox_options.set_preference("general.useragent.override", "userAgent=Mozilla/5.0 "
                                                                     "(iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like "
                                                                     "Gecko) CriOS/101.0.4951.44 Mobile/15E148 Safari/604.1")
        # firefox_options.set_preference("general.useragent.override", "Nexus 7")

        driver = webdriver.Firefox(service=ser_firefox, options=firefox_options)

    elif browser_name == "android-emulator":
        dc = {
            "platformName": "Android",
            "platformVersion": "8.1.0",
            "deviceName": "Android Emulator",
            # "platformVersion": "11.0.0",
            # "deviceName": "1aaa4ea80404",
            "automationName": "Appium",
            # "app": "com.android.chrome",
            "browserName": "Chrome"
        }
        driver = webdriver.Remote("http://localhost:4723/wd/hub", dc)

    elif browser_name == "android-phone":
        dc = {
            "platformName": "Android",
            "platformVersion": "11.0.0",
            "deviceName": "1aaa4ea80404",
            "automationName": "Appium",
            "browserName": "Chrome"
        }

        driver = webdriver.Remote("http://localhost:4723/wd/hub", dc)
    else:
        raise Exception("driver doesn't exists")
    yield driver
    driver.close()


def test_if_text_displayed(driver):
    driver.get("http://localhost:5000")
    my_text = driver.find_element(By.CSS_SELECTOR, "body").text
    assert "Welcome to the Application with updated code!" == my_text


def test_response(driver):
    response = requests.get("http://localhost:5000")
    status = response.status_code

    assert status == 200


def test_response(driver):
    response = requests.get("http://localhost:5000/stub")
    status = response.status_code

    assert status == 200


def test_if_text_displayed_sub(driver):
    driver.get("http://localhost:5000/stub")
    my_text = driver.find_element(By.CSS_SELECTOR, "body").text
    assert "Value of Stub: 200" == my_text
