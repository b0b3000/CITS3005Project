from flask import Flask, render_template, request, jsonify, redirect, url_for
import json

app = Flask(__name__)

import ontology, build, queries, searches

from process import add_new_procedure, delete_procedure

from owlready2 import *
from rdflib import *

ONTO_FILE_PATH = "ont/mac.owl"
JSON_FILE_PATH = "ont/temp3.json"
RDFXML_FILE_PATH = "ont/rdf_out.xml"

#fix = Namespace("http://ifixit.org/mac.owl#")
mac = get_ontology("http://ifixit.org/mac.owl#")

ontology.create_ontology(mac, ONTO_FILE_PATH)
mac = get_ontology(ONTO_FILE_PATH).load()
graph, mac, consistent, report = build.parse_data_to_owl(JSON_FILE_PATH, ONTO_FILE_PATH, RDFXML_FILE_PATH, mac)
# Configure the upload set


#
#
#
# USE CONSISTENT
#
#
#
#


# Ensure the upload directory exists
if not os.path.exists('uploads/images'):
    os.makedirs('uploads/images')
    
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route("/sparql_queries")
def sparql():
    query_names = list(queries.get_queries())
    print(query_names)
    return render_template('queries.html', title='Search', searches=query_names)

@app.route("/key_searches")
def key_searches():
    return render_template('key_searches.html', title='Search', search_functions=searches.get_search_functions())

@app.route("/search_procedures")
def search_procedures():
    return render_template('search_procedures.html', title='Search', search=searches.get_procedure_search())

@app.route("/procedure")
def procedure():
    # get all relevant information for the procedure
    return render_template('procedure.html', title='Procedure')

@app.route("/user_guide")
def user_guide():
    return render_template('guide.html', title='User Guide')

@app.route("/create", methods = ['GET', 'POST'])
def create():
    return render_template('create.html', title='Create')

@app.route("/consistent", methods = ['GET', 'POST'])
def consistent():
    consistent, report = build.reason_ontology(mac)
    return jsonify({"Consistent" : consistent, "report" : report})


@app.route("/result_viewer", methods=['GET'])
def result_viewer():
    result_uri = request.args.get('data')
    print(f"View URI: {result_uri}")
    if not result_uri:
        return jsonify({"error": "No data provided"}), 400

    # get the procedure information
    procedure_info = searches.get_procedure_info(result_uri, mac)
    if "error" in procedure_info.keys():
        return render_template("result_viewer.html",data={"name": "No procedure found"})
    print(f"View Procedure info: {procedure_info}")
    return render_template("result_viewer.html", data=procedure_info)

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
        return jsonify({"error": "Query not found"}), 404
    if results == ["Query has no results"]:
        return jsonify({"error": "Query has no results"}), 404
    # redirect to query results page
    return jsonify(results), 200

@app.route("/search_results", methods = ['GET', 'POST'])
def search_results():
    data = request.get_json()
    search_func = data['searchFunction']
    search_value = data['searchInput']

    results = searches.run_search(search_func, search_value, graph, mac)
    for result in results:
        print(result)
    if results[0] == "Query not found":
        return jsonify({"error": "Query not found"}), 404
    
    if results[0] == "Query has no results":
        return jsonify({"error": "Query has no results"}), 404
    return jsonify(results), 200

@app.route("/create_procedure", methods = ['GET', 'POST'])
def add_procedure():
    # use pyshacl to validate the procedure add request
    new_procedure_data = request.get_json()
    print(new_procedure_data)
    with mac:
        add_new_procedure(ONTO_FILE_PATH,new_procedure_data, mac)
        graph = default_world.as_rdflib_graph()
        file = open(RDFXML_FILE_PATH, mode="w", encoding='utf-8')  
        file.write(graph.serialize(format='turtle'))
    
    consistent, report = build.reason_ontology(mac)
    if not consistent:
       return jsonify({"Consistent" : consistent, "report" : report})
    # add the procedure to the ontology
    return jsonify("Procedure added"), 200


@app.route("/get_ancestors", methods = ['GET', 'POST'])
def get_ancestors():
    item_name = request.get_json()
    print(f"Item name: {item_name}")
    ancestors = searches.get_ancestors(item_name, mac)
    return jsonify(ancestors), 200

