from selenium import webdriver
import time
from bs4 import BeautifulSoup
import xlsxwriter
from tkinter import *
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import re
import pandas as pd
import xlwt



text_file = open("output.txt", "w")
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) 
file = open('sample.txt')
lines = file.readlines()


"""
elementID = browser.find_element("id",'username')
elementID.send_keys(username)

elementID = browser.find_element("id",'password')
elementID.send_keys(password)
#elementID.submit()
browser.find_element(By.XPATH,"//*[@type='submit']").click();"""
browser.get('https://www.linkedin.com/login')
browser.find_element('id','username').send_keys('mail') #Enter username of linkedin account here
browser.find_element('id','password').send_keys('pass')  #Enter Password of linkedin account here
browser.find_element(By.XPATH,"//*[@type='submit']").click();

df = pd.read_csv("link.csv")
for i in range(len(df)):
    link = df["links"][i]
    browser.get(link)

    SCROLL_PAUSE_TIME = 5

    #Reading Link 
    # Get scroll height
    last_height = browser.execute_script("return document.body.scrollHeight")
    print(link)
    for i in range(3):
        # Scroll down to bottom
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    src = browser.page_source
    soup = BeautifulSoup(src, 'lxml')



    """Finding Name""" """
    name_div = soup.find('div', {'class': 'pv-text-details__left-panel'})


    name_loc = name_div.find_all('div')

    name = name_loc[0].find('h1').get_text().strip()
    print(name)
    """





    #Findingg all sections
    exp_sec = soup.find_all('li', {'class': 'artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column pvs-list--ignore-first-item-top-padding'})
    print(len(exp_sec))
    with open('li.txt',  "w", encoding="utf-8") as file:
        # Write the number and unit for each match into the file
        for match in exp_sec:
            file.write(str(exp_sec))

    with open('li.txt', 'r', encoding='utf-8') as file:
        file_contents = file.read()
    # Initialisation du drapeau pour marquer le début de la section à extraire
    start_flag = False
    extracted_content = ""
    count = 0

    # Parcourir le contenu du fichier ligne par ligne
    for line in file_contents.splitlines():
        # Chercher la première occurrence de "yr" ou "yrs" dans la ligne courante
        if  (("yr" in line) or ("yrs" in line)):
            extracted_content += line + '\n'
            start_flag = True
            count += 1
            # Arrêter le parcours si 20 occurrences sont trouvées
            if count >= 4:
                break

        # Ajouter la ligne courante à la section extraite si le drapeau est activé
        elif start_flag:
            extracted_content += line + '\n'

 


    with open('parse.txt',  "w", encoding="utf-8") as file:
        file.write(str(extracted_content))

    soup = BeautifulSoup(extracted_content, 'html.parser')

    # Find the span tag with the experience information using a regular expression
    experience_span = soup.find_all('span', string=re.compile(r'\d+ (?:yr|mos)'))

#print((exp_sec[1]).get_text(strip=True))
    # Sample text containing the words "yo" and "mos"
    sample_text = extracted_content

    # Regular expression to find the numbers before "yo" or "mos"
    pattern = r'(\d+)\s+yr'

    # Find all occurrences of the pattern in the text
    matches = re.findall(pattern, sample_text)

    # Print the number before "yo" or "mos" for each match
    years_at_company_list = []
    other_exp_list = []

    import csv

    header = ['years_at_company_list','other_exp_list']
    data = []


    with open('countries.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)

        # write the data
        writer.writerow(data)
    print(matches)
    for match in range(len(matches)):
        if(match%2==0):
            number = matches[match]
            years_at_company_list.append(number)
            data.append(years_at_company_list[0])
        if(match%2!=0):
            number = matches[match]
            other_exp_list.append(number)
            data.append(other_exp_list[0:])
            print(f"Experience: {number}")
       
    with open('resultat.csv', 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerow(data)
    
