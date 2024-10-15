from rdflib import Graph
query1 = """
            PREFIX ns: <http://ifixit.org/mac.owl#>
                SELECT ?procedure
                WHERE {
                    ?procedure a ns:Procedure .
                    ?procedure ns:has_step ?step .
                }
                GROUP BY ?procedure
                HAVING (COUNT(?step) > 6)
            """
query2 = """
            PREFIX ns: <http://ifixit.org/mac.owl#>
                SELECT ?item
                WHERE {
                    ?item a ns:Item .
                    ?item ns:has_procedure ?procedure .
                }
                GROUP BY ?item
                HAVING (COUNT(?procedure) > 10)
            """
query3 = """
            PREFIX ns: <http://ifixit.org/mac.owl#>
                SELECT DISTINCT ?procedure
                WHERE {
                    ?procedure a ns:Procedure .
                    ?procedure ns:has_toolbox ?toolbox .
                    ?tool ns:in_toolbox ?toolbox .
                    MINUS {
                        ?procedure ns:has_step ?step .
                        ?tool ns:used_in ?step .
                    }
                }
            """
        
query4 = """
            PREFIX ns: <http://ifixit.org/mac.owl#>
                SELECT ?procedure ?step
                WHERE {
                    ?procedure a ns:Procedure .
                    ?procedure ns:has_step ?step .
                    ?step ns:step_description ?text .
                    FILTER(CONTAINS(STR(?text), "care") || CONTAINS(STR(?text), "danger") || CONTAINS(STR(?text), "hazard")) .
                }
            """


def get_queries():
    return [
        {'id': 1, 'name': "All procedures with more than 6 steps"},
        {'id': 2, 'name': "All items that have more than 10 procedures written for them"},
        {'id': 3, 'name': "All procedures that include a tool that is never mentioned in the procedure steps"},
        {'id': 4, 'name': "Potential hazards in the procedure by identifying steps with works like careful and dangerous."}
    ]

def run_query(query_id: int, graph: Graph):
    id = int(query_id)
    current_query = ""
    tuple = False
    if id == 1:
        current_query = query1
    elif id == 2:
        current_query = query2
    elif id == 3:
        current_query = query3
    elif id == 4:
        current_query = query4
        tuple = True
    results = graph.query(current_query)
    result_list = []
    for row in results:
        uri = ""
        if tuple == True:
            procedure = str(row[0]).split("/")[-1].replace("_", " ")
            step = str(row[1]).split("/")[-1].replace("_", " ")
            uri = procedure +  "/" + step
        else: 
            uri = str(row).split("/")[-1].replace("_", " ")[:-4] #Outputs just the part im interested in
        result_list.append(uri)
    return result_list



def run_queries(graph, mac):
    with mac:
        
        
        query4 = """
            PREFIX ns: <http://ifixit.org/mac.owl#>
                SELECT ?procedure ?step
                WHERE {
                    ?procedure a ns:Procedure .
                    ?procedure ns:has_step ?step .
                    ?step ns:step_description ?text .
                    FILTER(CONTAINS(STR(?text), "care") || CONTAINS(STR(?text), "danger") || CONTAINS(STR(?text), "hazard")) .
                }
            """
        result4 = graph.query(query4)

        print("\n\n\nPotential hazards in the procedure by identifying steps with works like careful and dangerous.\n\n\n")
        for row in result4:
            procedure = str(row[0]).split("/")[-1].replace("_", " ")
            step = str(row[1]).split("/")[-1].replace("_", " ")
            print(procedure, step)