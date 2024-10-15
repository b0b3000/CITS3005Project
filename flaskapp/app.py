from flask import Flask, render_template, request, jsonify, redirect, url_for
import json

app = Flask(__name__)

import ontology, build, queries
     
from owlready2 import *
from rdflib import *

ONTO_FILE_PATH = "ont/mac.owl"
JSON_FILE_PATH = "ont/data.json"
RDFXML_FILE_PATH = "ont/rdf_out.xml"

fix = Namespace("http://ifixit.org/mac.owl#")
mac = get_ontology("http://ifixit.org/mac.owl")

ontology.create_ontology(mac, ONTO_FILE_PATH)
mac = get_ontology(ONTO_FILE_PATH).load()
graph, mac = build.parse_data_to_owl(JSON_FILE_PATH, ONTO_FILE_PATH, RDFXML_FILE_PATH, fix, mac)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home', image="static/images/banner.png")

@app.route("/search")
def search():
    searches = queries.get_queries()
    return render_template('search.html', title='Search', searches=searches)

@app.route("/browse")
def browse():
    return render_template('browse.html', title='Browse')


@app.route("/get_query", methods = ['GET', 'POST'])
def get_query():
    data = request.get_json()
    search_id = data['search_id']
    results = queries.run_query(search_id, graph) 
    # redirect to query results page
    return json.dumps(results)