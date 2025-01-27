document.getElementById("donate-food").addEventListener("click", function () {
    const donorId = document.getElementById("donor-id").value;

    fetch("/email/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(), // Ensure CSRF protection
        },
        body: JSON.stringify({
            donor_id: donorId,
        }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                alert(data.success);
                console.log(`Nearest recipient is ${data.distance} km away.`);
            } else {
                alert(`Error: ${data.error}`);
            }
        })
        .catch((error) => console.error("Error:", error));
});

