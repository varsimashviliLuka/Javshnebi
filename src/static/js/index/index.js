function populateSelect(selectElement, data) {
    selectElement.innerHTML = ""; // Clear existing options
    for (const [label, value] of Object.entries(data)) {
        const option = document.createElement("option");
        option.value = value;
        option.textContent = label;
        selectElement.appendChild(option);
    }
}


function sendData(option) {
    const selectedCityId = selectCities.value;
    const selectedCategoryId = selectCategories.value;

    if(option == 'subscribe'){
        if (localStorage.getItem('access_token')){
    const formData = {
        
    category_id: selectedCategoryId,
    center_id: selectedCityId,
    active: true

    }

    let data = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    }
        makeApiRequest('/api/subscription', data)
        .then(resp => {
        if (resp.message){
            showAlert('alertPlaceholder', 'success', resp.message)
        }
        else {
            showAlert('alertPlaceholder', 'danger', resp.error)
        }
        })
    }else {
        showAlert('alertPlaceholder', 'danger', 'გთხოვთ გაიაროთ ავტორიზაცია')
    }
}else if (option == 'check') {
  if (localStorage.getItem('access_token')) {
    const formData = {
      category_id: selectedCategoryId,
      center_id: selectedCityId,
    };

    const requestData = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(formData)
    };

    makeApiRequest('/api/filter', requestData)
      .then(resp => {
        const list = document.getElementById("availabilityList");
        list.innerHTML = "";

        if (resp.available_slots && resp.available_slots.length > 0) {
          resp.available_slots.forEach(slot => {
            const { bookingDate, bookingDateStatus } = slot;

            if (bookingDateStatus === 1) {
              const [day, month, year] = bookingDate.split("-");
              const dateObj = new Date(`${year}-${month}-${day}`);
              const formatted = dateObj.toLocaleDateString('en-US', {
                weekday: 'long',
                year: 'numeric',
                month: 'long',
                day: 'numeric'
              });

              const li = document.createElement("li");
              li.className = "list-group-item bg-dark text-white border-secondary";
              li.textContent = formatted;
              list.appendChild(li);
            }
          });
        } else {
          const li = document.createElement("li");
          li.className = "list-group-item bg-secondary text-white";
          li.textContent = "No available dates found.";
          list.appendChild(li);
        }

        const modal = new bootstrap.Modal(document.getElementById("availabilityModal"));
        modal.show();
      })
      .catch(err => {
        console.error("Error checking availability:", err);
        showAlert('alertPlaceholder', 'danger', 'დაფიქსირდა შეცდომა');
      });
  } else {
    showAlert('alertPlaceholder', 'danger', 'გთხოვთ გაიაროთ ავტორიზაცია');
  }
}

}

function loadAvailableSlots() {
    let send = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    }
    makeApiRequest('/api/filter', send)
    .then(data => {
    const tbody = document.querySelector("table tbody");
    tbody.innerHTML = ""; // Clear old rows

    data.forEach(entry => {
      const { city, category, earliest_date } = entry;

      // Convert to readable format: "DD-MM-YYYY" → "Month DD, YYYY"
      const [day, month, year] = earliest_date.split("-");
      const jsDate = new Date(`${year}-${month}-${day}`);
      const formattedDate = jsDate.toLocaleDateString('en-US', {
        year: 'numeric', month: 'long', day: 'numeric'
      });

      const row = `
        <tr>
          <td>${city}</td>
          <td>${capitalize(category)}</td>
          <td>${formattedDate}</td>
        </tr>
      `;

      tbody.insertAdjacentHTML("beforeend", row);
    });
  })
  .catch(err => {
    console.error("Error fetching available slots:", err);
  });
}

function capitalize(word) {
  return word.charAt(0).toUpperCase() + word.slice(1);
}




document.addEventListener("DOMContentLoaded", () => {

    const selectCities = document.getElementById('selectCities')
    const selectCategories = document.getElementById('selectCategories')

    const cities = {
        "Rustavi": 15,
            "Kutaisi": 2,
            "Batumi": 3,
            "Telavi": 4,
            "Akhalcikhe": 5,
            "Zugdidi": 6,
            "Gori": 7,
            "Foti": 8,
            "Ozurgeti": 9,
            "Sachkhere": 10
    };

    const categories = {
        "Automatic": 4,
            "Manual": 3  
    }

    populateSelect(selectCities, cities);
    populateSelect(selectCategories, categories);
    loadAvailableSlots();

})