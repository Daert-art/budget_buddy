document.addEventListener("DOMContentLoaded", function(e) {
    const form = document.getElementById("operation-form");
    if (!form) return;

    const url = form.dataset.url;
    const responseEl = document.getElementById("operation-response");

    form.addEventListener("submit", async function(e) {
        e.preventDefault();
        const formData = new FormData(form);
        const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;

        try {
            const response = await fetch(url, {
                method: "POST",
                headers: {
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: formData
            });

            const data = await response.json();
            if (response.ok) {
                responseEl.innerText = data.message || "✅ Успішно збережено!";
            } else {
                responseEl.innerText = data.message || "❌ Помилка!";
                console.error(data.errors);
            }
        } catch (err) {
            console.error(err);
            responseEl.innerText = "⚠️ Щось пішло не так.";
        }
    });
});
