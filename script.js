function filterTasks() {
  let filter = document.getElementById("filter").value;
  let rows = document.querySelectorAll("#taskTable tr");

  rows.forEach(row => {
    let status = row.getAttribute("data-status");
    if (filter === "All" || status === filter) {
      row.style.display = "";
    } else {
      row.style.display = "none";
    }
  });
}
