# Author: Bishal Sarang
import json
import pickle
import time

import bs4
import colorama
import requests
from colorama import Back, Fore
from ebooklib import epub
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utils import *
import epub_writer

# Initialize Colorama
colorama.init(autoreset=True)

# Setup Selenium Webdriver
# CHROMEDRIVER_PATH = r"./driver/chromedriver.exe"
# put it into the same folder in Mac
CHROMEDRIVER_PATH = r"./chromedriver"

options = Options()
options.headless = True
# Disable Warning, Error and Info logs
# Show only fatal errors
options.add_argument("--log-level=3")
# driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=options)

s = Service(CHROMEDRIVER_PATH)
# driver = webdriver.Chrome(service=s)
# usernameStr = 'osuyuanqi'
# passwordStr = 'xxx'

driver = webdriver.Chrome(service=s)

def login(url,usernameId, username, passwordId, password, submit_buttonId):
   driver.get(url)
   # driver.find_element(By.ID,usernameId).send_keys(username)
   # driver.find_element(By.ID,passwordId).send_keys(password)
   # driver.find_element(By.ID,submit_buttonId).click()

# Get upto which problem it is already scraped from track.conf file
completed_upto = read_tracker("track.conf")

# Load chapters list that stores chapter info
# Store chapter info
with open('chapters.pickle', 'rb') as f:
    chapters = pickle.load(f)

def download(problem_num, url, title, solution_slug):  
    print(Fore.BLACK + Back.CYAN + f"Fetching problem num " + Back.YELLOW + f" {problem_num} " + Back.CYAN + " with url " + Back.YELLOW + f" {url} ")
    n = len(title)

    try:

        driver.get(url)
        # print(url+"aaaaa")

        # Wait 20 secs or until div with id initial-loading disappears
        element = WebDriverWait(driver, 20).until(
            EC.invisibility_of_element_located((By.ID, "initial-loading"))
        )
        # Get current tab page source
        html = driver.page_source
        soup = bs4.BeautifulSoup(html, "html.parser")
        # print(html,soup,"bbbbb")
        # Construct HTML
        title_decorator = '*' * n
        problem_title_html = title_decorator + f'<div id="title">{title}</div>' + '\n' + title_decorator
        problem_html = problem_title_html + str(soup.find("div", {"class": "content__u3I1 question-content__JfgR"})) + '<br><br><hr><br>'
        
        # Append Contents to a HTML file
        with open("out.html", "ab") as f:
            f.write(problem_html.encode(encoding="utf-8"))
        
        # create and append chapters to construct an epub
        # c = epub.EpubHtml(title=title, file_name=f'chap_{problem_num}.xhtml', lang='hr')
        # c.content = problem_html
        # chapters.append(c)


        # Write List of chapters to pickle file
        dump_chapters_to_file(chapters)
        # Update upto which the problem is downloaded
        update_tracker('track.conf', problem_num)
        print(Fore.BLACK + Back.GREEN + f"Writing problem num " + Back.YELLOW + f" {problem_num} " + Back.GREEN + " with url " + Back.YELLOW + f" {url} " )
        print(Fore.BLACK + Back.GREEN + " successfull ")
        # print(f"Writing problem num {problem_num} with url {url} successfull")

    except Exception as e:
        print(Back.RED + f" Failed Writing!!  {e} ")
        driver.quit()

def main():

    # Leetcode API URL to get json of problems on algorithms categories
    ALGORITHMS_ENDPOINT_URL = "https://leetcode.com/api/problems/algorithms/"

    # Problem URL is of format ALGORITHMS_BASE_URL + question__title_slug
    # If question__title_slug = "two-sum" then URL is https://leetcode.com/problems/two-sum
    ALGORITHMS_BASE_URL = "https://leetcode.com/problems/"

    # Load JSON from API
    algorithms_problems_json = requests.get(ALGORITHMS_ENDPOINT_URL).content
    algorithms_problems_json = json.loads(algorithms_problems_json)

    styles_str = "<style>pre{white-space:pre-wrap;background:#f7f9fa;padding:10px 15px;color:#263238;line-height:1.6;font-size:13px;border-radius:3px margin-top: 0;margin-bottom:1em;overflow:auto}b,strong{font-weight:bolder}#title{font-size:16px;color:#212121;font-weight:600;margin-bottom:10px}hr{height:10px;border:0;box-shadow:0 10px 10px -10px #8c8b8b inset}</style>"
    with open("out.html", "ab") as f:
            f.write(styles_str.encode(encoding="utf-8"))

    # List to store question_title_slug
    links = []
    # extract all the topics that you prefer. e.g. topic is 1,2,3
    # target_topic =[146,200,56,253,273,588,49,79,17,54,212,23,33,460,295,443,51,362,297,138,25,716,44,207,128,151,1647,103,706,1405,1344,1578,348,233,1448,1275,93,1822,979,895,340,545,769,622,1615,1304,285,462,768,984]
    # login("https://leetcode.com/accounts/login/","id_login",usernameStr,"id_password",passwordStr,"signin_btn")
    target_topic = [1,2,3]
    # print(algorithms_problems_json["stat_status_pairs"])
    for child in algorithms_problems_json["stat_status_pairs"]:
            for j in target_topic:
                # question_id is the topic id
                if child['stat']['question_id'] == j:
                    print(child["stat"])

                    question__title_slug = child["stat"]["question__title_slug"]
                    question__article__slug = child["stat"]["question__article__slug"]
                    question__title = child["stat"]["question__title"]
                    frontend_question_id = child["stat"]["question_id"]
                    difficulty = child["difficulty"]["level"]
                    links.append((question__title_slug, difficulty, frontend_question_id, question__title, question__article__slug))

    # Sort by difficulty follwed by problem id in ascending order
    links = sorted(links, key=lambda x: (x[1], x[2]))

    try: 
        # ll=[1,5,6]
        # for i,j in enumerate(ll):
        # for j,i in enumerate(ll):
        for i in range(completed_upto , len(links)):
             question__title_slug, _ , frontend_question_id, question__title, question__article__slug = links[i]
             url = ALGORITHMS_BASE_URL + question__title_slug
             title = f"{frontend_question_id}. {question__title}"
             print(url, title,i,j)

             # Download each file as html and write chapter to chapters.pickle
             download(i, url , title, question__article__slug)

             # Sleep for 20 secs for each problem and 2 minns after every 30 problems
             # if i % 30 == 0:
             #     print(f"Sleeping 120 secs\n")
             #     time.sleep(120)
             # else:
             #     print(f"Sleeping 20 secs\n")
             #     time.sleep(5)

    finally:
        # Close the browser after download
        driver.quit()
    
    try:
        epub_writer.write("Leetcode Questions.epub", "Leetcode Questions", "Anonymous", chapters)
        print(Back.GREEN + "All operations successful")
    except Exception as e:
        print(Back.RED + f"Error making epub {e}")
    


if __name__ == "__main__":
    main()
