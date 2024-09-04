document.getElementById("file")
.addEventListener("change", function($event) {
    const file = $event.target.files[0];
    if (!file) { return; }

    window.alert("test")

    $event.target.value = '';
});

