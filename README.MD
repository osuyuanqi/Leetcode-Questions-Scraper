This project was mainly based on [Bishalsarang](https://github.com/Bishalsarang/Leetcode-Questions-Scraper), [LeetCode API](https://leetcode.com/api/problems/algorithms/)

What I did? adjust main.py to personal needs

- find out the specific topics and output them into out.html. e.g. If you want to download the Google interview topics, let's say 2,3,4. You may follow the following steps:
  - 1. delete the out.html
  - 2. edit the track.conf as 0
  - 3. in the main.py, search the keyword 'target_topic =[1,2,3]' and change it to 'target_topic =[2,3,4]'
- fixed the deprecated usage in [Selenium](https://medium.com/@kikigulab/how-to-automate-opening-and-login-to-websites-with-python-6aeaf1f6ae98) Webdriver. BTW, I've tried autologin and download every but failed. Personally, I think it's leetcode used another web framework hiden their content. e.g. \<div>, we can check it from the HTML source code. 
- add method for Mac users. Any voice is welcome. yuanqingxiao@outlook.com
