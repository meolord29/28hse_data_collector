import requests
from concurrent.futures import ThreadPoolExecutor
import concurrent
from bs4 import BeautifulSoup


def post_request(page_number):
    url = "https://www.28hse.com/en/property/dosearch"
    form_data = {
        "page": page_number,
        "searchText": "",
        "myfav": "",
        "myvisited": "",
        "item_ids": "",
        "sortBy": "",
        "is_grid_mode": "",
        "search_words_thing": "default",
        "buyRent": "rent",
        "mobilePageChannel": "residential",
        "cat_ids": "",
        "search_words_value": "",
        "is_return_newmenu": "0",
        "plan_id": "",
        "propertyDoSearchVersion": "2.0",
        "sortBy": "default",
        "locations": "",
        "locations_by_text": "0",
        "mainType": "5",
        "mainType_by_text": "0",
        "otherRentalShortCut": "",
        "otherRentalShortCut_by_text": "0",
        "price": "",
        "price_by_text": "0",
        "areaOption": "",
        "areaOption_by_text": "0",
        "areaRange": "",
        "areaRange_by_text": "0",
        "roomRange": "",
        "roomRange_by_text": "0",
        "searchTags": "",
        "searchTags_by_text": "0",
        "others": "",
        "others_by_text": "0",
        "direction": "",
        "direction_by_text": "0",
        "landlordAgency": "",
        "landlordAgency_by_text": "0",
        "yearRange": "",
        "yearRange_by_text": "0",
        "floors": "",
        "floors_by_text": "0",
        "more_options": "",
        "more_options_by_text": "0"
    }

    response = requests.post(url, data=form_data)
    return response.status_code, response.text

def main():

    url = "https://www.28hse.com/en/rent"
    response = requests.get(url)
    if response.status_code == 200:
        page_content = response.text
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        exit()

    # Step 2: Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(page_content, 'lxml')

    # Step 3: Locate the element using the converted XPath
    # XPath: /html/body/div[1]/div/div/div[1]/div[4]/div[1]/div[5]/div/a[10]
    # Converting XPath to BeautifulSoup's select method
    element = soup.select_one('html > body > div:nth-of-type(1) > div > div > div:nth-of-type(1) > div:nth-of-type(4) > div:nth-of-type(1) > div:nth-of-type(5) > div > a:nth-of-type(10)')

    # Step 4: Retrieve the text value of the located element
    if element:
        text_value = element.get_text(strip=True)
        print(f"Text value located at the specified XPath: {text_value}")
    else:
        print("Element not found at the specified XPath.")






    with ThreadPoolExecutor(max_workers=12) as executor:
        # Create a list of futures
        futures = [executor.submit(post_request, page) for page in range(1, 1372)]

        # Iterate over the futures as they complete
        for future in concurrent.futures.as_completed(futures):
            try:
                status_code, response_text = future.result()
                print(f"Page processed with status code: {status_code}")
            except Exception as exc:
                print(f"Generated an exception: {exc}")

if __name__ == "__main__":
    main()