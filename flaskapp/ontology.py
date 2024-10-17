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
            is_transitive = True
        
        class subprocedure2(ObjectProperty):
            domain = [Procedure]
            range = [Procedure]
            is_transitive = True

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

        # ---------------------------------------------------------PROPERTY CONSTRAINTS---------------------------------------------------------

        class Procedure(Thing):
            is_a = [
                has_step.min(1),
                has_step.only(Step),
                has_toolbox.exactly(1),
                has_toolbox.only(Toolbox),
                has_item.exactly(1),
                has_item.only(Item),
                has_part.exactly(1),
                has_part.only(Part),
                has_name.exactly(1)
            ]
        
        class Part(Thing):
            is_a = [
                has_name.exactly(1)
            ]
        
        class Item(Thing):
            is_a = [
                has_name.exactly(1)
            ]
        
        class Tool(Thing):
            is_a = [
                has_name.exactly(1)
            ]

        class Step(Thing):
            is_a = [
                step_number.exactly(1),
                step_description.exactly(1)
            ]

        AllDisjoint([Procedure, Step])
        
        # ---------------------------------------------------- SWRL ENFORCEMENTS -----------------------------------------------------------------
        
        rule1 = Imp().set_as_rule("""Procedure(?proc), has_step(?proc, ?step) -> Step(?step)""")
        rule2 = Imp().set_as_rule("""Procedure(?proc), has_toolbox(?proc, ?toolbox) -> Toolbox(?toolbox)""")
        rule3 = Imp().set_as_rule("""Procedure(?proc), has_item(?proc, ?item) -> Item(?item)""")
        rule4 = Imp().set_as_rule("""Procedure(?proc), has_part(?proc, ?part) -> Part(?part)""")
        rule5 = Imp().set_as_rule("""Toolbox(?toolbox), has_tool(?toolbox, ?tool) -> Tool(?tool)""")
        rule6 = Imp().set_as_rule("""Step(?step), has_image(?step, ?img) -> Image(?img)""")
        rule7 = Imp().set_as_rule("""Tool(?tool), used_in(?tool, ?step) -> Step(?step)""")
        rule8 = Imp().set_as_rule("""Part(?part), part_of(?part, ?item) -> Item(?item)""")
        rule9 = Imp().set_as_rule("""Part(?item1), part_of(?item1, ?item2) -> Item(?item2)""")



        # ---------------------------------------------------- SWRL ADDITIONS -----------------------------------------------------------------
        
        # Create subprocedures
        rule_a1 = Imp().set_as_rule("""Procedure(?proc1), has_item(?proc1, ?item), Procedure(?proc2), has_item(?proc2, ?item), DifferentFrom(?proc1, ?proc2) -> subprocedure(?proc1, ?proc2)""") #First Item is same as Second Item
        rule_a2 = Imp().set_as_rule("""Procedure(?proc1), has_item(?proc1, ?item1), part_of(?item1, ?item2), Procedure(?proc2), has_item(?proc2, ?item2) -> subprocedure(?proc1, ?proc2)""") # First Item is a part of second Item
        rule_a3 = Imp().set_as_rule("""Procedure(?proc1), has_part(?proc1, ?part), part_of(?part, ?item), Procedure(?proc2), has_item(?proc2, ?item) -> subprocedure(?proc1, ?proc2)""") # First Part is a part of second Item
        rule_a4 = Imp().set_as_rule("""Procedure(?part1), Procedure(?part2), Procedure(?part3), subprocedure(?part1, ?part2), subprocedure(?part2, ?part3)-> subprocedure(?part1, ?part3)""") # Adds transitive subprocedure 
        
        #Tools used in step of procedure should appear in toolbox
        rule_a5 = Imp().set_as_rule("""Tool(?tool), used_in(?tool, ?step), Step(?step), has_step(?proc, ?step), has_toolbox(?proc, ?toolbox) -> has_tool(?toolbox, ?tool)""") # First Part is a part of second Item

        # Ensure 'part_of' is transitive
        rule_a6 = Imp().set_as_rule("""Part(?part1), Item(?part2), Item(?part3), part_of(?part1, ?part2), part_of(?part2, ?part3) -> part_of(?part1, ?part3)""")
        rule_a7 = Imp().set_as_rule("""Item(?part1), Item(?part2), Item(?part3), part_of(?part1, ?part2), part_of(?part2, ?part3) -> part_of(?part1, ?part3)""")


        mac.save(filepath)