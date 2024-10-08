


from playwright.sync_api import Playwright, sync_playwright, expect
import pandas as pd
import time, json

URL = "https://www.nmlsconsumeraccess.org/TuringTestPage.aspx?ReturnUrl=/Home.aspx/SubSearch"
USER_INFO_URL = "https://www.nmlsconsumeraccess.org/EntityDetails.aspx/INDIVIDUAL/"

# Get ZIP code from list
df = pd.read_csv("fl-zip-codes-data.csv")
zip_list = df["zip"].tolist()
users_ids = []


def run(playwright: Playwright) -> None:
	browser = playwright.chromium.launch(headless=False, slow_mo=50)
	context = browser.new_context()
	page = context.new_page()
	page.goto(URL)
	time.sleep(10)

	# Loop through each zip
	for zip_code in zip_list:
		zip_code_index = zip_list.index(zip_code)
		print(zip_code_index + 1)
		if zip_code_index == 0:
			agree_button = page.query_selector("#ctl00_MainContent_cbxAgreeToTerms")
			agree_button.click()
			time.sleep(3)
			captcha_field = page.query_selector(".authenticateBox > input")
			captcha_text = input("Enter captcha characters: \n")
			print()
			captcha_field.fill(captcha_text)
			time.sleep(2)
			continue_button = page.query_selector("div.accept input#ctl00_MainContent_btnContinue")
			continue_button.click()
			time.sleep(1)
		else:
			pass

		input_field = page.query_selector("input#searchText")
		while input_field == None:
			time.sleep(1)
			captcha_field = page.query_selector(".authenticateBox > input")
			if captcha_field != None:
				captcha_field.fill("")
				captcha_text = input("Enter captcha characters: \n")
				print()
				captcha_field.fill(captcha_text)
				continue_button = page.query_selector("div.accept input#ctl00_MainContent_btnContinue")
				continue_button.click()
				time.sleep(2)
			else:
				input_field = page.query_selector("input#searchText")

		# Enter the ZIP code on input field.
		input_field.fill("")
		input_field.fill(str(zip_code))
		time.sleep(1)

		checkbox = page.query_selector("input#filterIndividual")
		checkbox.click()

		dropdown = page.query_selector("select#states")
		dropdown.select_option("FL")

		apply_filter_button = page.query_selector("div.applyFilter")
		apply_filter_button.click()
		time.sleep(3)

		should_continue = True
		consecutive_next_on_count = 0  # Counter for consecutive 'nextOn' elements
		while should_continue:
			# Find all elements with the class 'name' inside a 'div'
			try:
				users_elements = page.query_selector_all("div.name")
				for user in users_elements:
					# Extract user ID from the 'id' attribute and get user id, next append it users_ids.
					user_id = user.get_attribute("id").split("_")[1]
					users_ids.append(user_id)
			except:
				pass

			# Check if there's next page.
			next_page_element = page.query_selector("div.pageNav ul > li:last-child")
			if next_page_element != None:
				class_name = next_page_element.evaluate("node => node.className")
				print(class_name)
				if class_name == "nextOn":
					consecutive_next_on_count += 1
					if consecutive_next_on_count > 20:
						break  # Break the loop if more than 50 'nextOn' elements
					try:
						page.click("div.pageNav ul > li:last-child a", timeout=500)
					except:
						pass
					time.sleep(1)
				else:
					should_continue = False
			else:
				should_continue = False

		# Write users ids on usrs-ids.json
		with open("FL-ids.json", "w") as file:
			json.dump(users_ids, file)

	# ---------------------
	browser.close()


with sync_playwright() as playwright:
	run(playwright)
