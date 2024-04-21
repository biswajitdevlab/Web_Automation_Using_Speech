import speech_recognition as sr
from selenium import webdriver
from selenium.common import NoSuchElementException, ElementClickInterceptedException, TimeoutException, \
    NoAlertPresentException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

default_url = "https://www.google.com"

def initialize_driver():
    # Set up Selenium WebDriver (update the path to your chromedriver executable)
    driver = webdriver.Firefox()
    return driver

def speech_to_text():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something:")

        try:
            # Adjust timeout and phrase duration to suit your needs
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            command = recognizer.recognize_google(audio).lower()
            print("You said:", command)
            return command

        except sr.WaitTimeoutError:
            print("Timeout waiting for speech input.")
            return None
        except sr.UnknownValueError:
            print("Unable to recognize speech.")
            return None
        except sr.RequestError as e:
            print("Error accessing the speech recognition service:", e)
            return None
        except Exception as e:
            print("An unexpected error occurred:", e)
            return None

def find_element_by_locator(driver, locator_type, locator_value):
    try:
        if locator_type == "ID":
            return driver.find_element(By.ID, locator_value)
        elif locator_type == "NAME":
            return driver.find_element(By.NAME, locator_value)
        elif locator_type == "CSS_SELECTOR":
            return driver.find_element(By.CSS_SELECTOR, locator_value)
        elif locator_type == "XPATH":
            return driver.find_element(By.XPATH, locator_value)
        else:
            raise ValueError("Invalid locator type.")
    except Exception as e:
        print(f"Error finding element by locator: {e}")
        return None

def execute_command(driver, command):
    try:
        if "open" in command:
            parts = command.split("open")
            if len(parts) > 1:
                url = parts[1].strip()
                try:
                    driver.get(url)
                    print(f"Opened {url}")
                except Exception as e:
                    print(f"Error opening {url}: {e}")
            else:
                print("Invalid 'open' command. Please provide a URL.")


        elif "click" in command:
            element_name = command.split("click")[1].strip().lower()
            try:
                # Use a case-insensitive XPath expression
                xpath = f"//*[translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz') = '{element_name}']"
                element = driver.find_element(By.XPATH, xpath)
                element.click()
                print(f"Clicked on {element_name}")
            except Exception as e:
                print(f"Error clicking on {element_name}: {e}")

        elif "textbox" in command:
            # Example for handling textboxes
            textbox_name = command.split("textbox")[1].strip()
            locator_type = input("Enter the locator type (ID, NAME, CSS_SELECTOR, XPATH, etc.): ").upper()
            locator_value = input("Enter the locator value: ")

            textbox = find_element_by_locator(driver, locator_type, locator_value)
            if textbox:
                text_to_enter = input("Type the text to enter: ")
                textbox.send_keys(text_to_enter)
                print(f"Data successfully sent to the textbox '{textbox_name}'")
            else:
                print(f"Textbox with locator {locator_value} not found.")

        elif "search" in command:
            search_query = command.split("search")[1].strip()
            locator_type = input("Enter the locator type (ID, NAME, CSS_SELECTOR, XPATH, etc.): ").upper()
            locator_value = input("Enter the locator value: ")

            search_box = find_element_by_locator(driver, locator_type, locator_value)
            if search_box:
                search_box.send_keys(search_query)
                search_box.send_keys(Keys.RETURN)
                print(f"Performed search for '{search_query}'")
            else:
                print(f"Search box with locator {locator_value} not found.")

        elif "dropdown" in command:
            # Example for handling dropdowns using Select class
            dropdown_name = command.split("dropdown")[1].strip()
            locator_type = input("Enter the locator type (ID, NAME, CSS_SELECTOR, XPATH, etc.): ").upper()
            locator_value = input("Enter the locator value: ")

            dropdown = find_element_by_locator(driver, locator_type, locator_value)
            if dropdown:
                select = Select(dropdown)
                select.select_by_index(0)
                print(f"Selected the first option in the dropdown '{dropdown_name}'")
            else:
                print(f"Dropdown with locator {locator_value} not found.")

        elif "alert" in command:
            alert_action = input("Enter the action for the alert (ACCEPT, DISMISS, TEXT): ").upper()
            alert_text=''
            if alert_action == "TEXT":
                alert_text = input("Enter the text for the alert: ")
            try:
                alert = driver.switch_to.alert
                if alert_action == "ACCEPT":
                    alert.accept()  # Accept the alert
                    print("Accepted the alert.")
                elif alert_action == "DISMISS":
                    alert.dismiss()  # Dismiss the alert
                    print("Dismissed the alert.")
                elif alert_action == "TEXT":
                    alert.send_keys(alert_text)  # Input text into the alert
                    alert.accept()  # Accept the alert after sending text
                    print(f"Sent text to the alert and accepted.")
                else:
                    print("Invalid alert action. Please enter ACCEPT, DISMISS, or TEXT.")
            except NoAlertPresentException:
                print("No alert present.")

        elif "checkbox" in command:
            # Example for handling checkboxes
            checkbox_name = command.split("checkbox")[1].strip()
            locator_type = input("Enter the locator type (ID, NAME, CSS_SELECTOR, XPATH, etc.): ").upper()
            locator_value = input("Enter the locator value: ")

            checkbox = find_element_by_locator(driver, locator_type, locator_value)
            if checkbox:
                checkbox.click()
                print(f"Clicked on the checkbox '{checkbox_name}'")
            else:
                print(f"Checkbox with locator {locator_value} not found.")

        elif "select" in command:
            # Example for selecting an option in a dropdown using its visible text
            select_name = command.split("select")[1].strip()
            locator_type = input("Enter the locator type (ID, NAME, CSS_SELECTOR, XPATH, etc.): ").upper()
            locator_value = input("Enter the locator value: ")

            select = find_element_by_locator(driver, locator_type, locator_value)
            if select:
                select.select_by_visible_text("Option 1")  # Hardcoded option selection for demonstration
                print(f"Selected 'Option 1' in the dropdown '{select_name}'")
            else:
                print(f"Dropdown with locator {locator_value} not found.")

        elif "radio button" in command:
            # Example for handling radio buttons
            radio_button_name = command.split("radio button")[1].strip()
            locator_type = input("Enter the locator type (ID, NAME, CSS_SELECTOR, XPATH, etc.): ").upper()
            locator_value = input("Enter the locator value: ")

            radio_button = find_element_by_locator(driver, locator_type, locator_value)
            if radio_button:
                radio_button.click()
                print(f"Clicked on the radio button '{radio_button_name}'")
            else:
                print(f"Radio button with locator {locator_value} not found.")

        elif "drag and drop" in command:
            # Example for handling drag-and-drop
            source_element_name, destination_element_name = command.split("drag and drop")[1].strip().split(" to ")
            source_locator_type = input(
                "Enter the locator type for source element (ID, NAME, CSS_SELECTOR, XPATH, etc.): ").upper()
            source_locator_value = input("Enter the locator value for source element: ")
            destination_locator_type = input(
                "Enter the locator type for destination element (ID, NAME, CSS_SELECTOR, XPATH, etc.): ").upper()
            destination_locator_value = input("Enter the locator value for destination element: ")

            source_element = find_element_by_locator(driver, source_locator_type, source_locator_value)
            destination_element = find_element_by_locator(driver, destination_locator_type, destination_locator_value)

            if source_element and destination_element:
                actions = ActionChains(driver)
                actions.drag_and_drop(source_element, destination_element).perform()
                print(f"Dragged '{source_element_name}' to '{destination_element_name}'")
            else:
                if not source_element:
                    print(f"Source element with locator {source_locator_value} not found.")
                if not destination_element:
                    print(f"Destination element with locator {destination_locator_value} not found.")

        else:
            print(f"Unknown command: {command}")

    except NoSuchElementException as e:
        print(f"Element not found: {e}")
    except ElementClickInterceptedException as e:
        print(f"Click intercepted: {e}")
    except TimeoutException as e:
        print(f"Timeout waiting for element: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    global command
    driver = initialize_driver()
    print(f"Default URL: {default_url}")

    try:
        speech_mode = False  # Flag to track if the program is in speech mode
        while True:
            if not speech_mode:
                print("Enter a command (or type 'exit' to quit):")
                text_command = input().lower()
            else:
                print("Speak now:")
                speech_command = speech_to_text()
                if speech_command:
                    print("Speech:", speech_command)
                    text_command = speech_command.lower()
                else:
                    # If speech recognition fails, continue to the next iteration
                    continue

            # Check if the user wants to switch to speech mode
            if text_command.strip().lower() == "speech mode":
                speech_mode = True
                continue  # Skip the rest of the loop and prompt for speech input

            # Check if the user wants to switch to text mode
            if text_command.strip().lower() == "text mod":
                speech_mode = False
                continue  # Skip the rest of the loop and prompt for text input

            # Check for exit command
            if text_command == 'exit':
                break

            if text_command:
                execute_command(driver, text_command)

    except KeyboardInterrupt:
        print("Script interrupted by user.")

    finally:
        driver.quit()
        print("Browser closed.")


if __name__ == "__main__":
    main()

