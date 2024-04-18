"""
import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

default_url = "https://www.google.com"

def initialize_driver():
    # Set up Selenium WebDriver (update the path to your chromedriver executable)
    driver = webdriver.Firefox()
    return driver

def speech_to_text():
    # Set up SpeechRecognition
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something:")
        try:
            audio = recognizer.listen(source, timeout=5)  # Adjust timeout if needed
            command = recognizer.recognize_google(audio).lower()
            print("You said: " + command)
            return command

        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Error accessing the speech recognition service: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

def execute_command(driver, command):
    # Implement your command execution logic here
    if "open" in command:
        url = default_url  # Use the default URL specified below
        try:
            driver.get(url)
            print(f"Opened {url}")
        except Exception as e:
            print(f"Error opening {url}: {e}")
    elif "click" in command:
        element_name = command.split("click")[1].strip()
        try:
            element = driver.find_element_by_partial_link_text(element_name)
            element.click()
            print(f"Clicked on {element_name}")
        except Exception as e:
            print(f"Error clicking on {element_name}: {e}")

    elif "search" in command:
        search_query = command.split("search")[1].strip()
        search_box = driver.find_element_by_name("q")  # Update with the correct locator
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)
        print(f"Performed search for {search_query}")

    # Add more commands as needed

def main():
    driver = initialize_driver()
    # Specify the default URL here for the "open" command
    #driver.get(default_url)
    print(f"Default URL: {default_url}")
    try:
        while True:
            command = speech_to_text()
            # Uncomment the line above if you want to listen for speech input
            # and comment the line below
            #command = "open"

            if command:
                execute_command(driver, command)

            # Additional commands can be added here if needed
            # execute_command(driver, "click some_element")
            # execute_command(driver, "search something")
    except KeyboardInterrupt:
        print("Script interrupted by user.")

    finally:
        driver.quit()
        print("Browser closed.")


if __name__ == "__main__":
    main()
"""
import speech_recognition as sr
from selenium import webdriver
from selenium.common import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.alert import Alert
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
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio).lower()
            print("You said: " + command)
            return command

        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Error accessing the speech recognition service: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

def execute_command(driver, command):
    """
    if "open" in command:
        url = default_url
        try:
            driver.get(url)
            print(f"Opened {url}")
        except Exception as e:
            print(f"Error opening {url}: {e}")
    """
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
            # Example for handling dropdowns using Select class
            textbox_name = command.split("textbox")[1].strip()
            q=input("Enter the css selector for the locator: ")
            textbox = driver.find_element(By.CSS_SELECTOR, q)
            # Select the first option (index 0) as an example
            q=input("Type the text to enter: ")
            textbox.send_keys(q)
            print(f"data successfully sent to the textfield {textbox_name}")

        elif "search" in command:
            search_query = command.split("search")[1].strip()
            j=input("Enter the css selector for the search box")
            #=input("Enter the Css Selector")
            search_box = driver.find_element(By.CSS_SELECTOR,j)
            search_box.send_keys(search_query)
            search_box.send_keys(Keys.RETURN)
            print(f"Performed search for {search_query}")

        elif "dropdown" in command:
            # Example for handling dropdowns using Select class
            dropdown_name = command.split("dropdown")[1].strip()
            dropdown = Select(driver.find_element(By.XPATH, f"//*[contains(text(), '{dropdown_name}')]"))
            # Select the first option (index 0) as an example
            dropdown.select_by_index(0)
            print(f"Selected the first option in the dropdown {dropdown_name}")

        elif "alert" in command:
            # Example for handling alerts
            alert_text = command.split("alert")[1].strip()
            alert = Alert(driver)
            alert.send_keys(alert_text)  # Input text into the alert, if needed
            alert.accept()  # Accept the alert
            print(f"Handled the alert with text: {alert_text}")

        elif "checkbox" in command:
            # Example for handling checkboxes
            checkbox_name = command.split("checkbox")[1].strip()
            checkbox = driver.find_element(By.XPATH, f"//*[contains(text(), '{checkbox_name}')]")
            checkbox.click()
            print(f"Clicked on the checkbox {checkbox_name}")

        elif "select" in command:
                # Example for selecting an option in a dropdown using its visible text
                select_name = command.split("select")[1].strip()
                select = Select(driver.find_element(By.XPATH, f"//*[contains(text(), '{select_name}')]"))
                select.select_by_visible_text("Option 1")
                print(f"Selected 'Option 1' in the dropdown {select_name}")

        elif "radio button" in command:
                # Example for handling radio buttons
                radio_button_name = command.split("radio button")[1].strip()
                radio_button = driver.find_element(By.XPATH, f"//*[contains(text(), '{radio_button_name}')]")
                radio_button.click()
                print(f"Clicked on the radio button {radio_button_name}")


        elif "drag and drop" in command:
                # Example for handling drag-and-drop
                source_element_name, destination_element_name = command.split("drag and drop")[1].strip().split(" to ")

                source_element = driver.find_element(By.NAME, source_element_name)
                destination_element = driver.find_element(By.NAME, destination_element_name)

                # Use ActionChains for drag-and-drop
                actions = ActionChains(driver)
                actions.drag_and_drop(source_element, destination_element).perform()

                print(f"Dragged {source_element_name} to {destination_element_name}")

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


    # Add more commands as needed

def main():
    global command
    driver = initialize_driver()
    print(f"Default URL: {default_url}")

    try:
        while True:

            print("Enter a command (or type 'exit' to quit):")
            command = input()
            #command= speech_to_text().lower()

            if command == 'exit':
                break

            if command:
                execute_command(driver, command)

    except KeyboardInterrupt:
        print("Script interrupted by user.")

    finally:
        driver.quit()
        print("Browser closed.")

if __name__ == "__main__":
    main()
