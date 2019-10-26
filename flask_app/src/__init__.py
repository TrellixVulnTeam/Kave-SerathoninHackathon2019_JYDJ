from flask import Flask, render_template, make_response, request, redirect
import pandas as pd
import numpy as np
import time
app = Flask(__name__)
from os.path import join, dirname, realpath
import pickle 
import os
from shutil import copyfile

copyfile("C:/Users/yemre/Desktop/flask_app/src/static/uploads/safe_zone/db.sqlite3", "C:/Users/yemre/Desktop/flask_app/src/db.sqlite3")

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
    data = pd.read_excel(UPLOADS_PATH+"BIST100.xlsx")
    data = data[['Close']]
    clf = pickle.load(open(UPLOADS_PATH+'model-BIST100.pkl', 'rb'))
    # Önümüzdeki 7 Gün için Tahmin yapma
    base = list(data.Close.values[-7:])
    for i in range(7):
        base.append(clf.predict(np.array([base[i:]]))[0].round(2))
    sample_Data = data.Close.values[-28:]
    predict_data = base[-7:]
    percantege_data = (((sample_Data[-2] - predict_data[-7])/ sample_Data[-2])*100).round(3)
    return render_template('index.html', sample_Data = sample_Data, predict_data=predict_data,percantege_data=percantege_data,symbol_name="BIST100",sybmol_kap_summary=sybmol_kap_summary,sybmol_kap_general=sybmol_kap_general)

sybmol_kap_summary = """
ASELSAN ile Savunma Sanayii Başkanlığı arasında 29.12.2017 tarihinde imzalanmış olan kısa menzilli/alçak irtifa hava savunma sistemi sözleşmesine ait 91.550.073 Euro + 1.094.428.811 TL tutarındaki opsiyon paketi sözleşme kapsamına dahil edilmiştir. Söz konusu opsiyona ait teslimatlar 2021-2023 yıllarında gerçekleştirilecektir. Bu açıklama Savunma Sanayii Başkanlığının Şirketimize 24.10.2019 tarihinde ulaşan iznine istinaden yapılmıştır.
"""

sybmol_kap_general= """
Şirketimiz tarafından 2019 yılının ilk dokuz ayında 1.134 yeni işe alım gerçekleştirilmiştir. Eylül ayı itibariyle 10 Milyar ABD Doları sipariş ile tarihi sipariş rekoru kırmış olan Şirketimiz, aldığı bu siparişler kapsamında mühendis ve teknisyen kadrosunu genişletmektedir. İşe yeni başlayan çalışanların %70'ini mühendis kadrosu; %25'ini de teknisyen kadrosu oluşturmaktadır. Bu çalışanların 26 adedi doktora, 144 adedi ise yüksek lisans mezunudur. Yurt dışındaki yetişmiş insan kaynağının ülkemize geri kazanımında ilk tercih edilen kurumların başında gelen ASELSAN, bu özelliğini 2019 yılında da sürdürmüştür.
"""


@app.route('/detail_view/<symbol_name>')
def detail_analytics(symbol_name):
    data = pd.read_excel(UPLOADS_PATH+symbol_name+".xlsx")
    data = data[['Close']]
    clf = pickle.load(open(UPLOADS_PATH+'model-'+symbol_name+'.pkl', 'rb'))
    # Önümüzdeki 7 Gün için Tahmin yapma
    base = list(data.Close.values[-7:])
    for i in range(7):
        base.append(clf.predict(np.array([base[i:]]))[0].round(2))
    sample_Data = data.Close.values[-28:]
    predict_data = base[-7:]
    percantege_data = (((predict_data[-7] - sample_Data[-2])/ predict_data[-7])*100).round(3)
    return render_template('index.html', sample_Data = sample_Data, predict_data=predict_data,percantege_data=percantege_data,symbol_name=symbol_name,sybmol_kap_summary=sybmol_kap_summary,sybmol_kap_general=sybmol_kap_general)


@app.route('/listele')
def list_page()->'html':
    return render_template('list.html')

@app.route('/chat-bot')
def chat_bot()->'html':
    text = request.args.get('query')
    response = chatbot.get_response(text)
    return {"result":{"fulfillment":{"speech":response.text}}}
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=37000)