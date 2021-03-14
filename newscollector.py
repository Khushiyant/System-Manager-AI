import os
import datetime
import requests
from bs4 import BeautifulSoup
import urllib.request


def scrappedData(url, date):

    new_url = url + date.strftime("%d-%m-%Y")
    r = requests.get(new_url)
    htmlContent = r.content
    soup = BeautifulSoup(htmlContent, "html.parser")
    if len(soup.find_all(class_="list-text")) == 0:
        scrappedData(url, date - datetime.timedelta(1))
    else:
        for links in soup.find_all(class_="list-text"):
            OneLiner(
                links.find("a").get("href"),
                links.find("a").get_text(),
                date.strftime("%d-%m-%Y")
            )


def OneLiner(topic, filename, date):

    r = requests.get(topic)
    htmlContent = r.content
    soup = BeautifulSoup(htmlContent, "html.parser")
    tag = soup.find(class_="posted-on").find("a").get_text()
    oneline = soup.find_all("div", class_="title--buttons")
    for a in oneline:
        appendOneliner(tag, a.find('a').get('href'), filename, date)


def appendOneliner(tag, file_url, filename, date):

    if os.path.isdir("StudyIQ"):
        if os.path.isdir("StudyIQ/" + date):
            if os.path.isdir("StudyIQ/" + date + "/" + tag):
                r = urllib.request.urlopen(file_url)
                with open("StudyIQ/"+date + "/" + tag+"/" + filename+".pdf", 'wb') as f:
                    f.write(r.read())
                f.close()
            else:
                os.mkdir("StudyIQ/" + date + "/" + tag)
                appendOneliner(tag, file_url, filename, date)
        else:
            os.mkdir("StudyIQ/" + date)
            appendOneliner(tag, file_url, filename, date)
    else:
        os.mkdir("StudyIQ")
        appendOneliner(tag, file_url, filename, date)
