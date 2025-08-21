window.onload = function() {
    const accountImg = document.getElementById("account-img");
    if (!accountImg) return;

    if (localStorage.getItem("isLoggedIn") === "true") {
        accountImg.style.backgroundColor = "#28a745";
    } else {
        accountImg.style.backgroundColor = "#e91313";
    }
};
function logout() {
    localStorage.removeItem("isLoggedIn");
    alert("You have been logged out.");

    const accountImg = document.getElementById("account-img");
    if (accountImg) {
        accountImg.style.backgroundColor = "#e91313";
        accountImg.style.transform = "scale(1)";
    }
    window.location.href = "biblio.html";
}
