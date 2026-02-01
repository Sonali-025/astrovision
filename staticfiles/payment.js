// ===============================
// SERVICE PRICE LIST (GLOBAL)
// ===============================
window.SERVICE_PRICES = {
    "Tarot Reading": 501,
    "Tarot Guidance (Combined)": 501,
    "Yes / No Answers": 101,
    "Angel Guidance (Combined)": 501,
    "Angel Oracle Reading": 501,
    "Akashic Record Reading": 2999,
    "Tarot + Angel Overall Package": 999,

    "Kundali Analysis": 251,
    "Palm Reading": 251,
    "Numerology": 251,
    "Spritiual Guidance": 251,
    "Vastu Consultation": 251
};

// ===============================
// PAYMENT HANDLER
// ===============================
document.addEventListener("DOMContentLoaded", function () {

    const payBtn = document.getElementById("payButton");
    if (!payBtn) return;

    payBtn.addEventListener("click", async function (e) {
        e.preventDefault();

        // ===============================
        // COLLECT FORM DATA
        // ===============================
        const name = document.getElementById("name").value.trim();
        const phone = document.getElementById("phone").value.trim();
        const service = document.getElementById("service").value;
        const message = document.getElementById("message").value.trim();
        const dob = document.getElementById("date").value;
        const tob = document.getElementById("time").value;
        const pob = document.getElementById("pob").value.trim();

        if (!name || !phone || !service) {
            alert("Please fill all required fields.");
            return;
        }

        const amount = SERVICE_PRICES[service];
        if (!amount) {
            alert("Invalid service selected.");
            return;
        }

        // ===============================
        // CREATE RAZORPAY ORDER
        // ===============================
        let order;
        try {
            const response = await fetch("/create-order/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": getCookie("csrftoken"),
                },
                body: new URLSearchParams({ amount })
            });

            if (!response.ok) throw new Error("Order creation failed");
            order = await response.json();

        } catch (err) {
            alert("Unable to initiate payment. Please try again.");
            console.error(err);
            return;
        }

        // ===============================
        // RAZORPAY POPUP
        // ===============================
        const options = {
            key: RAZORPAY_KEY,
            amount: order.amount,
            currency: "INR",
            name: "AstroVision",
            description: service,
            order_id: order.id,

            handler: async function (response) {

                // ===============================
                // STEP 1: VERIFY PAYMENT
                // ===============================
                let verifyResult;
                try {
                    const verifyResponse = await fetch("/verify-payment/", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/x-www-form-urlencoded",
                            "X-CSRFToken": getCookie("csrftoken"),
                        },
                        body: new URLSearchParams({
                            razorpay_order_id: response.razorpay_order_id,
                            razorpay_payment_id: response.razorpay_payment_id,
                            razorpay_signature: response.razorpay_signature,
                        })
                    });

                    verifyResult = await verifyResponse.json();

                    if (verifyResult.status !== "success") {
                        window.location.href = "/payment-failed/";
                        return;
                    }

                } catch (err) {
                    window.location.href = "/payment-failed/";
                    return;
                }

                // ===============================
                // STEP 2: SAVE BOOKING (DB + EMAIL)
                // ===============================
                try {
                    const bookingResponse = await fetch("/confirm-booking/", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/x-www-form-urlencoded",
                            "X-CSRFToken": getCookie("csrftoken"),
                        },
                        body: new URLSearchParams({
                            name,
                            phone,
                            service,
                            dob,
                            tob,
                            pob,
                            message,
                            amount,
                            razorpay_order_id: response.razorpay_order_id,
                            payment_id: response.razorpay_payment_id,
                            razorpay_signature: response.razorpay_signature
                        })
                    });

                    const bookingResult = await bookingResponse.json();

                    if (bookingResult.status === "success") {
                        window.location.href = "/payment-success/";
                    } else {
                        window.location.href = "/payment-failed/";
                    }

                } catch (err) {
                    window.location.href = "/payment-failed/";
                }
            },

            theme: {
                color: "#7A0C0C"
            }
        };

        const rzp = new Razorpay(options);
        rzp.open();
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
