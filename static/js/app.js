document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(".prediction-form");
    const button = document.querySelector(".predict-btn");

    if (form && button) {
        form.addEventListener("submit", () => {
            button.querySelector("span").textContent = "Analyzing Customer...";
            button.style.opacity = "0.8";
        });
    }

    const totalCharges = document.querySelector('[name="TotalCharges"]');
    const monthlyCharges = document.querySelector('[name="MonthlyCharges"]');
    const tenure = document.querySelector('[name="tenure"]');

    function updateTotalCharges() {
        if (monthlyCharges.value && tenure.value && !totalCharges.value) {
            totalCharges.value = (parseFloat(monthlyCharges.value) * parseFloat(tenure.value)).toFixed(2);
        }
    }

    monthlyCharges?.addEventListener("blur", updateTotalCharges);
    tenure?.addEventListener("blur", updateTotalCharges);
});
