async function runQuery(search_id) {
  // Send a POST request with the search_id and search term
  try {
    console.log("Search ID:", search_id);
    const response = await fetch("/get_query", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ search_id: search_id }),
    });
    

    const resultsList = document.getElementById("results_list");
    resultsList.innerHTML = ""; // Clear previous results
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || "Network response was not ok");
    }
    const results = await response.json();
    
     // Clear previous results

    for (let result of results) {
      console.log("Result:", result);
      const listItem = document.createElement("li");
      listItem.classList.add("result-item"); // Add class to list item
      listItem.textContent = result;
      resultsList.appendChild(listItem);
    }
  } catch (error) {
    console.error("There was a problem with the fetch operation:", error);
    const error_div = document.createElement("div");
    const resultsList = document.getElementById("results_list");

    if (error.message == "Network response was not ok") {
      error_div.innerHTML = "Network response was not ok";
    }
    if (error.message == "Query not found") {
      error_div.innerHTML = "Query not found";
    }
    if (error.message == "Query has no results") {
      error_div.innerHTML = "Query has no results";
    }
    resultsList.appendChild(error_div);
  }
}

async function createNewQuery() {
  // Get the value from the textbox
  name_obj = document.getElementById("newQueryName");
  value_obj = document.getElementById("newQueryValue");
  const newQueryName = name_obj.value;
  const newQueryValue = value_obj.value;
  console.log("New Query Name:", newQueryName);
  console.log("New Query Value:", newQueryValue);

  try {
    const response = await fetch("/add_query", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name: newQueryName, value: newQueryValue }),
    });

    // Reload the page or update the button list to include the new query
    location.reload();
  } catch (error) {
    console.error("Error:", error);
  }
}
