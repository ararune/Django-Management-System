function filterStudents(status) {
    var tableRows = document.getElementsByClassName("student-row");
    for (var i = 0; i < tableRows.length; i++) {
      var row = tableRows[i];
      if (status === "all" || row.getAttribute("data-status") === status) {
        row.style.display = "table-row";
      } else {
        row.style.display = "none";
      }
    }
  }