import requests, json
import random
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText

load_dotenv()

token = os.getenv('TOKEN')
databaseId = os.getenv('DATABASEID')

headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def read_db(dbId, headers):
    url = f"https://api.notion.com/v1/databases/{dbId}/query"
	
    res = requests.request("POST", url, headers=headers)
	
    if res.status_code != 200:
        print(f'Response Status: {res.status_code}')
        print(res.url)
    else:
        return res.json()

	
def choose_random_word(data):
    definition = ""
    lenght = len(data["results"]) - 1
    random_index = random.randint(0, lenght)
    word = data["results"][random_index]["properties"]["Mot"]["title"][0]["plain_text"]
    definition_props = data["results"][random_index]["properties"]["Definition"]["rich_text"]

    for prop in definition_props:
        definition += prop["plain_text"]
    mot_du_jour = f"<h2>Le mot du jour est</h2> \n<strong>{word}</strong> : {definition}"

    return mot_du_jour

def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body, 'html')
    msg['subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    

    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(sender, password)
    smtp_server.sendmail(sender, recipients, msg.as_string())
    smtp_server.quit()

data = read_db(databaseId, headers)
word = choose_random_word(data)
recipients = [os.getenv("ADDRESS1"), os.getenv("ADDRESS2")]

send_email("Le mot du jour", word, os.getenv("SENDER"), recipients, os.getenv("MAILAPPPASS") )
