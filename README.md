# ZIP-NMLS-Playwright-Scraper

Web Scraping NMLS Consumer Access Data
Project Overview
This project automates the extraction of user data from the NMLS Consumer Access website. The system uses Playwright to interact with the website, bypass CAPTCHA challenges, and scrape data by inputting ZIP codes from various states. The scraped data is stored in JSON and CSV formats for further analysis.

Features:
Automated Data Scraping: Utilizes Playwright to simulate browser interaction, input ZIP codes, and handle CAPTCHA verification.
Data Handling: The project processes ZIP codes from several states including Florida, Illinois, Michigan, North Carolina, Tennessee, and Texas, scraping user IDs and storing them in JSON files.
CAPTCHA Support: The scraping script prompts for manual CAPTCHA entry, allowing the script to continue even with CAPTCHA challenges.
CSV Integration: ZIP codes are loaded from CSV files for batch processing, ensuring data is systematically retrieved for multiple locations.
Key Files:
main_restrict_nexton.py: The core script responsible for automating the web scraping process. It navigates through the NMLS website, enters ZIP codes, and retrieves individual user IDs.
CSV Files: Each state’s ZIP codes are stored in CSV files (e.g., fl-zip-codes-data.csv), and the scraped data is saved in corresponding CSV/JSON files.
JSON Files: Scraped user IDs are saved in JSON files (e.g., FL-ids.json), enabling easy data retrieval and further processing.
How to Run:
Install Dependencies:

Make sure you have Python and Playwright installed. You can install Playwright by running:

pip install playwright
playwright install
Run the Script:

Execute the scraping script by running:

python main.py
The script will prompt you to solve a CAPTCHA for the first query.
After entering the CAPTCHA, it will process each ZIP code sequentially.
Data Storage:

The scraped data will be saved in the JSON format for user IDs and in the CSV format for any additional information.
