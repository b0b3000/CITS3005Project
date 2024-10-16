from owlready2 import *
from rdflib import *

def create_ontology(mac: Ontology, filepath):
    with mac:

        # --------------------------------------------------------- TYPES ---------------------------------------------------------------------
        class Procedure(Thing):
            pass

        class Step(Thing):
            pass

        class Toolbox(Thing):
            pass

        class Tool(Thing):
            pass

        class Item(Thing):
            pass

        class Part(Thing):
            pass

        class Image(Thing):
            pass

        # --------------------------------------------------------- RELATIONS ---------------------------------------------------------------------
        class has_step(ObjectProperty):
            domain = [Procedure]
            range = [Step]

        class in_toolbox(ObjectProperty):
            domain = [Tool]
            range = [Toolbox]

        class has_image(ObjectProperty):
            domain = [Step]
            range = [Image]

        class part_of(ObjectProperty):
            domain = [Or([Item, Part])]
            range = [Item]
            is_transitive = True
        
        class used_in(ObjectProperty):
            domain = [Tool]
            range = [Step]

        class has_procedure(ObjectProperty):
            domain = [Or([Item, Part])]
            range = [Procedure]
        
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

        '''class procedure_name(DataProperty, FunctionalProperty):
            domain = [Procedure]
            range = [str]

        class tool_name(DataProperty, FunctionalProperty):
            domain = [Tool]
            range = [str]

        class item_name(DataProperty, FunctionalProperty):
            domain = [Item]
            range = [str]

        class part_name(DataProperty, FunctionalProperty):
            domain = [Part]
            range = [str]'''
        
        class test(ObjectProperty):
            domain = [Procedure]
            range = [Procedure]
        
        # ---------------------------------------------------- SWRL -----------------------------------------------------------------
        
        rule = Imp()
        rule.set_as_rule("""Procedure(?proc1), subprocedure(?proc1, ?proc2), Procedure(?proc2) -> test(?proc1, ?proc2)""")

        mac.save(filepath)

#TO DO: 
        
#1) OWL ONTOLOGY RULES
#2) DOWNWARD DIRECTION OF RELATIONS
#3) SWRL RULES