from dataclasses import dataclass

from colorama import Fore
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


@dataclass
class Item:
    """Class for keeping track of an item in store inventory."""
    name: str
    price: float
    cartPointer: WebElement


# Initialize the store inventory
global items
items = []


@dataclass
class Store:
    """Class for keeping track of a store."""

    name: str
    hours: str
    isClosed: bool
    selectButton: WebElement


@dataclass
class Modifier:
    """Class for keeping track of a store."""
    # count = 0
    name: str
    position: int
    selectButton: WebElement
    isSelected: bool = False


@dataclass
class itemListing:
    category: str
    item: str


def setupOrder(orderString):
    # Sample order string
    # store; category:item, category:item, category:item
    """Function that sets up the order by parsing the order string and returning a tuple of the store, category, and items."""
    # Splits the order string into a list of items
    orderList = orderString.split(",")
    # Gets the store name
    store = orderList[0]
    # Gets the category name
    category = orderList[1]
    # Gets the items
    items = orderList[2:]
    return (store, category, items)


def main(orderString, driver):
    """ Main function that runs the program."""
    wait = WebDriverWait(driver, 150, poll_frequency=1)
    # Opens the ondemand website
    driver.get("https://ondemand.rit.edu/")

    store, category, items = setupOrder(orderString)

    # username, password, firstName, lastInitial, phoneNumber = USERNAME, PASSWORD, "", "", PHONE
    # Asks the user for the store they want to shop from

    selectStore(store, None)

    # Waits for the site to load and calls the selectCategory function

    # wait.until(ec.visibility_of_element_located((By.CLASS_NAME, "detail-container")))
    # driver.get("https://ondemand.rit.edu/streamlinedmenu/dc9df36d-8a64-42cf-b7c1-fa041f5f3cfd/2195")

    selectCategory(category, None)
    input("Press Enter to continue...")
    # Calls the addToCart function and asks the user if they wish to continue shopping, change the category, or checkout
    while True:
        addToCart(None)
        choice = input(
            "Press Y if you are done adding to cart, Press C if you wish to choose another category, Press any key to keep selecting\n")
        if (choice == "Y"):
            break
        elif choice == "C":
            # Calls the selectCategory function for the user to change their category
            selectCategory(driver)

    print("Logging in\n")

    # Calls the signIn function to log the user in
    login(driver)
    input("Waiting for duo press any key when complete")

    # Calls the fulfillment function to complete the purchase after the cart container is loaded
    wait.until(ec.presence_of_element_located((By.CLASS_NAME, "cart-link-container")))
    print("Fulfilling order\n")
    fulfillment(firstName, lastInitial, phoneNumber, None)
    print("Done placing order\n")


def selectStore(selectedStore, driver):
    """ Selects the store the user wants to shop from
    :param driver:
    """

    # Confirms the site is loaded and stores the store containers in a list
    wait = WebDriverWait(driver, 150, poll_frequency=1)
    wait.until(ec.visibility_of_element_located((By.CLASS_NAME, "top-container")))
    storeContainers = driver.find_element(By.CLASS_NAME, "BottomContainer").find_elements(By.CLASS_NAME,
                                                                                          "top-container")
    print("Site loaded\n")
    stores = []
    # Loops through the store containers and creates a Store object for each store
    for storeContainer in storeContainers:
        list = storeContainer.text.split("\n")
        isClosed = (list[2] == "Closed")
        stores.append(Store(list[0], list[1], isClosed, storeContainer.find_element(By.ID, "pickup-0")))

    while True:
        for store in stores:
            print(str(stores.index(store)) + " - " + store.name)
            print(store.hours)
            if store.isClosed:
                print(Fore.RED + "Closed\n" + Fore.RESET)
            else:
                print("Open\n")
        if selectedStore is None or selectedStore == "":
            selectedStore = str(input("Select a store by entering the index\n"))
            selectedStore = stores[int(selectedStore)]
        for store in stores:
            if selectedStore in str(store.name):
                print("Selected store: " + store.name)
                if store.isClosed:
                    raise Exception("Store is closed")
                else:
                    store.selectButton.click()
                return


def selectCategory(selectedCategory, driver):
    """Allows the user to change the category.
    :param driver:
    """
    # Clears the list of items
    items.clear()

    wait = WebDriverWait(driver, 150, poll_frequency=1)
    wait.until(ec.visibility_of_element_located((By.CLASS_NAME, "MuiButtonBase-root")))

    categories = driver.find_elements(By.CLASS_NAME, "MuiButtonBase-root")
    index = 0
    for category in categories:
        print(str(index) + " - " + category.text)
        index += 1
    # Asks the user for the index of the category they want to select and then clicks it

    choice = input("Choose the menu you want to shop from: \n")
    choice = None
    for category in categories:
        if selectedCategory in category.text:
            choice = categories.index(category)
            break

    if int(choice) > len(categories) or choice == None:
        raise Exception("INVALID CHOICE")
    categories[int(choice)].click()
    print("Reindexing items\n")
    # Waits for the store to load and searches the site for the items
    wait.until(ec.visibility_of_element_located((By.CLASS_NAME, "detail-container")))
    searchForItems(int(choice), None)


def searchForItems(categoryNumber, driver):
    """Searches for items in the store. Creates an updated a list of items.
    :param driver:
    """

    # Waits for the store to load
    print("Searching for items")

    driver.find_elements(By.CLASS_NAME, "MuiTabs-flexContainer")[0].find_elements(By.CSS_SELECTOR, "*")[
        categoryNumber].click()

    page = driver.find_element(By.ID, "streamlinedmenu")

    containers = page.find_elements(By.CLASS_NAME, "list-items-container")
    # Gets the list of all elements with a class name of "detail-container"

    itemContainersElement = containers[categoryNumber].find_element(By.CLASS_NAME, "item-listcontainer")
    itemContainers = itemContainersElement.find_elements(By.CLASS_NAME, "top-container")

    # Iterates through each element and creates an Item object for each item
    for itemContainer in itemContainers:
        # Gets the bottom container of the detail
        bottomContainer = itemContainer.find_element(By.CLASS_NAME, "bottom-container")

        # Finds the name, price and cart element of the item and creates an Item object
        price = bottomContainer.text.split("\n")[0]
        cartPointer = bottomContainer.find_element(By.CLASS_NAME, "add-to-cart-text")
        name = itemContainer.find_element(By.CLASS_NAME, "title-hover").text
        newItem = Item(name, price, cartPointer)

        # adds all items to the list of items
        items.append(newItem)


def addToCart(driver, selectedItem=None):
    """Adds an item to the cart.
    :param driver:
    """
    # If no item index is given, ask the user for one. Otherwise, use the given index.
    # TODO: add the ability to add items without waiting for user input
    wait = WebDriverWait(driver, 150, poll_frequency=1)
    itemIndex = None
    if itemIndex is None:
        # Iterates through each item in the list of items and prints the name and index

        for item in items:
            print(str(items.index(item)) + " - " + item.name)
        print("999 - To not add an item")
        # Asks the user for the index of the item they want to add
        itemIndex = int(input("Enter the index of the item you want to add to cart: \n"))

    # TODO: Add functionality to add items with modifiers
    # Checks if the user doesn't want to add an item
    if itemIndex != 999:
        try:
            # Adds the item to the cart
            items[itemIndex].cartPointer.click()
            wait.until(ec.visibility_of_element_located((By.ID, "item-detail-parent")))
            wait.until(ec.visibility_of_element_located((By.CLASS_NAME, 'add-to-cart-button')))
            idk = driver.find_element(By.ID, "item-detail-parent")

            # looks for the modifiers element
            wait.until(ec.visibility_of_element_located((By.CLASS_NAME, 'add-to-cart-button')))
            modifiers = idk.find_element(By.CLASS_NAME, "modifiers")
            modifiersAvailable = len(idk.find_elements(By.CLASS_NAME, "modifiers")) > 0

            if modifiersAvailable:
                print("Modifiers Available")
                modifiersList = {}
                modifierGroups = modifiers.find_elements(By.CLASS_NAME, "sc-cTjmhe")
                modifierGroupsList = []
                for modifierGroup in modifierGroups:

                    name, rules = modifierGroup.find_element(By.ID, "modifier-header-parent").text.split("\n")
                    modifierGroupsList.append(name + " - " + rules)
                    modifiersList[name] = []

                    # print(name + " - " + rules)
                    modifiers = modifierGroup.find_elements(By.XPATH, "./*")

                    for modifierCount in range(1, len(modifiers)):
                        modifiersList[name].append(
                            Modifier(modifiers[modifierCount].text, modifierCount, modifiers[modifierCount]))

                while True:
                    count = 0
                    for modifierGroup in modifierGroupsList:
                        print(str(count) + " - " + modifierGroup)
                        count += 1
                    print("999 - To not add a modifier")
                    categoryChoice = int(input(
                        "Enter the index of the modifier you want to add (You must add all of the required ones): \n"))
                    if categoryChoice != 999 and categoryChoice < len(modifierGroupsList):
                        groupBeingUsed = modifiersList[modifierGroupsList[categoryChoice].split(" - ")[0]]
                        while True:
                            print(modifierGroupsList[categoryChoice])
                            for modifier in groupBeingUsed:
                                print(str(groupBeingUsed.index(modifier)) + " - " + modifier.name, end="")
                                if modifier.isSelected:
                                    print(Fore.RED + " - SELECTED" + Fore.RESET)

                                else:
                                    print()
                            print("999 - To go back to category selection")
                            modifierChoice = int(input("Enter the index of the modifier you want to add: \n"))
                            if modifierChoice != 999:

                                actions = ActionChains(driver)
                                # driver.execute_script("arguments[0].scrollIntoView(true);", groupBeingUsed[modifierChoice+1].selectButton)
                                # driver.execute_script("arguments[0].scrollIntoView();", groupBeingUsed[modifierChoice].selectButton)

                                # input("Press enter to continue")
                                # wait.until(ec.visibility_of_element_located(groupBeingUsed[modifierChoice].selectButton.find_element(By.CLASS_NAME, "fa")))
                                # groupBeingUsed[modifierChoice].selectButton.find_element(By.CLASS_NAME, "fa").click()

                                actions.move_to_element(groupBeingUsed[modifierChoice].selectButton).click().perform()

                                # actions.click(groupBeingUsed[modifierChoice].selectButton)
                                # actions.perform()
                                # time.sleep(2)
                                #
                                groupBeingUsed[modifierChoice].isSelected = not groupBeingUsed[
                                    modifierChoice].isSelected
                            else:
                                break
                    else:
                        break

            ask = input("Any text for the comments box? (Y or N")

            if ask.capitalize().equals("Y"):
                idk.find_element(By.CLASS_NAME, "custom-tip-input-field").send_keys(ask)

            idk.find_element(By.CLASS_NAME, 'add-to-cart-button').click()
            print("Added " + items[itemIndex].name + " to cart")


        except Exception as e:
            # Catches any errors and prints the error
            idk.find_element(By.CLASS_NAME, 'close-icon').click()
            print(e)
            print("Couldn't add " + str(items[itemIndex].name) + " to cart")
        except IndexError:
            pass


def fulfillment(firstName, lastInitial, phoneNumber, driver):
    """Fulfills the order.
    :param driver:
    """
    wait = WebDriverWait(driver, 150, poll_frequency=1)
    # Clicks the cart button, waits for the checkout button to appear and clicks it
    driver.find_element(By.CLASS_NAME, "cart-icon").click()
    wait.until(ec.visibility_of_element_located((By.CLASS_NAME, "pay-cart-button")))
    driver.find_element(By.CLASS_NAME, "pay-cart-button").click()

    # Waits for the fulfillment page to load and then fills out the form
    wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, "#parent > input")))
    fields = driver.find_elements(By.CSS_SELECTOR, "#parent > input")

    # Fills out the fields
    fields[0].send_keys(firstName)
    fields[1].send_keys(lastInitial)
    fields[2].send_keys(phoneNumber)

    # Clicks the submit button at the end of the fulfillment form
    driver.find_element(By.CLASS_NAME, "pay-button-site-has-signin").click()

    input("IF YOU PRESS ENTER YOU WILL BUY FOOD")
    input("IF YOU PRESS ENTER AGAIN YOU WILL BUY FOOD")
    input("IF YOU PRESS ENTER AGAIN YOU WILL BUY FOOD")
    # Clicks the finalize button, waits for the payment buttons to load, and selects the RIT Dining Dollars method
    wait.until(ec.visibility_of_element_located((By.CLASS_NAME, "pay-button")))
    driver.find_element(By.CLASS_NAME, "pay-button").click()
    finalCheckoutSelector = "#parent > div.BottomContainer.sc-mWPeY.iESGGn.sc-bwzfXH.hKiLMS.sc-bdVaJa.iHZvIS > div > div.desktop-pay.sc-khfTgR.cOrHDO.sc-bwzfXH.hKiLMS.sc-bdVaJa.iHZvIS > div > div.pay-list-top-container.sc-koJQpy.hVbJaq.sc-bwzfXH.hKiLMS.sc-bdVaJa.iHZvIS > div.pay-options-parent.sc-ckixc.ddwhEt.sc-bwzfXH.hKiLMS.sc-bdVaJa.iHZvIS > div.click-cont.container.tile.atrium-3.sc-kQeHGI.lbGlam.sc-bwzfXH.cjHxAH.sc-bdVaJa.iHZvIS > div > div.detail-container-atrium.sc-fWMzbn.wlcrT.sc-bwzfXH.iaREIe.sc-bdVaJa.gRrvFh > div"
    wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, finalCheckoutSelector)))
    driver.find_element(By.CSS_SELECTOR, finalCheckoutSelector).click()

    # Waits for the text receipt button to load and clicks it
    textReceiptSelector = "#parent > div.BottomContainer.sc-mWPeY.iESGGn.sc-bwzfXH.hKiLMS.sc-bdVaJa.iHZvIS > div > div.additional-options-container.sc-ePZHVD.fphWHk.sc-bwzfXH.hKiLMS.sc-bdVaJa.iHZvIS > div > div:nth-child(3) > button"
    wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, textReceiptSelector)))
    driver.find_element(By.CSS_SELECTOR, textReceiptSelector).click()

    # Waits for the send button to load and clicks it
    sendSelector = "#receipt-modal > div.receipt-modal-parent.sc-bmyXtO.lkstDj.sc-frDJqD.bDtUxi.sc-ksYbfQ.kYqsUP.sc-TOsTZ.cESxnL > div.sc-kaNhvL.fPGvtj.sc-bdVaJa.gRrvFh > button"
    wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, sendSelector)))
    driver.find_element(By.CSS_SELECTOR, sendSelector).click()
