from flask import Flask, render_template, request, make_response, g
from redis import Redis
from prometheus_flask_exporter import PrometheusMetrics
import os
import socket
import random
import json

category_1 = os.getenv('CATEGORY_1', "BEST MOTION PICTURE")
option_11 = os.getenv('OPTION_11', "Jojo Rabbit")
option_12 = os.getenv('OPTION_12', "Little Women")
option_13 = os.getenv('OPTION_13', "Parasite")
option_14 = os.getenv('OPTION_14', "Marriage Story")
option_15 = os.getenv('OPTION_15', "Joker")
category_2 = os.getenv('CATEGORY_2', "BEST ADAPTED SCREENPLAY")
option_21 = os.getenv('OPTION_21', "Jojo Rabbit")
option_22 = os.getenv('OPTION_22', "Joker")
option_23 = os.getenv('OPTION_23', "Little Women")
option_24 = os.getenv('OPTION_24', "The two popes")
option_25 = os.getenv('OPTION_25', "The Irishman")
category_3 = os.getenv('CATEGORY_3', "BEST ORIGINAL SCREENPLAY")
option_31 = os.getenv('OPTION_31', "Knives Out")
option_32 = os.getenv('OPTION_32', "Parasite")
option_33 = os.getenv('OPTION_33', "The Lighthouse")
option_34 = os.getenv('OPTION_34', "Marriage Story")
option_35 = os.getenv('OPTION_35', "1917")
category_4 = os.getenv('CATEGORY_4', "BEST LEADING ACTOR")
option_41 = os.getenv('OPTION_41', "Al Pacino")
option_42 = os.getenv('OPTION_42', "Joe Pesci")
option_43 = os.getenv('OPTION_43', "Brad Pitt")
option_44 = os.getenv('OPTION_44', "Tom Hanks")
option_45 = os.getenv('OPTION_45', "Anthony Hopkins")
category_5 = os.getenv('CATEGORY_5', "BEST LEADING ACTRESS")
option_51 = os.getenv('OPTION_51', "Scarlet Johansson")
option_52 = os.getenv('OPTION_52', "Saoirse Ronan")
option_53 = os.getenv('OPTION_53', "Charlize Theron")
option_54 = os.getenv('OPTION_54', "Renee Zellweger")
option_55 = os.getenv('OPTION_55', "Cynthia Erivo")
category_6 = os.getenv('CATEGORY_6', "BEST DIRECTOR")
option_61 = os.getenv('OPTION_61', "Martin Scorsese")
option_62 = os.getenv('OPTION_62', "Todd Phillips")
option_63 = os.getenv('OPTION_63', "Sam Mendes")
option_64 = os.getenv('OPTION_64', "Quentin Tarantino")
option_65 = os.getenv('OPTION_65', "Bong Joon Ho")
hostname = socket.gethostname()

app = Flask(__name__)
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Application info', version='1.0')

def get_redis():
    if not hasattr(g, 'redis'):
        g.redis = Redis(host="redis", db=0, socket_timeout=5)
    return g.redis

@app.route("/", methods=['POST','GET'])
def hello():
    voter_id = request.cookies.get('voter_id')
    if not voter_id:
        voter_id = hex(random.getrandbits(64))[2:-1]

    voteA = None
    voteB = None
    voteC = None
    voteD = None
    voteE = None
    voteF = None

    if request.method == 'POST':
        redis = get_redis()
        voteA = request.form['categoryA']
        voteB = request.form['categoryB']
        voteC = request.form['categoryC']
        voteD = request.form['categoryD']
        voteE = request.form['categoryE']
        voteF = request.form['categoryF']
        data = json.dumps({'voter_id': voter_id, 'voteA': voteA, 'voteB': voteB, 'voteC': voteC, 'voteD': voteD, 'voteE':voteE,'voteF': voteF})
        redis.rpush('votes', data)
        print("pushed data to redis queue")

    resp = make_response(render_template(
        'index.html',
        category_1=category_1,
        category_2=category_2,
        category_3=category_3,
        category_4=category_4,
        category_5=category_5,
        category_6=category_6,
        option_11=option_11,
        option_12=option_12,
        option_13=option_13,
        option_14=option_14,
        option_15=option_15,
        option_21=option_21,
        option_22=option_22,
        option_23=option_23,
        option_24=option_24,
        option_25=option_25,
        option_31=option_31,
        option_32=option_32,
        option_33=option_33,
        option_34=option_34,
        option_35=option_35,
        option_41=option_41,
        option_42=option_42,
        option_43=option_43,
        option_44=option_44,
        option_45=option_45,
        option_51=option_51,
        option_52=option_52,
        option_53=option_53,
        option_54=option_54,
        option_55=option_55,
        option_61=option_61,
        option_62=option_62,
        option_63=option_63,
        option_64=option_64,
        option_65=option_65,
        hostname=hostname
    ))
    resp.set_cookie('voter_id', voter_id)
    return resp


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
