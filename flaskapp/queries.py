from rdflib import Graph


query_dict = {
    "All procedures with more than 6 steps": """
            PREFIX ns: <http://ifixit.org/mac.owl#>
                SELECT ?procedure
                WHERE {
                    ?procedure a ns:Procedure .
                    ?procedure ns:has_step ?step .
                }
                GROUP BY ?procedure
                HAVING (COUNT(?step) > 6)
            """,
    "All items that have more than 10 procedures written for them ": """PREFIX ns: <http://ifixit.org/mac.owl#>
                SELECT ?item
                WHERE {
                    ?item a ns:Item .
                    ?item ns:has_procedure ?procedure .
                }
                GROUP BY ?item
                HAVING (COUNT(?procedure) > 10)""",
    "All procedures that include a tool that is never mentioned in the procedure steps": """PREFIX ns: <http://ifixit.org/mac.owl#>
                SELECT DISTINCT ?procedure
                WHERE {
                    ?procedure a ns:Procedure .
                    ?procedure ns:has_toolbox ?toolbox .
                    ?tool ns:in_toolbox ?toolbox .
                    MINUS {
                        ?procedure ns:has_step ?step .
                        ?tool ns:used_in ?step .
                    }
                }""",
    "All procedures with potential hazards, with steps containing words like 'careful' and 'dangerous'.": """PREFIX ns: <http://ifixit.org/mac.owl#>
                SELECT ?procedure ?step
                WHERE {
                    ?procedure a ns:Procedure .
                    ?procedure ns:has_step ?step .
                    ?step ns:step_description ?text .
                    FILTER(CONTAINS(STR(?text), "care") || CONTAINS(STR(?text), "danger") || CONTAINS(STR(?text), "hazard"))) .
                }
            """,
    """ Retrieve all items that are part of another item """: """PREFIX ns: <http://ifixit.org/mac.owl#> 
                    SELECT ?item1
                    WHERE {
                        ?item1 a ns:Item .
                        ?item1 ns:part_of ?item2 .
            }
    """,
    """ Retrieve All Images Associated with Steps""": """\
        PREFIX ns: <http://ifixit.org/mac.owl#>
        SELECT ?step ?image
        WHERE {
            ?step a ns:Step .
            ?step ns:has_image ?image .
        }
""",
}


def get_queries():
    return query_dict.keys()


def add_query(query_name: str, query_value: str):
    query_dict.update(
        {query_name: "PREFIX ns: <http://ifixit.org/mac.owl#>" + query_value}
    )


def run_query(query_name: str, graph: Graph):
    current_query = query_dict.get(query_name)
    print(current_query)
    if current_query == None:
        return ["Query not found"]
    results_list = []
    try:
        results = graph.query(current_query)
    except:
        return ["Query has no results"]
    for row in results:
        uri = ""
        for item in row:
            item = str(item)
            uri += item + " "
        results_list.append(uri)
    return results_list
