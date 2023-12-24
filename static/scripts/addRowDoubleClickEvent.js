function addRowDoubleClickEvent() {
    document.querySelectorAll("#objectsTable tbody tr").forEach(function (row) {
      row.addEventListener("dblclick", function (event) {
        event.preventDefault();
        window.location.href = "/objects/" + row.getAttribute("data-obj-id");
      });
    });
  }