async function performSearch() {
  const searchFunction = document.getElementById("searchFunction").value;
  const searchInput = document.getElementById("searchInput").value;
  const searchResults = document.getElementById("results_list");
  searchResults.innerHTML = "";

  const existingNoResultsMessage =
    document.getElementById("no-results-message");
  if (existingNoResultsMessage) {
    existingNoResultsMessage.remove();
  }
  try {
    const response = await fetch("/search_results", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        searchFunction: searchFunction,
        searchInput: searchInput,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error("Error:", errorData.error);
      throw new Error(errorData.error || "Network response was not ok");
    }

    const results = await response.json();
    console.log("Success:", results);

    for (let result of results) {
      console.log(result.text);
      const listItem = document.createElement("li");
      listItem.classList.add("result-item");

      const label = document.createElement("label");
      label.textContent = result.text.replace(/_/g, ' ').replace(/-/g, ' ')
      label.classList.add("result-label");
      listItem.appendChild(label);
      searchResults.appendChild(listItem);
    }
  } catch (error) {
    const noResultsMessage = document.createElement("p");
    noResultsMessage.id = "no-results-message";
    noResultsMessage.textContent = "No results found.";
    searchResults.appendChild(noResultsMessage);
  }

}

async function displayResult() {
  const resultData = this.parentElement.textContent;
  window.location.href = `/result_viewer?data=${resultData}`;
}
