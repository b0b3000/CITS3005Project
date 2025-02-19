

<div class="content-section">

</div>

<div class="schema">
  <section id="into">
    <h1 class="title_heading">Introduction</h1>
    <div class="section overview_section">
      <h2 class="section_heading">Welcome to the iFixit Knowledge Graph App User Manual!</h2>
      <p class="guide_text">
        This manual contains three sections to help you make the most out of this application, and harness the full capacity of its accompanying source code.
        The manual has 3 sections: 
        <br>The first will explain the ontology and schema of our knowledge graph. 
        <br>The second will explain our queries, how to implement your own custom SPARQL queries, and how to search different areas of the graph.
        <br>The third section will explain how to add, edit and remove procedures from the knowledge graph, or edit the ontology.
      </p>
      <h2 class="section_heading">Running our application</h2>
      <p class="guide_text">
        In order to run the application, follow the following steps:
        <br>1: Unzip the project folder
        <br>2: Open the location of the project folder in an IDE or a terminal window
        <br>3: Change directory into the flask app's location by executing the following command: 'cd flaskapp'
        <br>4: Ensure all requirements are fulfilled by running 'pip install -r requirements.txt' (Optional: Use a virtual environment to manage packages)
        <br>5: Start the flask app by running 'flask run'
        <br>6: Allow some time for the graph to be built and verified with the ontology. When you see the terminal output: 'Running on http://127.0.0.1:500' or similar, the webpage is ready to access
        <br>7: Access the web page by navigating to the outputted address above in a browser
        <br>8: Begin using the features of the page!
      </p>
      <h2 class="section_heading">Application Runtime description</h2>
      <p class="guide_text">
        The running of our flask application follows the following broad steps:
        <br>1: The ontology is created using ontology.py.
        <br>2: Data is parsed from a json file. <strong>The file being loaded be changed by modifying JSON_FILE_PATH in app.py</strong>
        <br>3: The ontology is populated with entities and relations, and saved in an owl file. <strong>The name of this can be changed by modifying ONTO_FILE_PATH in app.py</strong>
        <br>4: The owl reasoner is ran to infer new relations and classes
        <br>5: Any ontology violations caught by the owl reasoner, or the function constrained_to_ont are noted, and amended by the reasoner if possible
        <br>6: The knowledge graph is serialised in RDF/XML Turtle form, and saved in a .xml file. <strong>The name of this can be changed by modifying RDFXML_FILE_PATH in app.py</strong>
        <br>7: The flask app is deployed, and users are notified if ontology violations exist
        <br>8: Users are free to navigate and use the webpage's many features.
      </p>
      <h2 class="section_heading">Building the knowledge graph without deploying a flask app</h2>
      <p class="guide_text">
        For testing purposes or otherwise, sometimes it is convenient to generate a knowledge graph from data without running the flask app.
        We have provided a functionality for doing so. Simply run the command 'python run_no_flask', which will generate .owl and .xml files containing the knowledge graph and ontology data.
        The names of the .json file the data is parsed from, and the .owl and .xml files serialised can be specified/changed in run_no_flask.py.
      </p>
    </div>
  </section>

  <section id="schema">
    <h1>Part 1: Ontology</h1>
<h2>Overview</h2>
The iFixit Knowledge Graph's ontology models and represents instructional repair guides and associated resources in the 'Mac' category. It captures the relationships between procedures, steps, tools, items, and other entities, allowing users to semantically query, edit, and add to the knowledge graph efficiently. It uses RDFS and OWL to place constraints on the data and SWRL statements to apply deductions. These are enforced using an OWL reasoner.  

---

## Classes (Types of Entities)  
- **Procedure**: Represents an entire guide for a Mac product fix.  
- **Step**: Represents a step within a **Procedure**.  
- **Toolbox**: A logical container for **Tools**.  
- **Tool**: An individual utility item used to conduct a fix.  
- **Item**: The Mac product which is the subject of the article.  
- **Part**: A specific component of the **Item** which the fix is about.  
- **Image**: A photo used to provide a visualization of how to complete a **Step**.  

---

## Object Properties (Relationships Between Entities)  
- **has_step**: Links a procedure to a step when a step is part of that procedure.  
- **has_tool**: Links a toolbox to a tool used in the procedure the toolbox belongs to.  
- **has_image**: Links a step to a reference image if it is used in that step.  
- **has_part**: Links a procedure to a part if it is the subject of the procedure.  
- **has_item**: Links a procedure to an item it is about.  
- **has_toolbox**: Links a procedure to the associated toolbox.  
- **part_of**: Indicates that an item (or part) is a component of another item. This relation is transitive.  
- **used_in**: Links a tool to a step it is used in.  
- **subprocedure**: Indicates that a procedure is for the same item as another procedure or for a part/item which is a **part_of** the other procedure's item. This relation is transitive.  

---

## Data Properties (Attributes of Entities)  
- **step_number**: An integer representing the order of a step in the procedure (begins at 0).  
- **step_description**: A string containing details of how to conduct a step.  
- **has_name**: A string containing the user-friendly name for an item, part, tool, or procedure.  

---

## Constraints (OWL & RDFS)  
- **Procedure**: Must have exactly one toolbox, one item, and one part, of classes **Toolbox**, **Item**, and **Part** respectively.  
  - Must have at least one step (of class **Step**).  
- **Part, Item, Tool, Procedure**: Must have exactly one name of type string.  
- **Step**: Must have exactly one integer step number and one string step description.  

---

## SWRL Rules (Logical Implications)  
These rules ensure logical consistency in the ontology and help to form new relations and deduce unstated relationships:  
- **Rule 1-9**: Ensure that a procedure has steps, toolboxes, items, and parts, and that tools are used in steps.  
- **Rules A1-A4**: Create **subprocedure** relationships and apply transitivity to this relation.  
- **Rule A5**: Ensures tools used in a step of a procedure appear in the toolbox.  
- **Rules A6-A7**: Ensures the **part_of** relation is transitive.  

---

## Disjoint Classes  
Disjointness ensures that an entity cannot belong to two specific classes at the same time:  
- **Procedure and Step**: An entity cannot be both a procedure and a step, ensuring a clear differentiation between the two.  

  <section id="Queries">
    <h2 class="title_heading">Part 2: Queries & Searches</h2>
    <div class="properties_section">
      <p class="guide_text">
        <h3>Using the Search Procedure tab</h3>
        The procedure search tab provides a helpful and intuitive method of navigating Mac guides.
        Search for a procedure in this tab by inputting some keywords or substrings of the procedure.
        <strong>For Example: </strong> To search for the procedure "Mac Intel 27" Fan Replacement", you
        searches "fan replacement", "mac intel 27", or even just "fan" would bring up the results containing this procedure.
        After generating a list of matching procedures, users can examine the details of a procedure, and its relations in the knowledge graph by <strong>clicking</strong> 
        on the procedure's box. This will bring up a page relating to the specific procedure, containing all relevant information.
        <h3>Using the Keyword Search tab</h3>
        In this tab, you can further refine your search by searching for a specific Item, Part, Tool or Step. 
        Similarly to the Search Procedure tab, users can search by keyword or substring of Item/Part/Tool name, or Step description.
        Users can choose which entity type is being searched by selecting the relevant search in the dropdown menu prior to searching.
      </p>
    </div>
    <div class="constraints_section">
      <p class="guide_text">
        <h3>Using the pre-made SPARQL queries</h3>
        We have provided a set of pre-written SPARQL queries. These can be ran on the current instance of the knowledge graph by selecting
        their corresponding button on the SPARQL queries tab of the web page. An example of these is the query: "All procedures with more than 6 steps"
        <h3>Inputting custom SPARQL queries</h3>
        We have also created a custom SPARQL query parses. Simply input your own query's name and accompanying SPARQL code into the boxes, using
        'ns' as the namespace prefix, and select 'Add New Query'. You will now be able to execute this query and view its results.
      </p>
    </div>
  </section>

  <section id="Adding Procedures">
    <h2 class="title_heading">Part 3: Editing Knowledge Graph & Ontology.</h2>
    <div class="properties_section">
      <p class="guide_text">
        <h3>Adding a procedure to the knowledge graph</h3>
        Our website provides an intuitive GUI feature for adding procedures to our knowledge graph. This can be found in the 'Add Procedure' tab.
        This interface is very self-explanatory, and guides a user through the process of adding a procedure, and does so in a way that ensures all 
        existing ontology conditions are adhered to. The process begins with requiring the user to input the Procedure, Item and Part name. Keywords 
        in the item name can be used to generate recommended 'ancestor' or parent items, in order to apply the 'part_of' relation. These can be searched 
        for by selecting the 'Search Ancestors' button after entering an item name, and selecting one of the entries in the outputted drop-down list.
        Not selecting an ancestor defaults the graph to assigning 'root' as an ancestor to the new item. <strong>Try this out! Only existing ancestors 
          can be recommneded, so test this feature by naming the item 'Mac', bringing up a number of existing items.</strong> Tools can be added iteratively by
          selecting the 'add tool' button, and finalised by selecting 'set tools'. Once the tools used are set, the user can begin writing steps, adding images to
          visualise these by selecting the empty image box in the 'Add Step' area and providing a reference URL. For each step, users can select which tools from the toolbox are being used.
          After all steps are finalised, users can submit this procedure by pressing the 'Submit' button. <br>
          Following this, users can check if their amended knowledge graph still follows the ontology restraints by navigating to the 'Home' tab and checking for ontology errors.
          Added procedures now show up in SPARQL query and search results (if applicable).
        <h3>Editing existing procedures in the knowledge graph</h3>
        Editing of the knowledge graph must be done through editing the source json data file. Alternatively, the json source file can be 
        adjusted to build the graph based on a different file (see Introduction section). To edit the existing json file, users should open the 
        data file in a text editor of their choosing. Next, they should edit any of the existing text values as they see fit. Following editing 
        of the knowledge graph, users should re-run the flask application (control+C followed by 'flask run' in the terminal)<strong>Note: </strong> 
        Each "entry" dictionary instance corresponds to one procedure. 
        Users can use the following as a guide of which json data points in the entry correspond to each entity for editing this data:
        <br><br><strong>Procedure:</strong> entry["Title"]
        <br><strong>Item:</strong> entry["Category"]
        <br><strong>Part:</strong> a concatenation of Item and entry["Subject"]
        <br><strong>Toolbox:</strong> a concatenation of Procedure and "toolbox"
        <br><strong>Tool:</strong> each value of entry["Toolbox"]["Name"]
        <br><strong>Step:</strong> each value of entry["Steps"]
        <br><strong>Image:</strong> each value of entry["Steps"]["Images"]
        <h3>Delete existing procedures from the knowledge graph</h3>
        Deleting of procedures in the knowledge graph should also be done in the aforementioned source json data file.
        This is a much simpler task, as users can simply delete entire 'entries' that they do not wish to be included in the graph.
        Alternatively, users can also delete specific tools or steps they deem unnecessary. However, it is the user's responsibility 
        to ensure the resulting knowledge graph adheres to ontology restrictions following edits or removals of data.
      </p>
    </div>
    <div class="constraints_section">
      <p class="guide_text">
        <h3>Editing existing ontology</h3>
        Ontologies can be edited in the ontology.py file, as this is where all ontology data is kept. Users have the power to edit the defined classes, properties, and rules. 
        They can add new classes by defining them as subclasses of Thing and create new object or data properties to define relationships or attributes with existing entities. 
        Constraints for each class can be modified by changing the is_a property of each entity to enforce specific rules (e.g., requiring a minimum number of attributes). 
        Additionally, users can modify existing SWRL rules, or create new rules using the set_as_rule() method. This can define interesting logical relationships and reasoning patterns within the ontology, resulting in powerful reasoning.
      </p>
    </div>
    <div class="swrl_rules_section">
      <p class="guide_text">
        <h3>Checking compliance of modified knowledge graph with ontology</h3>
        On the home page of the website, users can find a 'Check Ontology Errors' button. Selecting this button will provide the users
        with an alert either stating that the graph adheres to the ontology, or that it doesn't, along with accompanying non-compliant classes
        (if applicable). <strong>Note: </strong>Allow some time for this button's output to appear, as it involves running an owl reasoner, which takes some time.
    </div>
</div>
