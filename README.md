Overview

This project is a Python-based application that automates the process of scraping game data from the Steam Store. It collects detailed information about top-selling games, including names, prices, discounts, images, and video links. The application features a graphical user interface (GUI) built with Tkinter, allowing users to start and stop the automation process and save the retrieved data in a structured format.
Features

    Web Scraping with BeautifulSoup and cloudscraper: Bypasses cloud security measures to scrape data from the Steam Store efficiently.
    GUI with Tkinter: Provides an intuitive interface to control the scraping process without dealing with the command line.
    Asynchronous Execution with Threading: Ensures the GUI remains responsive during the scraping process.
    Data Retrieval: Collects game names, current and original prices, discount percentages, image URLs, and video links.
    Data Export: Allows users to save the scraped data into a text file for further analysis or sharing.
    Error Handling: Includes robust error handling to manage network issues and unexpected changes in the website structure.

Technologies Used

    Python 3
    Tkinter: For building the graphical user interface.
    BeautifulSoup: For parsing HTML content.
    cloudscraper: To handle Cloudflare's anti-bot protection.
    threading: To run the scraping process without freezing the GUI.

How It Works

    Start the Automation: Click the "Start Automation" button to initiate the scraping process.
    Data Scraping: The application sends HTTP requests to the Steam Store, parses the HTML content, and extracts the required information.
    Data Display: Progress and status messages are displayed in the console for real-time monitoring.
    Save Data: After scraping, click the "Get Data" button to save the information into a text file.
    Stop Automation: The "Stop" button allows you to halt the scraping process at any time.

Installation and Usage

    Clone the Repository:

    bash

git clone https://github.com/yourusername/steam-data-scraper.git

Install Dependencies:

bash

pip install cloudscraper pandas beautifulsoup4 lxml

Run the Application:

bash

python steam_data_scraper.py

Use the GUI:

    Click "Start Automation" to begin.
    Click "Get Data" to save the results.
    Click "Stop" to halt the process if needed.
