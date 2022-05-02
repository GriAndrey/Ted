from flask import Flask, render_template, request
from find import find_usage
import sqlite3
import random
import re

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def main():
    flag = 0
    # Вывод информации в зависимости от переданных данных
    if request.method == 'POST':
        if request.form['title'] == "":
            return render_template('index.html')

        req = request.form['title'].lower()
        CONNECTION = sqlite3.connect('subtitles.db')
        finder = find_usage(req, CONNECTION)
        CONNECTION.close()

        # нахождение необходимых слов
        goodFinder = []
        for i in finder:
            if re.search(rf'\b{req}\b', i[2].lower()) == None:
                continue
            goodFinder.append(i)
        if len(goodFinder) == 0:
            flag = 1
            return render_template('index.html', flag=flag)
        goodFinder = random.sample(goodFinder, 1)

        try:
            return render_template('index.html', finder=goodFinder, req=req)
        except:
            return render_template('index.html')

    else:
        return render_template('index.html')


app.run()