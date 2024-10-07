def run_queries(graph, mac):
    with mac:
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
        result1 = graph.query(query1)
        print(result1)

        print("\n\n\nAll procedures with more than 6 steps\n\n\n")

        for row in result1:
            procedure_title = str(row).split("/")[-1].replace("_", " ")[:-4] #Outputs just the part im interested in
            print(procedure_title)

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
        result2 = graph.query(query2)

        print("\n\n\nall items that have more than 10 procedures written for them\n\n\n")

        for row in result2:
            item = str(row).split("/")[-1].replace("_", " ")[:-4]
            print(item)
        
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
        result3 = graph.query(query3)

        print("\n\n\nAll procedures that include a tool that is never mentioned in the procedure steps\n\n\n")
        for row in result3:
            item = str(row).split("/")[-1].replace("_", " ")[:-4]
            print(item)
        
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

