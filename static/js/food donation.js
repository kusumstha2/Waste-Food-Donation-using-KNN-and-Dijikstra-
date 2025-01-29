document.addEventListener("DOMContentLoaded", function () {
  // Fetch donations from localStorage
  let donations = JSON.parse(localStorage.getItem('donations')) || [];

  function renderDonations() {
    const donationList = document.getElementById('donation-list');
    
    if (donations.length === 0) {
      donationList.innerHTML = '<p>No donations available yet.</p>';
    } else {
      let cards = donations.map(donation => `
        <div class="card">
          <img src="${donation.foodImage}" alt="${donation.foodName}">
          <h3>${donation.foodName}</h3>
          <p><strong>Donor:</strong> ${donation.donorName}</p>
          <p><strong>Type:</strong> ${donation.foodType}</p>
          <button class="view-details-btn" onclick="viewDetails('${donation.id}')">View Details</button>
          <button class="edit-btn" onclick="editDonation('${donation.id}')">Edit</button>
          <button class="delete-btn" onclick="deleteDonation('${donation.id}')">Delete</button>
        </div>
      `).join("");

      donationList.innerHTML = cards;
    }
  }

  renderDonations();
});

// Function to view details
function viewDetails(id) {
  alert(`Viewing details for donation ID: ${id}`);
}

// Function to delete a donation
function deleteDonation(id) {
  let donations = JSON.parse(localStorage.getItem('donations')) || [];
  donations = donations.filter(donation => donation.id !== id);
  localStorage.setItem('donations', JSON.stringify(donations));
  location.reload();
}

// Function to edit a donation
function editDonation(id) {
  window.location.href = `edit_donation.html?id=${id}`;
}

// Close button redirection
document.getElementById("closeButton").addEventListener("click", function () {
  window.location.href = "/dashboard/";
});
