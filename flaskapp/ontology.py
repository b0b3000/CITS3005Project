from owlready2 import *
from rdflib import *

fix = Namespace("http://ifixit.org/mac.owl#")
mac = get_ontology("http://ifixit.org/mac.owl")


def create_ontology(mac, filepath):
    with mac:

        # --------------------------------------------------------- TYPES ---------------------------------------------------------------------
        class Procedure(Thing):
            pass

        class Step(Procedure):
            pass

        class Toolbox(Procedure):
            pass

        class Tool(Toolbox):
            pass

        class Item(Procedure):
            pass

        class Part(Item):
            pass

        class Image(Step):
            pass

        # --------------------------------------------------------- RELATIONS ---------------------------------------------------------------------
        class has_step(ObjectProperty):
            domain = [Procedure]
            range = [Step]

        class has_tool(ObjectProperty):
            domain = [Toolbox]
            range = [Tool]

        class has_image(ObjectProperty):
            domain = [Step]
            range = [Image]

        class has_part(ObjectProperty):
            domain = [Procedure]
            range = [Part]

        class part_of(ObjectProperty):
            domain = [Or([Item, Part])]
            range = [Item]
            is_transitive = True
            inverse_property = has_part()
        
        class used_in(ObjectProperty):
            domain = [Tool]
            range = [Step]

        class has_item(ObjectProperty):
            domain = [Procedure]
            range = [Item]      
        
        class has_toolbox(ObjectProperty):
            domain = [Procedure]
            range = [Toolbox]

        class subprocedure(ObjectProperty):
            domain = [Procedure]
            range = [Procedure]

        # --------------------------------------------------------- DATA PROPERTIES ---------------------------------------------------------------------

        class step_number(DataProperty, FunctionalProperty):
            domain = [Step]
            range = [int]

        class step_description(DataProperty, FunctionalProperty):
            domain = [Step]
            range = [str]

        class has_name(DataProperty, FunctionalProperty):
            domain = [Or([Procedure, Tool, Item, Part])]
            range = [str]
        
        # ---------------------------------------------------- SWRL -----------------------------------------------------------------
        
        rule1 = Imp()
        rule1.set_as_rule("""Procedure(?proc1), has_item(?proc1, ?item), Procedure(?proc2), has_item(?proc2, ?item) -> subprocedure(?proc1, ?proc2)""")

        rule2 = Imp()
        rule2.set_as_rule("""Procedure(?proc1), has_item(?proc1, ?item1), part_of(?item1, ?item2), Procedure(?proc2), has_item(?proc2, ?item2),  -> subprocedure(?proc1, ?proc2)""") # First Item is a part of second Item

        rule3 = Imp()
        rule3.set_as_rule("""Procedure(?proc1), has_part(?proc1, ?part), part_of(?part, ?item), Procedure(?proc2), has_item(?proc2, ?item) -> subprocedure(?proc1, ?proc2)""") # First Part is a part of second Item

        rule4 = Imp()
        rule4.set_as_rule("""Procedure(?proc1), has_part(?proc1, ?part1), part_of(?part1, ?part2), Procedure(?proc2), has_part(?proc2, ?part2) -> subprocedure(?proc1, ?proc2)""") # First Part is a part of second Part
        
        mac.save(filepath)

#TO DO: 
        
#1) OWL ONTOLOGY RULES
#2) DOWNWARD DIRECTION OF RELATIONS DONE
#3) SWRL RULES