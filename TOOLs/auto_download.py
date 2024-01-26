import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

def send_url(target_url, payload_url):
    """
    Sends a URL to a specified target website.

    Args:
    target_url (str): The URL of the target website to which the URL is sent.
    payload_url (str): The URL that needs to be sent to the target website.

    Returns:
    response: The response from the target website.
    """
    # Prepare the payload. This might vary depending on the target website's requirements.
    payload = {'url': payload_url}

    # Make a POST request to the target website
    try:
        response = requests.post(target_url, data=payload)
        return response
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

def get_page_content(url):
    """
    Fetches the content of the specified URL.

    Args:
    url (str): The URL of the web page to fetch.

    Returns:
    str: The content of the web page or an error message.
    """
    try:
        response = requests.get(url)
        # Check if the request was successful
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        return f"An error occurred: {e}"



def fill_input_field(url, input_name, value_to_fill):
    """
    Navigates to a URL and fills out an input field.

    Args:
    url (str): The URL to navigate to.
    input_name (str): The name or ID of the input field to fill.
    value_to_fill (str): The value to enter into the input field.
    """
    # Create a new instance of the browser driver
    driver = webdriver.Chrome()  # Replace with webdriver.Firefox() if using Firefox

    try:
        # Navigate to the URL
        driver.get(url)

        # Find the input field by its name or ID and fill it out
        input_element = driver.find_element_by_name(input_name)  # or use find_element_by_id
        input_element.send_keys(value_to_fill)

        # Add any other interactions here (e.g., clicking a submit button)

    finally:
        # Close the browser window
        driver.quit()

def test_with_google():
    driver = webdriver.Chrome()
    url ='https://www.google.com.tw'
    driver.get(url)
    time.sleep(2)
    driver.close()

def google_search(query):
    # URL encoding the query
    query = query.replace(' ', '+')
    
    # Google Search URL
    URL = f"https://google.com/search?q={query}"
    
    # Performing the GET request
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(URL, headers=headers)

    # Parsing the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extracting search results
    search_results = []
    for g in soup.find_all('div', class_='tF2Cxc'):
        title = g.find('h3').text
        link = g.find('a')['href']
        item = {'title': title, 'link': link}
        search_results.append(item)
    
    return search_results



if __name__ == "__main__":
    target_url = "https://www.bigconv.com/v215"
    payload_url = "https://www.youtube.com/watch?v=iAYXm1V3FB4&list=RDajJanul_K4k&index=5"

    # response = send_url(target_url, payload_url)
    # response = get_page_content(target_url)
    # print(response)
    # fill_input_field(target_url, "Search MP3 Here ...", "hehe")

    # test_with_google()
    # Example usage
    results = google_search("Python programming")
    for result in results:
        print(result['title'], result['link'])
