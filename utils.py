from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import json


def save_json_to_file(filename, data):
    # Open the file in append mode
    with open(filename, "a") as file:
        # Write the JSON data to the file
        json.dump(data, file, ensure_ascii=False)
        # Add a newline character to separate entries
        file.write('\n')


def retrieve_data_from_quote(quote):
    # Retrieve the text, author, and tags from the quote element
    quote_text = quote.find_element_by_class_name('text').text
    quote_author = quote.find_element_by_class_name('author').text
    quote_tags = quote.find_element_by_class_name('tags').text

    # Extract the tags by removing the "Tags: " prefix and splitting the string
    tags_list = quote_tags.replace('Tags: ', '').split(' ')

    # Create a dictionary to store the quote data
    data = {
        'text': quote_text,
        'author': quote_author,
        'tags': tags_list
    }
    return data


def get_all_quotes_from_link(driver, wait, output_file):
    # Wait for the quote elements to be clickable
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'quote')))

    # Retrieve all the quote elements on the page
    page_quotes = driver.find_elements_by_class_name('quote')

    # Process each quote on the page
    for quote in page_quotes:
        # Retrieve the data from the quote element
        single_quote_in_json = retrieve_data_from_quote(quote)

        # Save the quote data to the output file
        save_json_to_file(output_file, single_quote_in_json)

    # Find the next page button if it exists
    try:
        next_page_button = driver.find_element_by_class_name('next').find_element_by_tag_name('a')
    except NoSuchElementException:
        next_page_button = None

    # Return the next page button element (or None if not found)
    return next_page_button
