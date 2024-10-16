function performSearch() {
  const searchFunction = document.getElementById("searchFunction").value;
  const searchInput = document.getElementById("searchInput").value;
  const searchResults = document.getElementById("results_list");
  searchResults.innerHTML = "";

  fetch("/search_results", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      searchFunction: searchFunction,
      searchInput: searchInput,
    }),
  })
    .then((response) => response.json())
    .then((results) => {
      console.log("Success:", results);

      // Add result items to the lists
      for (let result of results) {
        const listItem = document.createElement("li");
        listItem.classList.add("result-item");
        
        const img = document.createElement("img");
        img.addEventListener("click", displayResult);
        img.src = "/static/banner.png"; // Assuming result has an imageUrl property
        img.alt = result.imageAlt || "Search result image"; // Optional alt text
        listItem.textContent = result;
        listItem.appendChild(img);
        searchResults.appendChild(listItem);
      }
      // Handle the response data here
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

document.addEventListener("DOMContentLoaded", function () {
  document
    .getElementById("searchInput")
    .addEventListener("keypress", function (e) {
      if (e.key === "Enter") {
        console.log(this.value);
        performSearch(this.value);
      }
    });
});

async function displayResult() {
  console.log("Only result");
}
