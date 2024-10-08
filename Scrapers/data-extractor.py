from playwright.sync_api import Playwright, sync_playwright, expect
import time, json
import pandas as pd

USER_INFO_URL = "https://www.nmlsconsumeraccess.org/EntityDetails.aspx/INDIVIDUAL/"


def run(playwright: Playwright) -> None:
	browser = playwright.chromium.launch(headless=False, slow_mo=50)
	context = browser.new_context()
	page = context.new_page()

	# Read user ids from json files
	with open("TN-ids.json", "r") as file:
		data_list = json.load(file)
		data_list = list(set(data_list))
		part_size = len(data_list) // 3
		# Use list slicing to create three parts
		part1 = data_list[0:part_size]
		part2 = data_list[part_size:2*part_size]
		part3 = data_list[2*part_size:]

  # Get names and phone numbers, and save them on utah-data.csv 
	data = []
	users_ids = data_list
	for user_id in users_ids:
		try:
			page.goto(USER_INFO_URL + user_id)
			time.sleep(1)
		except:
			time.sleep(10)
			try:
				page.goto(USER_INFO_URL + user_id)
				time.sleep(1)
			except:
				time.sleep(10)
				page.goto(USER_INFO_URL + user_id)

		user_index = users_ids.index(user_id)
		print(user_index + 1 )
		if user_index == 0:
			print(len(users_ids))
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
		
		name_element = page.query_selector(".individual")
		phone_number_element = page.query_selector(".summary > table:nth-child(3) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(4)")

		while name_element == None and phone_number_element == None:
			captcha_field = page.query_selector(".authenticateBox > input")
			captcha_field.fill("")
			captcha_text = input("Enter captcha characters: \n")
			print()
			continue_button = page.query_selector("div.accept input#ctl00_MainContent_btnContinue")
			captcha_field.fill(captcha_text)
			time.sleep(2)
			continue_button.click()
			time.sleep(1)

			name_element = page.query_selector(".individual")
			phone_number_element = page.query_selector(".summary > table:nth-child(3) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(4)")


		name = name_element.text_content().strip()
		phone_number = phone_number_element.evaluate('(element) => element.textContent').strip()
				
		entry_data = { "name": name, "phone number": phone_number}
		data.append(entry_data)
		

	# Create a DataFrame from the list of data
	# Save the DataFrame to a CSV file
	df = pd.DataFrame(data)
	df.to_csv("TN-final.csv", index=False)


	# ---------------------
	context.close()
	browser.close()


with sync_playwright() as playwright:
	run(playwright)
