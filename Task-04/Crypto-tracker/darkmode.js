const darkmode = localStorage.getItem("darkmode");
const themeSwitch = document.getElementById("theme-switch");
const refreshButton = document.getElementById("refresh-button");

const enableDarkMode = () => {
    document.body.classList.add("darkmode");
    localStorage.setItem("darkmode", "active");
};

const disableDarkMode = () => {
    document.body.classList.remove("darkmode");
    localStorage.removeItem("darkmode");
};

const triggerRefreshAnimation = () => {
    if (!refreshButton) return;

    refreshButton.classList.add("loading");
    refreshButton.disabled = true;

    setTimeout(() => {
        refreshButton.classList.remove("loading");
        refreshButton.disabled = false;
    }, 1200);
};

if (darkmode === "active") {
    enableDarkMode();
}

if (themeSwitch) {
    themeSwitch.addEventListener("click", () => {
        document.body.classList.contains("darkmode") ? disableDarkMode() : enableDarkMode();
    });
}

if (refreshButton) {
    refreshButton.addEventListener("click", triggerRefreshAnimation);
}