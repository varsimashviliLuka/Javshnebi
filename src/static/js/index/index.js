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
    

}}


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

})