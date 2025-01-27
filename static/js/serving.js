// Add functionality to the close button
document.getElementById("closeButton").addEventListener("click", function () {
    window.location.href = "{% url 'foodapp:index' %}";
});
