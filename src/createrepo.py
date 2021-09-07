#!E:/PythonAutomation/venv/Scripts/python
import os
from getpass import getpass

from selenium import webdriver
import time
from config import USERNAME, GITHUB_PROFILE, CHROME_DRIVER_PATH
import sys
import pyperclip

try:
    PASSWORD = getpass("Enter Password for " + USERNAME + ":")
except:
    print('Please provide github password.')
    sys.exit()

cwd = os.getcwd()

try:
    repo_name = sys.argv[1]
    # repo_name = input("Please enter repo name: ")
except:
    print('Please provide repo name.')
    sys.exit()

create_virtual_env = input("Do you want to create python virtual env? 1 for YES. Any other key for NO\n")
if create_virtual_env == "1":
    try:
        print('Virtual env is creating....\n')
        os.chdir(cwd)
        os.system("python -m venv venv")
        print('Virtual env created....\n')
    except:
        print('Error occurred while creating virtual env.\n')
        ok_continue = input("Do you want to? 1 for YES. Any other key for NO\n")

        if ok_continue != "1":
            sys.exit()
else:
    print('Virtual env creation skipped.\n')
try:
    visibility = sys.argv[2]
except:
    visibility = 'public'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--log-level=1')

browser = webdriver.Chrome(
    executable_path=CHROME_DRIVER_PATH, options=chrome_options)

browser.get("https://github.com/login")

login_field = browser.find_element_by_name('login')
login_field.send_keys(USERNAME)

password_field = browser.find_element_by_name('password')
password_field.send_keys(PASSWORD)

login_field.submit()

browser.get('https://github.com/new')

repository_name = browser.find_element_by_name('repository[name]')
repository_name.send_keys(repo_name)

time.sleep(1)

visibility_radio_input = browser.find_element_by_xpath(
    f'//input[@name="repository[visibility]"][@value="{visibility}"]')
visibility_radio_input.click()

repository_name.submit()

try:
    content = browser.find_element_by_xpath(
        '//clipboard-copy[@for="empty-setup-push-repo-echo"]')
    content.click()
    time.sleep(1)

    print('****Repository created successfully****', end="\n\n")

    do_push = input('Do you want to commit and push all files? 1 for YES, any other key for NO.\n')

    if do_push == "1":
        os.chdir(cwd)
        os.system("git init")
        os.system("git add .")
        os.system('git commit -m "Initial commit"')
        os.system(f"git remote add origin {GITHUB_PROFILE}/{repo_name}.git")
        os.system("git branch -M main")
        os.system("git push -u origin main")

        print('****GITHUB Commit and push successful***', end="\n\n")

    # print(pyperclip.paste())
    print(f"git remote add origin {GITHUB_PROFILE}/{repo_name}.git")
    print("git branch -M main")
    print("git push -u origin main")

except:
    print('Repository cannot be created. (Confirm the repo name is unique)')
