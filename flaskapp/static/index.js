document.addEventListener("DOMContentLoaded", function () {
  fetch("/consistent")
    .then((response) => response.json())
    .then((result) => {
      if (!result) {
        const errorPopup = document.createElement("div");
        errorPopup.textContent = "Ontology has errors!";
        errorPopup.id = "error-popup";

        document.body.appendChild(errorPopup);

        setTimeout(() => {
          document.body.removeChild(errorPopup);
        }, 3000);
      }
    })
    .catch((error) => {
      console.error("Error fetching consistency data:", error);
    });
});
