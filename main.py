from flask import Flask
from flask import request
from flask import Response
import requests
import openai
import os

app = Flask(__name__)

TOKEN = os.environ['TELEGRAM_TOKEN']


def getTheData(text):
    prompt = text
    openai.api_key = os.environ['OPENAI_KEY']
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
              
                "role":
                "system",
                "content":
                "You are a career counselor, offering advice and guidance to users seeking to make informed decisions about their professional lives. Help users explore their interests, skills, and goals, and suggest potential career paths that align with their values and aspirations. Offer practical tips for job searching, networking, and professional development.",
            },
            {
                "role": "user",
                "content": prompt
            },
        ],
        # temperature=0.2,
        # max_tokens=50  # Adjust as needed
    )
    print(response)
    generated_text = response.choices[0].message.content
    return generated_text


def sendMessage(chat_id, out_txt):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {"chat_id": chat_id, "text": out_txt}
    requests.post(url, json=payload)


@app.get("/")
def hi():
    return "Hi There"


@app.post("/")
def index():
    try:
        msg = request.get_json()
        print(msg)
        chat_id = msg['message']['chat']['id']
        txt = msg['message']['text']
        print("text is ", txt)
        generated_text = getTheData(txt)
        print(generated_text)
        sendMessage(chat_id, generated_text)
        return Response('ok', status=200)
    except Exception as e:
        print(e)
        sendMessage(chat_id, "Limit Reached! Please post your question after some time may be after 3min")
        return Response('ok', status=200)


app.run('0.0.0.0', 8080)
