from flask import Flask, render_template, request, jsonify, redirect, url_for
import json

app = Flask(__name__)

import ontology, build, queries, searches

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
    return render_template('index.html', title='Home')

@app.route("/sparql_queries")
def sparql():
    query_names = list(queries.get_queries())
    print(query_names)
    return render_template('queries.html', title='Search', searches=query_names)

@app.route("/search")
def search():
    return render_template('search.html', title='Search', search_functions=["Search by procedure", "Search by item", "Search by part", "Search by tool"])

@app.route("/procedure")
def procedure():
    # get all relevant information for the procedure
    return render_template('procedure.html', title='Procedure')

@app.route("/user_guide")
def user_guide():
    return render_template('guide.html', title='User Guide')

@app.route("/create")
def edit_graph():
    return render_template('create.html', title='Create')

@app.route("/add_query", methods = ['POST'])
def add_query():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid data"}), 400
    print(data)
    query_name = data['name']
    query_value = data['value']
    queries.add_query(query_name, query_value)
    # redirect to query results page
    

@app.route("/get_query", methods = ['GET', 'POST'])
def run_query():
    data = request.get_json()
    query_key = data['search_id']
    results = queries.run_query(query_key, graph) 
    if results == ["Query not found"]:
        return jsonify({"error": "Query not found"}), 400
    if results == ["Query has no results"]:
        return jsonify({"error": "Query has no results"}), 400
    # redirect to query results page
    return jsonify(results), 200

@app.route("/search_results", methods = ['GET', 'POST'])
def search_results():
    data = request.get_json()
    search_type = data['searchFunction']
    search_value = data['searchInput']

    results = searches.run_search(search_type, search_value, graph)
    return jsonify(results), 200

@app.route("/create_procedure", methods = ['GET', 'POST'])
def add_procedure():
    # use pyshacl to validate the procedure add request
    new_procedure_data = request.get_json()
    print(new_procedure_data)

    
    # add the procedure to the ontology

    return jsonify("Procedure added"), 200

