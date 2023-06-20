import warnings
warnings.filterwarnings("ignore")
from arango import ArangoClient
from flask import Flask, render_template, request, jsonify
import pandas as pd
from pyArango.connection import *
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app)


conn1 = Connection(username='root', password='')
client = ArangoClient()
db1 = conn1['summary']
coll = db1['data']

conn2 = Connection(username='root', password='')
client = ArangoClient()
db2 = conn2['CDR_New']
coll = db2['contacts']

@app.route("/summary_of_total", methods=["POST", "GET"])
def summary_of_total():
    conn1 = Connection(username="root", password="")
    db1 = conn1["summary"]
    phone1 = request.form['phone1']
    print(phone1)
    # f = coll.find({'phone1': phone1})
    aql = f'''FOR doc IN data FILTER doc.phone1 == "{phone1}" RETURN doc'''
    queryresult = db1.AQLQuery(aql, rawResults=True)
    df = pd.DataFrame(queryresult, columns=["first_name", "last_name", "city", "address", "company_name", "county", "state", "email", "web", "IMEI"])
    print(df)
    df_dict = df.to_dict(orient='records')
    response = {'data_dict': df_dict, 'phone1': phone1, 'headers': list(df)}
    return jsonify(response)

@app.route("/summary_of_state", methods=["POST", "GET"])
def summary_of_state():
    conn1 = Connection(username="root", password="")
    db1 = conn1["summary"]
    phone1 = request.form['phone1']
    state = request.form['state']
    print(phone1, state)
    # f = coll.find({'phone1': phone1, 'state': state})
    aql = f'''FOR doc IN data FILTER doc.phone1 == "{phone1}" && doc.state == "{state}"RETURN doc'''
    print(aql)
    queryresult = db1.AQLQuery(aql, rawResults=True)
    df = pd.DataFrame(queryresult, columns=["first_name", "last_name", "company_name", "address"])
    print(df)
    df_dict = df.to_dict(orient='records')
    response = {'data_dict': df_dict, 'phone1': phone1, 'state':state, 'headers': list(df)}
    return jsonify(response)

@app.route("/imei_search", methods=["POST", "GET"])
def imei_search():
    conn1 = Connection(username="root", password="")
    db1 = conn1["summary"]
    IMEI = request.form['IMEI']
    print(IMEI)
    # f = coll.find({'IMEI': IMEI})
    aql = f'''FOR doc IN data FILTER doc.IMEI == "{IMEI}" RETURN doc'''
    print(aql)
    queryresult = db1.AQLQuery(aql, rawResults=True)
    df = pd.DataFrame(queryresult, columns=["first_name", "last_name", "city", "address", "company_name", "county", "state", "email", "web", "zip", "phone1", "phone2", "IMEI"])
    print(df)
    df_dict = df.to_dict(orient='records')
    response = {'data_dict': df_dict, 'IMEI': IMEI, 'headers': list(df)}
    return jsonify(response)

@app.route("/single_address", methods=["POST", "GET"])
def single_address():
    conn1 = Connection(username="root", password="")
    db1 = conn1["summary"]
    phone1 = request.form['phone1']
    phone2 = request.form['phone2']
    f = coll.find({'phone1': phone1, 'phone2': phone2})
    aql = f''' FOR doc IN data FILTER doc.phone1 == "{phone1}" OR (doc.phone2 == "{phone2}") RETURN doc'''
    queryresult = db1.AQLQuery(aql, rawResults=True)
    df = pd.DataFrame(queryresult, columns=["address"])
    print(df)
    df_dict = df.to_dict(orient='records')
    response = {'data_dict': df_dict, 'phone1':phone1, 'phone2':phone2, 'headers': list(df)}
    return jsonify(response)

@app.route("/data_search", methods=["POST", "GET"])
def data_address():
    conn2 = Connection(username="root", password="")
    db2 = conn2["CDR_New"]
    party_a = request.form['party_a']
    # f = coll.find({'party_a':party_a})
    aql = f''' FOR doc IN contacts FILTER doc.party_a == "{party_a}" RETURN doc'''
    queryresult = db2.AQLQuery(aql, rawResults=True)
    df = pd.DataFrame(queryresult, columns=["party_a", "party_a_ori", "party_b", "party_b_ori", "call_type", "IMEI", "IMSI", "first_BTS", "last_BTS", "roaming", "provider"])
    print(df)
    df_dict = df.to_dict(orient='records')
    response = {'data_dict': df_dict, 'party_a':party_a, 'headers': list(df)}
    return jsonify(response)

@app.route("/profile_num", methods=["POST","GET"])
def profile_num():
    conn = Connection(username="root", password="")
    db2 = conn2["CDR_New"]
    number = request.form['number']
    print(number)
    aql = f'''FOR doc IN contacts FILTER doc.party_a == "{number}" RETURN DISTINCT doc'''
    queryResult = db2.AQLQuery(aql, rawResults=True)
    df = pd.DataFrame(queryResult, columns=["party_a", "party_a_ori", "party_a", "party_b", "party_b", "call_type", "duration", "IMEI", "IMSI", "service_type", "call_date", "call_time", "call_end", "call_comp", "first_BTS", "last_BTS", "first_CGI", "last_CGI", "roaming", "provider", "source"])
    print(df)
    df_dict = df.to_dict(orient='records')
    response = {'data_dict': df_dict, 'number': number, 'headers': list(df)}
    return jsonify(response)

@app.route("/search", methods=["POST","GET"])
def search():
    conn = Connection(username="root", password="")
    db2 = conn2["CDR_New"]
    number = request.form['number']
    print(number)
    aql = f'''FOR doc IN contacts FILTER doc.party_a == "{number}" RETURN DISTINCT doc'''
    queryResult = db2.AQLQuery(aql, rawResults=True)
    df = pd.DataFrame(queryResult, columns=["party_a", "party_a_ori", "party_a", "party_b", "party_b", "call_type", "duration", "IMEI", "IMSI", "service_type", "call_date", "call_time", "call_end", "call_comp", "first_BTS", "last_BTS", "first_CGI", "last_CGI", "roaming", "provider", "source"])
    print(df)
    df_dict = df.to_dict(orient='records')
    response = {'data_dict': df_dict, 'number': number, 'headers': list(df)}
    return jsonify(response)

@app.route("/call_id_search", methods=["POST","GET"])
def call_id_search():
    conn = Connection(username="root", password="")
    db2 = conn2["CDR_New"]
    number = request.form['number']
    print(number)
    aql = f'''FOR doc IN contacts FILTER doc.party_a == "{number}" RETURN DISTINCT doc'''
    queryResult = db2.AQLQuery(aql, rawResults=True)
    df = pd.DataFrame(queryResult, columns=["party_a", "party_b", "call_type", "duration", "call_date", "call_time", "call_end", "call_comp", "roaming", "provider", "source"])
    print(df)
    df_dict = df.to_dict(orient='records')
    response = {'data_dict': df_dict, 'number': number, 'headers': list(df)}
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
