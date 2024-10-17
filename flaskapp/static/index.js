document.addEventListener("DOMContentLoaded", function () {
  fetch("/consistent")
    .then((response) => response.json())
    .then((result) => {
      console.log("Consistency data:", result);
      if (!result.Consistent) {
        error_report = ""
        for (let report of result.report) {
          error_report += report + "\n";
        }
        const errorPopup = document.createElement("div");
        errorPopup.textContent = error_report;
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
