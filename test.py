import warnings

warnings.filterwarnings("ignore")

import sys
import time
import json

from tqdm import tqdm

from seleniumwire import webdriver
from seleniumwire.utils import decode


BASE_URL = "https://food.grab.com/ph/en/"
BINARY_LOCATION = "./chromedriver"
SSR_PROPS_TAG_ID = "__NEXT_DATA__"
SEED_LOCATION = "Marawi City Police Station - West, Matina Crossing, Davao City, Davao del Sur, Davao City, Davao Region (Region XI), 8000, Philippines"


# Holder of all restro data
papa_json = []
progress_bar = tqdm()

# EZ bypass to circumvent clicking inputs and buttons
# # driver.add_cookie({'name' : 'location', 'value' : '{"id":"IT.0JTF5M1GR9W2Y","latitude":7.065093,"longitude":125.592139,"address":"Marawi City Police Station - West, Matina Crossing, Davao City, Davao del Sur, Davao City, Davao Region (Region XI), 8000, Philippines","countryCode":"PH","isAccurate":true,"addressDetail":"","noteToDriver":"","city":"Davao City","cityID":8}', 'domain' : "https://food.grab.com/ph/en/restaurants" })
# driver.get("https://food.grab.com/ph/en/restaurants")


def input_search_location_and_proceed(driver: webdriver.Chrome):
    """
    Input search query and click on a list option
    """
    clicked = False
    driver.find_element_by_id("location-input").send_keys(
        "Manila City Hall - 369 Antonio Villegas St., Ermita, Manila, Metro Manila, NCR, 1000, Philippines"
    )
    time.sleep(2)
    for op in driver.find_elements_by_tag_name("ul"):
        if op.text.startswith("Manila"):
            op.click()
            clicked = True
            break

    search_button = driver.find_element_by_class_name("ant-btn")
    if search_button.text != "Search":
        clicked = False

    if not clicked:
        raise Exception("Couldn't Proceed with Searching")

    search_button.click()


def scroll_to_end(driver: webdriver.Chrome) -> None:
    """
    Scroll to the end of page
    """
    progress_bar.set_description("Scrolling to the load more button")
    total_height = int(driver.execute_script("return document.body.scrollHeight"))

    for i in range(1, total_height, 5):
        driver.execute_script("window.scrollTo(0, {});".format(i))


def filter_restro_result(
    result: dict,
    required_keys: list = ["id", "listing_type", "name", "latitude", "longitude"],
) -> dict:
    """
    Filter and Save specific keys from result dict
    """
    result = {key: value for key, value in result.items() if key in required_keys}
    return result


# TODO: Convert exceptions into something good
def get_ssr_props(driver: webdriver.Chrome) -> list:
    """
    Grabs the Server Side Rending props for listings currently in the viewport
    """
    progress_bar.set_description("Grabbing Restro data")
    script_element = driver.find_element_by_id(SSR_PROPS_TAG_ID)
    if not script_element:
        raise Exception("SSR Element Not Found")
    script_inner_html = script_element.get_attribute("innerHTML")
    if not script_inner_html:
        raise Exception("Listing Data Not Found")
    script_inner_html_parsed = json.loads(script_inner_html)

    _popular_restros = script_inner_html_parsed["props"]["initialReduxState"][
        "pageRestaurantsV2"
    ]["entities"].get("recommendedMerchants", {})
    _avail_restros = script_inner_html_parsed["props"]["initialReduxState"][
        "pageRestaurantsV2"
    ]["entities"].get("restaurantList", {})

    for _, item in _popular_restros.items():
        # item["listing_type"] = "recommendedMerchants"
        papa_json.append(filter_restro_result(item))

    for _, item in _avail_restros.items():
        # item["listing_type"] = "restaurantList"
        papa_json.append(filter_restro_result(item))


def load_more_button_present(driver: webdriver.Chrome) -> bool:
    """
    Check if load more button is present and scroll+click it if present
    """
    try:
        temp_button = driver.find_element_by_class_name("ant-btn-block")
    except Exception as e:
        raise Exception("Failed to find 'Load More' Button, possibly timed out.")
    # cross check if correct button
    if not temp_button.text == "Load More":
        return False

    # scrolling to load more button
    desired_y = (temp_button.size["height"] / 2) + temp_button.location["y"]
    window_h = driver.execute_script("return window.innerHeight")
    window_y = driver.execute_script("return window.pageYOffset")
    current_y = (window_h / 2) + window_y
    scroll_y_by = desired_y - current_y

    driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)
    temp_button.click()

    return True


def synthetic_wait():
    """
    Wait before fetching for more search data
    """
    per_page_wait = 5
    for total_tick in range(per_page_wait + 1):
        time_tick = 1
        progress_bar.set_description(f"Sleeping for {per_page_wait-total_tick} seconds")
        time.sleep(time_tick)


def intercept_search_results(driver: webdriver.Chrome):
    """
    Grab response data from /search api calls
    """
    for request in driver.requests:
        if (
            request.response
            and "https://portal.grab.com/foodweb/v2/search" == request.url
        ):
            response_body = json.loads(
                decode(
                    request.response.body,
                    request.response.headers.get("Content-Encoding", "identity"),
                )
            )

            things = [
                filter_restro_result(
                    res,
                    required_keys=["id", "address", "latlng"],
                )
                for res in response_body["searchResult"]["searchMerchants"]
            ]
            papa_json.extend(things)


try:
    driver = webdriver.Chrome(BINARY_LOCATION)
    driver.get(BASE_URL)
    input_search_location_and_proceed(driver)
    scroll_to_end(driver)
    get_ssr_props(driver)
    while True:
        progress_bar.update(1)
        synthetic_wait()

        scroll_to_end(driver)
        intercept_search_results(driver)
        with open("current_buffer.json", "w") as json_buffer:
            json.dump(papa_json, json_buffer)
            progress_bar.set_description(
                f"Current we have # of {len(papa_json)} restro listings"
            )
        if not load_more_button_present(driver):
            raise Exception("Load More ButtonNotFound")

except Exception as e:
    # check if cloudfront rate limiting
    if "403 ERROR" in driver.page_source:
        print("Cloudfront Ratelimited. Exiting now...")
        sys.exit(0)
    print(
        "Failed while scrapping elements due to element not being present. Exiting since Page failed to load."
    )
