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
        
        class transitive_part_of(ObjectProperty):
            domain = [Or([Item, Part])]
            range = [Item]
            is_transitive = True

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

        class Procedure(Thing):
            has_step.min(1),  
            has_toolbox.exactly(1),
            has_item.exactly(1),
            has_part.exactly(1),
            has_name.exactly(1)
        
        class Part(Item):
            has_name.exactly(1)
        
        class Item(Procedure):
            has_name.exactly(1)
        
        class Tool(Toolbox):
            has_name.exactly(1)
        
        class Step(Procedure):
            step_number.exactly(1)
            step_description.exactly(1)
        
        # ---------------------------------------------------- SWRL -----------------------------------------------------------------
        
        #Subprocedure
        rule1 = Imp().set_as_rule("""Procedure(?proc1), has_item(?proc1, ?item), Procedure(?proc2), has_item(?proc2, ?item) -> subprocedure(?proc1, ?proc2)""") #First Item is same as Second Item
        rule2 = Imp().set_as_rule("""Procedure(?proc1), has_item(?proc1, ?item1), part_of(?item1, ?item2), Procedure(?proc2), has_item(?proc2, ?item2),  -> subprocedure(?proc1, ?proc2)""") # First Item is a part of second Item
        rule3 = Imp().set_as_rule("""Procedure(?proc1), has_part(?proc1, ?part), part_of(?part, ?item), Procedure(?proc2), has_item(?proc2, ?item) -> subprocedure(?proc1, ?proc2)""") # First Part is a part of second Item
        rule4 = Imp().set_as_rule("""Procedure(?proc1), has_part(?proc1, ?part1), part_of(?part1, ?part2), Procedure(?proc2), has_part(?proc2, ?part2) -> subprocedure(?proc1, ?proc2)""") # First Part is a part of second Part
        
        #Transitive 'part_of'
        rule5 = Imp().set_as_rule("""Part(?part1), Item(?part2), Item(?part3), part_of(?part1, ?part2), part_of(?part2, ?part3) -> part_of(?part1, ?part3)""")
        rule6 = Imp().set_as_rule("""Item(?part1), Item(?part2), Item(?part3), part_of(?part1, ?part2), part_of(?part2, ?part3) -> part_of(?part1, ?part3)""")

        mac.save(filepath)