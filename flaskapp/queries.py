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
    if id == 1:
        print("Returning query 1")
        result1 = graph.query(query1)
        results = []
        for row in result1:
            procedure_title = str(row).split("/")[-1].replace("_", " ")[:-4] #Outputs just the part im interested in
            results.append(procedure_title)
        return results
    elif id == 2:
        return graph.query(query2)
    elif id == 3:
        return graph.query(query3)
    elif id == 4:
        return graph.query(query4)
    return None
