function confirmDelete(deleteUrl) {
    if (confirm("Are you sure you want to delete this item?")) {
        window.location.href = deleteUrl;
    } else {
        // Do nothing
    }
}
