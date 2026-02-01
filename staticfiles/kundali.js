document.addEventListener("DOMContentLoaded", function () {

    console.log("kundali.js loaded");

    const yearEl = document.getElementById("year");
    if (yearEl) {
        yearEl.textContent = new Date().getFullYear();
    }

    const form = document.getElementById("kundaliForm");
    if (!form) {
        console.error("kundaliForm not found");
        return;
    }

    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        const data = {
            full_name: document.getElementById("name").value.trim(),
            whatsapp: document.getElementById("phone").value.trim(),
            dob: document.getElementById("dob").value,
            tob: document.getElementById("tob").value,
            pob: document.getElementById("pob").value.trim(),
            gender: document.getElementById("gender").value,
            purpose: document.getElementById("purpose").value,
            message: document.getElementById("message").value.trim(),
        };

        // Required field validation
        for (let key in data) {
            if (!data[key] && key !== "message") {
                alert("Please fill all required fields.");
                return;
            }
        }

        try {
            const response = await fetch("/submit-kundali/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken"),
                },
                body: JSON.stringify(data),
            });

            if (!response.ok) {
                throw new Error("Server returned error");
            }

            const result = await response.json();

            if (result.status === "success") {
                window.location.href = "/kundali-success/";
            } else {
                alert("Something went wrong. Please try again.");
            }

        } catch (error) {
            console.error("Kundali error:", error);
            alert("Unable to submit kundali request. Please try later.");
        }
    });
});

// ===============================
// CSRF HELPER
// ===============================
function getCookie(name) {
    let value = null;
    document.cookie.split(";").forEach(cookie => {
        cookie = cookie.trim();
        if (cookie.startsWith(name + "=")) {
            value = cookie.substring(name.length + 1);
        }
    });
    return value;
}
