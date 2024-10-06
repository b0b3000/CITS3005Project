from owlready2 import *
from rdflib import *

fix = Namespace("http://ifixit.org/mac.owl#")
mac = get_ontology("http://ifixit.org/mac.owl")

def create_ontology(mac):
    with mac:
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

        class has_step(ObjectProperty):
            domain = [Procedure]
            range = [Step]

        class in_toolbox(ObjectProperty):
            domain = [Tool]
            range = [Toolbox]

        class has_images(ObjectProperty):
            domain = [Step]
            range = [Image]

        class part_of(ObjectProperty):
            domain = [Item, Part]
            range = [Item]
            is_transitive = True
        
        class used_in(ObjectProperty):
            domain = [Tool]
            range = [Step]

        class has_procedure(ObjectProperty):
            domain = [Item, Part]
            range = [Step]
        
        class has_toolbox(ObjectProperty):
            domain = [Procedure]
            range = [Toolbox]

        class step_number(DataProperty):
            domain = [Step]
            range = [int]

        class step_description(DataProperty):
            domain = [Step]
            range = [str]

        class subprocedure(ObjectProperty):
            domain = [Procedure]
            range = [Procedure]

        mac.save("mac.owl")
    return mac
