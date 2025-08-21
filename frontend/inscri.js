function validateForm() {
    let pass = document.querySelector('input[name="password"]').value;
    let confirm = document.querySelector('input[name="confirm_password"]').value;
    let nom = document.querySelector('input[name="nom"]').value;
    let prenom = document.querySelector('input[name="prenom"]').value;

    if (pass !== confirm) {
        alert("Passwords do not match!");
        return false;
    }

    localStorage.setItem("isLoggedIn", "true");
    localStorage.setItem("username", nom + " " + prenom);

    alert("Account created successfully!");
    window.location.href = "biblio.html"; 
    return false; 
}

