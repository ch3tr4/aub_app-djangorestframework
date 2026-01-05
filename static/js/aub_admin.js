document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.getElementById("darkModeToggle");

    if (toggleBtn) {
        toggleBtn.addEventListener("click", function () {
            document.body.classList.toggle("dark-mode");

            // save preference
            localStorage.setItem(
                "aub-dark-mode",
                document.body.classList.contains("dark-mode")
            );
        });
    }

    // load saved mode
    if (localStorage.getItem("aub-dark-mode") === "true") {
        document.body.classList.add("dark-mode");
    }
});
