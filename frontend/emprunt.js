document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    if (!form) return;
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            id_utilisateur: form.id_utilisateur.value,
            id_livre: form.id_livre.value,
            date_remettre: form.date_retour.value
        };
        try {
            const res = await fetch('/api/emprunter', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            const json = await res.json();
            alert(json.message);
        } catch (err) {
            alert("Erreur lors de l'emprunt");
        }
    });
});

