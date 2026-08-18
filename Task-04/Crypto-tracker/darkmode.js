const darkmode = localStorage.getItem("darkmode");
const themeSwitch = document.getElementById("theme-switch");

const enableDarkMode = () => {
    document.body.classList.add("darkmode");
    localStorage.setItem("darkmode", "active");
};

const disableDarkMode = () => {
    document.body.classList.remove("darkmode");
    localStorage.removeItem("darkmode");
};

if (darkmode === "active") {
    enableDarkMode();
}

if (themeSwitch) {
    themeSwitch.addEventListener("click", () => {
        document.body.classList.contains("darkmode") ? disableDarkMode() : enableDarkMode();
    });
}