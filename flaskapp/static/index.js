async function checkConsistency() {
  fetch("/consistent")
    .then((response) => response.json())
    .then((result) => {
      console.log("Consistency data:", result);
      if (!result.Consistent) {
        alert(result.report);
      } else {
        alert("All data is consistent with ontology")
      }
    })
    .catch((error) => {
      console.error("Error fetching consistency data:", error);
    });
}
