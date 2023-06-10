import warnings
warnings.filterwarnings("ignore")
from arango import ArangoClient
from flask import Flask, render_template, request, jsonify
import pandas as pd
from pyArango.connection import *
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app)
client = ArangoClient()
db = client.db('summary')
coll = db.collection('data')

@app.route("/summary_of_total", methods=["POST", "GET"])
def summary_of_total():
    conn=Connection(username='root',password='')
    db=conn['summary']
    phone1 = request.form['phone1']
    print(phone1)
    f=coll.find({'phone1':phone1})
    aql = f'''FOR doc IN data FILTER doc.phone1 == "{phone1}" RETURN doc'''
    queryresult = db.AQLQuery(aql, rawResults=True)
    df = pd.DataFrame(queryresult, columns=["first_name", "last_name", "city", "address", "company_name", "county", "state", "email", "web", "IMEI"])
    print(df)
    df_dict = df.to_dict(orient='records')
    # print(df_dict)
    response = {'data_dict': df_dict, 'phone1': phone1, 'headers': list(df)}
    return jsonify(response)


@app.route("/summary_of_state", methods=["POST", "GET"])
def summary_of_state():
    conn=Connection(username='root',password='')
    db=conn['summary']
    phone1 = request.form['phone1']
    state = request.form['state']
    print(phone1, state)
    f1=coll.find({'phone1':phone1, 'state':state})
    aql = f'''FOR doc IN data FILTER doc.phone1 == "{phone1}" && doc.state == "{state}"RETURN doc'''
    print(aql)
    queryresult = db.AQLQuery(aql, rawResults=True)
    df = pd.DataFrame(queryresult, columns=["first_name", "last_name", "company_name", "address"])
    print(df)
    df_dict = df.to_dict(orient='records')
    response = {'data_dict': df_dict, 'phone1': phone1, 'state':state, 'headers': list(df)}
    return jsonify(response)

@app.route("/imei_search", methods=["POST", "GET"])
def imei_search():
    conn=Connection(username='root',password='')
    db=conn['summary']
    IMEI = request.form['IMEI']
    print(IMEI)
    f1=coll.find({'IMEI':IMEI})
    aql = f'''FOR doc IN data FILTER doc.IMEI == "{IMEI}" RETURN doc'''
    print(aql)
    queryresult = db.AQLQuery(aql, rawResults=True)
    df = pd.DataFrame(queryresult, columns=["first_name", "last_name", "city", "address", "company_name", "county", "state", "email", "web", "zip", "phone1", "phone2", "IMEI"])
    print(df)
    df_dict = df.to_dict(orient='records')
    response = {'data_dict': df_dict, 'IMEI': IMEI, 'headers': list(df)}
    return jsonify(response)

@app.route("/single_address", methods=["POST", "GET"])
def single_address():
    conn=Connection(username='root',password='')
    db=conn['summary']
    phone1 = request.form['phone1']
    phone2 = request.form['phone2']
    f1=coll.find({'phone1':phone1, 'phone2':phone2})
    aql = f''' FOR doc IN data FILTER doc.phone1 == "{phone1}" OR (doc.phone2 == "{phone2}") RETURN doc'''
    queryresult = db.AQLQuery(aql, rawResults=True)
    df = pd.DataFrame(queryresult, columns=["address"])
    print(df)
    df_dict = df.to_dict(orient='records')
    response = {'data_dict': df_dict, 'phone1':phone1, 'phone2':phone2, 'headers': list(df)}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)


    