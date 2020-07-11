import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException


@pytest.fixture(scope='module')
def driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = True
    try:
        browser = webdriver.Chrome(options=chrome_options)
    except WebDriverException as e:
        pytest.skip(str(e))
    else:
        yield browser
        browser.quit()
