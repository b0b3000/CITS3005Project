async function runQuery(search_id) {
  // Send a POST request with the search_id and search term
  try {
    const resultsList = document.getElementById("results_list");
    resultsList.innerHTML = "";
    console.log("Search ID:", search_id);
    const loadingPopup = document.createElement("div");
    loadingPopup.style.position = "fixed";
    loadingPopup.style.top = "50%";
    loadingPopup.style.left = "50%";
    loadingPopup.style.transform = "translate(-50%, -50%)";
    loadingPopup.style.padding = "10px 20px";
    loadingPopup.style.backgroundColor = "#fff";
    loadingPopup.style.border = "1px solid #ccc";
    loadingPopup.style.boxShadow = "0 0 10px rgba(0, 0, 0, 0.1)";
    loadingPopup.style.zIndex = "1000";
    loadingPopup.id = "loadingPopup";
    loadingPopup.innerHTML = "Loading...";
    document.body.appendChild(loadingPopup);

    const response = await fetch("/get_query", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ search_id: search_id }),
    });
    

     // Clear previous results
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || "Network response was not ok");
    }

    

    // Remove the loading popup once the results are fetched
    const results = await response.json();

    console.log("Results:", results);
    document.body.removeChild(loadingPopup);
    
     // Clear previous results

    for (let result of results) {
      console.log("Result:", result);
      const listItem = document.createElement("li");
      listItem.classList.add("result-item"); // Add class to list item
      listItem.textContent = result.replace(/_/g, ' '); // Replace underscores with spaces
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
