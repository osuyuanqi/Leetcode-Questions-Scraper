This project was mainly based on [Bishalsarang](https://github.com/Bishalsarang/Leetcode-Questions-Scraper), [LeetCode API](https://leetcode.com/api/problems/algorithms/)

What I did? just main.py

- find out the specific topics and output them into out.html. e.g. If you want to download the Google interview topics, let's say 2,3,4. You may follow the following steps:
  - 1. delete the out.html
  - 2. edit the track.conf as 0
  - 3. in the main.py, search the keyword 'target_topic =[1,2,3]' and change it to 'target_topic =[2,3,4]'
- fixed the deprecated usage in Selenium Webdriver 
- add method for Mac users
