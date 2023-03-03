from dataclasses import dataclass

from colorama import Fore
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement

from login import *


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


def addToCart(driver, items, selected_item=None, modifiers_choices=None, comments=None):
    """Adds an item to the cart.
    :param comments: 
    :param modifiers_choices: 
    :param items: 
    :param selected_item: 
    :param driver:
    """
    itemIndex = 99999
    # If no item index is given, ask the user for one. Otherwise, use the given index.

    wait = WebDriverWait(driver, 150, poll_frequency=1)
    # TODO move all code about selecting options to a script to search all stores
    if itemIndex is None:
        # Iterates through each item in the list of items and prints the name and index

        for item in items:
            print(str(items.index(item)) + " - " + item.name)
        print("999 - To not add an item")
        # Asks the user for the index of the item they want to add
        itemIndex = int(input("Enter the index of the item you want to add to cart: \n"))

    # Checks if the user doesn't want to add an item
    if itemIndex != 999:
        if selected_item is None:
            selected_item = items[itemIndex]
        try:
            # Adds the item to the cart
            actions = ActionChains(driver)
            actions.move_to_element(selected_item.cartPointer).perform()
            selected_item.cartPointer.click()
            wait.until(ec.visibility_of_element_located((By.ID, "item-detail-parent")))
            wait.until(ec.visibility_of_element_located((By.CLASS_NAME, 'add-to-cart-button')))
            itemPane = driver.find_element(By.ID, "item-detail-parent")

            # looks for the modifiers element
            wait.until(ec.visibility_of_element_located((By.CLASS_NAME, 'add-to-cart-button')))
            modifiersAvailable = len(itemPane.find_elements(By.CLASS_NAME, "modifiers")) > 0

            if modifiersAvailable:
                add_modifiers(driver, itemPane, modifiers_choices)

            if comments is not None:
                actions.move_to_element(itemPane.find_element(By.CLASS_NAME, "custom-tip-input-field")).perform()
                itemPane.find_element(By.CLASS_NAME, "custom-tip-input-field").send_keys(comments)

            itemPane.find_element(By.CLASS_NAME, 'add-to-cart-button').click()
            print("Added " + selected_item.name + " to cart")


        except Exception as e:
            # Catches any errors and prints the error
            print("Error adding item to cart")
            try:
                itemPane.find_element(By.CLASS_NAME, 'close-icon').click()
            except:
                print("Couldn't close item pane")
            print(e)
            print("Couldn't add " + str(selected_item.name) + " to cart")


def fulfillment(firstName, lastInitial, phoneNumber, driver, wait=True):
    """Fulfills the order.
    :param driver:
    """

    wait = WebDriverWait(driver, 150, poll_frequency=1)
    # Clicks the cart button, waits for the checkout button to appear and clicks it
    driver.find_element(By.CLASS_NAME, "cart-icon").click()
    wait.until(ec.element_to_be_clickable((By.CLASS_NAME, "pay-cart-button")))
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

    # if wait:
    #     input("IF YOU PRESS ENTER YOU WILL BUY FOOD")
    #     input("IF YOU PRESS ENTER AGAIN YOU WILL BUY FOOD")
    #     input("IF YOU PRESS ENTER AGAIN YOU WILL BUY FOOD")
    # # Clicks the finalize button, waits for the payment buttons to load, and selects the RIT Dining Dollars method
    # wait.until(ec.visibility_of_element_located((By.CLASS_NAME, "pay-button")))
    # driver.find_element(By.CLASS_NAME, "pay-button").click()
    # finalCheckoutSelector = "#parent > div.BottomContainer.sc-mWPeY.iESGGn.sc-bwzfXH.hKiLMS.sc-bdVaJa.iHZvIS > div > div.desktop-pay.sc-khfTgR.cOrHDO.sc-bwzfXH.hKiLMS.sc-bdVaJa.iHZvIS > div > div.pay-list-top-container.sc-koJQpy.hVbJaq.sc-bwzfXH.hKiLMS.sc-bdVaJa.iHZvIS > div.pay-options-parent.sc-ckixc.ddwhEt.sc-bwzfXH.hKiLMS.sc-bdVaJa.iHZvIS > div.click-cont.container.tile.atrium-3.sc-kQeHGI.lbGlam.sc-bwzfXH.cjHxAH.sc-bdVaJa.iHZvIS > div > div.detail-container-atrium.sc-fWMzbn.wlcrT.sc-bwzfXH.iaREIe.sc-bdVaJa.gRrvFh > div"
    # wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, finalCheckoutSelector)))
    # driver.find_element(By.CSS_SELECTOR, finalCheckoutSelector).click()
    #
    # # Waits for the text receipt button to load and clicks it
    # textReceiptSelector = "#parent > div.BottomContainer.sc-mWPeY.iESGGn.sc-bwzfXH.hKiLMS.sc-bdVaJa.iHZvIS > div > div.additional-options-container.sc-ePZHVD.fphWHk.sc-bwzfXH.hKiLMS.sc-bdVaJa.iHZvIS > div > div:nth-child(3) > button"
    # wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, textReceiptSelector)))
    # driver.find_element(By.CSS_SELECTOR, textReceiptSelector).click()
    #
    # # Waits for the send button to load and clicks it
    # sendSelector = "#receipt-modal > div.receipt-modal-parent.sc-bmyXtO.lkstDj.sc-frDJqD.bDtUxi.sc-ksYbfQ.kYqsUP.sc-TOsTZ.cESxnL > div.sc-kaNhvL.fPGvtj.sc-bdVaJa.gRrvFh > button"
    # wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, sendSelector)))
    # driver.find_element(By.CSS_SELECTOR, sendSelector).click()


def open_login(driver):
    wait = WebDriverWait(driver, 150, poll_frequency=1)
    # Waits until the cart icon is visible and clicks it
    wait.until(ec.visibility_of_element_located((By.CLASS_NAME, "cart-icon")))
    driver.find_element(By.CLASS_NAME, "cart-icon").click()

    # Waits until the checkout icon is visible and clicks it
    wait.until(ec.visibility_of_element_located((By.CLASS_NAME, "pay-cart-button")))
    driver.find_element(By.CLASS_NAME, "pay-cart-button").click()

    # Waits until the login icon is visible and clicks it
    wait.until(ec.visibility_of_element_located((By.CLASS_NAME, "login-btn-atrium")))
    driver.find_element(By.CLASS_NAME, "login-btn-atrium").click()


def other_open_login(driver):
    wait = WebDriverWait(driver, 150, poll_frequency=1)
    wait.until(ec.visibility_of_element_located((By.CLASS_NAME, "agilysys-icon-menu_black")))
    driver.find_element(By.CLASS_NAME, "agilysys-icon-menu_black").click()

    # Waits until the checkout icon is visible and clicks it
    wait.until(ec.visibility_of_element_located((By.CLASS_NAME, "sign-in")))
    driver.find_element(By.CLASS_NAME, "sign-in").click()

    # Waits until the login icon is visible and clicks it
    wait.until(ec.visibility_of_element_located((By.CLASS_NAME, "login-btn-atrium")))
    driver.find_element(By.CLASS_NAME, "login-btn-atrium").click()


def breakfast(driver, amount=2, add_drink=True):
    driver.get("https://ondemand.rit.edu/")
    selectStore(driver, "Ctrl Alt DELi")
    items = selectCategory(driver, "Breakfast")
    selected_item = select_item(items, "Bagel, Egg, and Cheese Sandwich")
    for i in range(amount):
        addToCart(driver, items, selected_item, {"Cheese": "Extra Cheese"}, "On a roll please")
    if add_drink:
        items = selectCategory(driver, "Beverages")
        selected_item = select_item(items, "Tropicana Apple Juice")
        addToCart(driver, items, selected_item)


def commons_burger(driver, amount=1):
    global items
    driver.get("https://ondemand.rit.edu/")
    selectStore(driver, "The Commons")
    items = selectCategory(driver, "Grill")
    selectedItem = select_item(items, "Black Bean Burger")
    for i in range(amount):
        addToCart(driver, items, selectedItem, {"Add Cheese?": "American Cheese"})
