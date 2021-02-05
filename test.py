import json
with open("websites.json") as wb:
    website = json.load(wb)
for i in website['websites']:
    if i['website_name']=='youtube':
        print(i['URL'])
