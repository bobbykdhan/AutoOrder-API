from dataclasses import dataclass

from colorama import Fore
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement

from login import *
from webdriver_handler import create_driver


@dataclass
class Item:
    """Class for keeping track of an item in store inventory."""
    name: str
    price: float
    cartPointer: WebElement


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
    store, category, items = setupOrder(orderString)

    selectCategory(driver, category)
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
    sign_in(driver)
    input("Waiting for duo press any key when complete")

    # Calls the fulfillment function to complete the purchase after the cart container is loaded
    wait.until(ec.presence_of_element_located((By.CLASS_NAME, "cart-link-container")))
    print("Fulfilling order\n")
    # fulfillment(firstName, lastInitial, phoneNumber, None)
    print("Done placing order\n")


def randomDebug(driver=None):
    if driver is None:
        driver = create_driver()
    driver.get("https://ondemand.rit.edu/")
    selectStore(driver, "Sol's Underground & Beanz")
    selectCategory(driver, "Beverages")


def selectStore(driver, selected_store=None):
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
        if selected_store is None or selected_store == "":
            selected_store = str(input("Select a store by entering the index\n"))
            selected_store = stores[int(selected_store)]
        for store in stores:
            if selected_store in str(store.name):
                print("Selected store: " + store.name)
                if store.isClosed:
                    raise Exception("Store is closed")
                else:
                    store.selectButton.click()
                return


def selectCategory(driver, selectedCategory=None):
    """Allows the user to change the category.
    :param driver:
    """
    # Clears the list of items

    wait = WebDriverWait(driver, 150, poll_frequency=1)
    wait.until(ec.visibility_of_element_located((By.CLASS_NAME, "MuiButtonBase-root")))
    choice = None
    categories = driver.find_elements(By.CLASS_NAME, "MuiButtonBase-root")
    index = 0
    for category in categories:
        print(str(index) + " - " + category.text)
        index += 1
    # Asks the user for the index of the category they want to select and then clicks it
    if selectedCategory is None or selectedCategory == "":
        choice = input("Choose the menu you want to shop from: \n")
    else:
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
    return searchForItems(int(choice), driver)


def searchForItems(categoryNumber, driver):
    """Searches for items in the store. Creates an updated a list of items.
    :param driver:
    """
    items = []
    # Waits for the store to load
    print("Searching for items")

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
    return items


def select_item(items, item_name=None):
    if item_name is None:
        for item in items:
            print(str(items.index(item)) + " - " + item.name)
        print("999 - To not add an item")
        # Asks the user for the index of the item they want to add
        itemIndex = int(input("Enter the index of the item you want to add to cart: \n"))
        if itemIndex == 999:
            return None
        return items[itemIndex]
    for item in items:
        if item_name in item.name:
            return item
    return None


def add_modifiers(driver, itemPane, modifersChoices=None):
    """Adds modifiers to the item
    :param itemPane:
    :param modifersChoices: [{"Group": "Item", "Group": "Item"}]
    """
    actions = ActionChains(driver)
    modifiersPane = itemPane.find_element(By.CLASS_NAME, "modifiers")
    print("Modifiers Available")
    modifiersList = {}
    modifierGroups = modifiersPane.find_elements(By.XPATH, "./*")
    modifierGroupsList = []
    for modifierGroup in modifierGroups:

        name, rules = modifierGroup.find_element(By.ID, "modifier-header-parent").text.split("\n")
        modifierGroupsList.append(name + " - " + rules)
        modifiersList[name] = []

        modifiers = modifierGroup.find_elements(By.XPATH, "./*")

        for modifierCount in range(1, len(modifiers)):
            modifiersList[name].append(
                Modifier(modifiers[modifierCount].text, modifierCount, modifiers[modifierCount]))

    for modifierChoice in modifersChoices.keys():
        for modifierGroup in modifiersList:
            if modifierChoice in modifierGroup:

                for modifier in modifiersList[modifierGroup]:
                    if modifersChoices[modifierChoice] in modifier.name:
                        # actions.move_to_element(modifiersList[modifierGroup][modifiersList[modifierGroup].index(modifier)+1].selectButton).perform()
                        actions.move_to_element(modifier.selectButton).perform()
                        modifier.selectButton.click()
                        print("Added " + modifier.name)
                        break

    # while True:
    #     count = 0
    #     for modifierGroup in modifierGroupsList:
    #         print(str(count) + " - " + modifierGroup)
    #         count += 1
    #     print("999 - To not add a modifier")
    #     categoryChoice = int(input(
    #         "Enter the index of the modifier you want to add (You must add all of the required ones): \n"))
    #     if categoryChoice != 999 and categoryChoice < len(modifierGroupsList):
    #         groupBeingUsed = modifiersList[modifierGroupsList[categoryChoice].split(" - ")[0]]
    #         while True:
    #             print(modifierGroupsList[categoryChoice])
    #             for modifier in groupBeingUsed:
    #                 print(str(groupBeingUsed.index(modifier)) + " - " + modifier.name, end="")
    #                 if modifier.isSelected:
    #                     print(Fore.RED + " - SELECTED" + Fore.RESET)
    #
    #                 else:
    #                     print()
    #             print("999 - To go back to category selection")
    #             modifierChoice = int(input("Enter the index of the modifier you want to add: \n"))
    #             if modifierChoice != 999:
    #
    #                 actions.move_to_element(groupBeingUsed[modifierChoice].selectButton).perform()
    #                 groupBeingUsed[modifierChoice].selectButton.click()
    #
    #                 groupBeingUsed[modifierChoice].isSelected = not groupBeingUsed[
    #                     modifierChoice].isSelected
    #             else:
    #                 break
    #     else:
    #         break


def addToCart(driver, items, selectedItem=None, modifersChoices=None, comments=None):
    """Adds an item to the cart.
    :param driver:
    """
    itemIndex = 99999
    # If no item index is given, ask the user for one. Otherwise, use the given index.
    # TODO: add the ability to add items without waiting for user input

    wait = WebDriverWait(driver, 150, poll_frequency=1)

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
        if selectedItem is None:
            selectedItem = items[itemIndex]
        try:
            # Adds the item to the cart
            actions = ActionChains(driver)
            actions.move_to_element(selectedItem.cartPointer).perform()
            selectedItem.cartPointer.click()
            wait.until(ec.visibility_of_element_located((By.ID, "item-detail-parent")))
            wait.until(ec.visibility_of_element_located((By.CLASS_NAME, 'add-to-cart-button')))
            itemPane = driver.find_element(By.ID, "item-detail-parent")

            # looks for the modifiers element
            wait.until(ec.visibility_of_element_located((By.CLASS_NAME, 'add-to-cart-button')))
            modifiersAvailable = len(itemPane.find_elements(By.CLASS_NAME, "modifiers")) > 0

            if modifiersAvailable:
                add_modifiers(driver, itemPane, modifersChoices)

            if comments is None:
                comments = input("Text for the comments section (N to skip):")

            if comments.capitalize() != "N":
                actions.move_to_element(itemPane.find_element(By.CLASS_NAME, "custom-tip-input-field")).perform()
                itemPane.find_element(By.CLASS_NAME, "custom-tip-input-field").send_keys(comments)

            itemPane.find_element(By.CLASS_NAME, 'add-to-cart-button').click()
            print("Added " + selectedItem.name + " to cart")


        except Exception as e:
            # Catches any errors and prints the error
            print("Error adding item to cart")
            itemPane.find_element(By.CLASS_NAME, 'close-icon').click()
            print(e)
            print("Couldn't add " + str(selectedItem.name) + " to cart")
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

# driver = create_driver(False, True)
# debug(driver)
