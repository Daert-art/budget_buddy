document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("recurring-form");
    if (!form) return;

    const url = form.dataset.url;
    const responseDiv = document.getElementById("recurring-response");

    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        const formData = new FormData(form);
        const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;

        try {
            const response = await fetch(url, {
                method: "POST",
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": csrfToken
                },
                body: formData
            });

            if (!response.ok) {
                throw new Error("Server error");
            }

            const data = await response.json();
            console.log("AJAX response:", data);

            if (data.success) {
                responseDiv.innerHTML = `<div class="alert alert-success">Операцію додано успішно</div>`;
                form.reset();
            } else {
                const errors = JSON.parse(data.error);
                let errorHtml = "";
                for (let field in errors) {
                    errors[field].forEach(e => {
                        errorHtml += `<div><strong>${field}:</strong> ${e.message}</div>`;
                    });
                }
                responseDiv.innerHTML = `<div class="alert alert-danger">${errorHtml}</div>`;
            }
        } catch (error) {
            console.error(error);
            responseDiv.innerHTML = `<div class="alert alert-danger">Щось пішло не так.</div>`;
        }
    });
});
