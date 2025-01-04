function closeToast() {
    var toast = document.getElementById("toast");
    toast.style.opacity = "0"; // Fade out effect
    setTimeout(function() {
        toast.style.visibility = "hidden"; // Hide after fade-out completes
    }, 500); // Wait for fade-out duration before hiding
}

window.onload = function() {
    var toast = document.getElementById("toast");
    if (toast.classList.contains("show")) {
        toast.style.visibility = "visible";
        toast.style.opacity = "1"; // Apply fade-in effect
        // Optionally, set a timeout to auto-hide the toast after a few seconds
        setTimeout(function() {
            closeToast(); // Auto-close after 30 seconds
        }, 30000); // Hide after 30 seconds
    }
};


// Function to show/hide coapplicant income field based on checkbox
function toggleCoapplicantIncome() {
    var coapplicantAvailable = document.getElementById("coapplicantAvailable").checked;
    var coapplicantIncomeField = document.getElementById("coapplicantIncome");
    var coapplicantIncomeLabel = document.getElementById("coapplicantIncomeLabel");

    if (coapplicantAvailable) {
        coapplicantIncomeField.style.display = "block";
        coapplicantIncomeLabel.style.display = "block";
    } else {
        coapplicantIncomeField.style.display = "none";
        coapplicantIncomeLabel.style.display = "none";
    }
}
