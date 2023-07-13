from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from dotenv import dotenv_values
import utils


def main():
    # Load environment variables from .env file
    env_vars = dotenv_values('.env')

    # Extract required variables from environment variables
    init_link, output_file, proxy = env_vars['INPUT_URL'], env_vars['OUTPUT_FILE'], env_vars['PROXY']
    
    # Erase previous data from destination file
    with open(output_file, 'w') as file:
        pass

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--no-sandbox")

    # Set up proxy capabilities for Chrome driver
    capabilities = webdriver.DesiredCapabilities.CHROME.copy()
    capabilities['proxy'] = {
        'httpProxy': proxy,
        'ftpProxy': proxy,
        'sslProxy': proxy,
        'noProxy': None,
        'proxyType': 'MANUAL',
        'class': 'org.openqa.selenium.Proxy',
        'autodetect': False
    }

    # Launch Chrome driver within a context manager
    with webdriver.Chrome('chromedriver/chromedriver', options=chrome_options,
                          desired_capabilities=capabilities) as driver:
        wait = WebDriverWait(driver, 30)

        # Load the initial link
        driver.get(init_link)

        # Get quotes from the initial page and retrieve the next page button
        next_page_button = utils.get_all_quotes_from_link(driver, wait, output_file)

        # Continue to click the next page button until it is no longer available
        while next_page_button:
            next_page_button.click()
            next_page_button = utils.get_all_quotes_from_link(driver, wait, output_file)


if __name__ == "__main__":
    main()
