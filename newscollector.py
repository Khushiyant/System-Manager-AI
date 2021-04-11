import os
import datetime
import requests
from bs4 import BeautifulSoup


'''
Get to daily current news webpage and open existing news page.
url - "https://currentaffairs.studyiq.com/daily/"
date - today's date

If today's date isn't present then, it used recurssion to find exiting page
'''
def scrappedData(url, date):
    new_url = url + date.strftime("%d-%m-%Y")
    r = requests.get(new_url)
    htmlContent = r.content     # Get the html parsed content obtained by new_url
    soup = BeautifulSoup(htmlContent, "html.parser")
    if len(soup.find_all(class_="list-text")) == 0:         # Check if page exists or not
        scrappedData(url, date - datetime.timedelta(1))
    else:
        for links in soup.find_all(class_="list-text"):
            OneLiner(links.find("a").get("href"), links.find(
                "a").get_text(), date.strftime("%d-%m-%Y"))


'''
Next step to ladder then, Move to page and extract information from each topic including:
1. Tag - present in "posted-on" div
2. Headline - present in "page-content" div

topic - current topic url
filename - name of topic
date - existing date of page

'''
def OneLiner(topic, filename, date):
    r = requests.get(topic)
    htmlContent = r.content
    soup = BeautifulSoup(htmlContent, "html.parser")
    tag = soup.find(class_="posted-on").find("a").get_text()
    oneline = soup.find_all("div", class_="page-content")       # -------> UNDER CONSTRUCTION
    for a in oneline:
        appendOneliner(tag, a.find_all("p")[1].get_text(), filename, date)
        # print(a.find_all("p")[1].get_text())


'''
Simply appending of extracted of data
tag - category of topic
content - headline
filename - name of the topic
date - date of existing page

Based on recursion for check filename existance
'''
def appendOneliner(tag, content, filename, date):
    if os.path.isdir("StudyIQ/"):
        if os.path.isdir("StudyIQ/" + date):
            if os.path.isdir("StudyIQ/" + date + "/" + tag):
                with open("StudyIQ/" + date + "/"+tag + "/" + filename+".txt", "w+") as f:  #Opening the file in write mode
                    f.write(content)            # Write the EXtracted content
                f.close()
            else:
                os.mkdir("StudyIQ/" + date + "/" + tag)
                appendOneliner(tag, content, filename, date)
        else:
            os.mkdir("StudyIQ/"+date)
            appendOneliner(tag, content, filename, date)
    else:
        os.mkdir("StudyIQ/")
        appendOneliner(tag, content, filename, date)


'''
Driving Main Section/Function
'''
if __name__ == "__main__":
    url = "https://currentaffairs.studyiq.com/daily/"
    currentDate = datetime.datetime.today().date()
    scrappedData(url, currentDate)
