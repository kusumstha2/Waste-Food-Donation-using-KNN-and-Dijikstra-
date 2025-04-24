// Get the donation list container
const donationList = document.getElementById('donation-list');
print('hello');
print(donationList);

// Fetch donations from localStorage
let donations = JSON.parse(localStorage.getItem('donations')) || [];
print('yeta');
print(donations);

// Function to render donation cards
function renderDonations() {
  donationList.innerHTML = ''; // Clear the list

  if (donations.length === 0) {
    donationList.innerHTML = '<p>No donations available yet.</p>';
  } else {
    donations.forEach((donation, index) => {
      const card = document.createElement('div');
      card.className = 'card';

      const img = document.createElement('img');
      img.src = donation.foodImage;
      img.alt = donation.foodName;
      card.appendChild(img);

      const details = `
        <h3>${donation.foodName}</h3>
        <p><strong>Donor:</strong> ${donation.donorName}</p>
        <p><strong>Type:</strong> ${donation.foodType}</p>
        <button class="view-details-btn" onclick="viewDetails(${index})">View Details</button>
        <button class="edit-btn" onclick="editDonation(${index})">Edit</button>
        <button class="delete-btn" onclick="deleteDonation(${index})">Delete</button>
      `;
      card.innerHTML += details;

      donationList.appendChild(card);
    });
  }
}

// Function to show details in the same card
// Get the donation list container



// Function to render donation cards

// Function to fetch and show details of a specific donation
async function viewDetails(donationId) {
  try {
    console.log('Fetching details for Donation ID:', donationId);
    const response = await fetch(`/donation_details/${donationId}/`);
    if (!response.ok) {
      throw new Error('Failed to fetch donation details');
    }
    const donation = await response.json();

    console.log('Donation Data:', donation);

    const detailsDiv = document.createElement('div');
    detailsDiv.innerHTML = `
      <div style="display: flex; gap: 10px; margin-bottom: 15px;">
        <button class="back-btn" onclick="renderDonations()">← Back</button>
        <button class="book-now-btn" onclick="bookNow(${donation.id})">Book Now</button>
      </div>
      <p><strong>Donor:</strong> ${donation.donor_name}</p>
      <p><strong>Food Name:</strong> ${donation.food_name}</p>
      <p><strong>Food Type:</strong> ${donation.food_type}</p>
      <p><strong>Description:</strong> ${donation.description}</p>
      <p><strong>Location:</strong> ${donation.location}</p>
      <p><strong>Expiry Date:</strong> ${donation.expiry_date}</p>
      <img src="${donation.food_image_url}" alt="${donation.food_name}" style="width: 100%; max-width: 300px;">
    `;

    const donationList = document.getElementById('donationList');
    if (!donationList) {
      throw new Error('donationList element not found in the DOM');
    }

    donationList.innerHTML = ''; // Clear the list
    donationList.appendChild(detailsDiv);
  } catch (error) {
    console.error('Error fetching donation details:', error);
  }
}