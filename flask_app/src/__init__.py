from flask import Flask, render_template, make_response, request, redirect
import pandas as pd
import time
app = Flask(__name__)
from os.path import join, dirname, realpath

UPLOADS_PATH = join(dirname(realpath(__file__)), 'static/uploads/')
################ Chatter BOT ###############

def get_deger(sembol):
    data = pd.read_excel(UPLOADS_PATH+sembol+'.xlsx')
    data = data[['Close']]
    deger = data.iloc[-1].values[0]
    return str(deger)
def get_Excel(sembol="KCHOL"):
    data = pd.read_excel(UPLOADS_PATH+sembol+'.xlsx')
    data = data[['Close']]
    return (((data.iloc[-1].values - data.iloc[-7].values) / data.iloc[-1].values)[0]*100).round(3),(((data.iloc[-1].values - data.iloc[-15].values) / data.iloc[-1].values)[0]*100).round(3),(((data.iloc[-1].values - data.iloc[-30].values) / data.iloc[-1].values)[0]*100).round(3)

from chatterbot import ChatBot

# Create a new chat bot named Charlie
chatbot = ChatBot(
    'Charlie',
    trainer='chatterbot.trainers.ListTrainer'
)

@app.route('/')
def entry_page()->'html':
    sample_Data = [16.87,16.91,17.87,17.59,17.67,18.16,18.17]
    predict_data = [18.12]
    return render_template('index.html', sample_Data = sample_Data, predict_data=predict_data )
@app.route('/listele')
def list_page()->'html':
    sample_Data = [16.87,16.91,17.87,17.59,17.67,18.16,18.17]
    predict_data = [18.12]
    return render_template('list.html', sample_Data = sample_Data, predict_data=predict_data )

@app.route('/chat-bot')
def chat_bot()->'html':
    text = request.args.get('query')
    response = chatbot.get_response(text)
    print(type(response))
    return {"result":{"fulfillment":{"speech":response.text}}}
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=37000)