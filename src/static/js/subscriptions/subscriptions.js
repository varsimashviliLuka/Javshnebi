  function get_subscriptions(){
if (localStorage.getItem('access_token')){
    let data = {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json'
    }}

    const tbody = document.getElementById("subscriptionsTableBody");
    tbody.innerHTML = ""; // clear existing

    makeApiRequest('/api/subscription', data)
    .then(resp => {
    resp.forEach(element => {
            const row = document.createElement("tr");
row.innerHTML = `
  <td>
    <span class="badge bg-${element.active ? 'success' : 'secondary'}">
      ${element.active ? 'Active' : 'Inactive'}
    </span>
  </td>
  <td>${element.center_name_english}</td>
  <td>${element.category_name_english}</td>
  <td>${element.email_sent_at}</td>
  <td>
    <button 
      class="btn btn-sm btn-${element.active ? 'outline-danger' : 'outline-success'}" 
      onclick="${element.active 
        ? `toggleSubscriptionAction(${element.subscription_id})` 
        : `toggleSubscriptionAction(${element.subscription_id})`}">
      ${element.active ? 'Deactivate' : 'Activate'}
    </button>
  </td>
`;
      tbody.appendChild(row);
    });

    })

}else {
    showAlert('alertPlaceholderSubscription', 'danger', 'To use this service, Please log in!')
}
  }


function toggleSubscriptionAction(subscription_id){

if (localStorage.getItem('access_token')){
    let data = {
    method: 'PATCH',
    headers: {
        'Content-Type': 'application/json'
    }}

    makeApiRequest(`/api/subscription/${subscription_id}`, data)
    .then(resp =>{
      if (resp.message){
        showAlert('alertPlaceholderSubscription', 'success', resp.message)
        get_subscriptions()
      }else {
        showAlert('alertPlaceholderSubscription', 'danger', resp.error)
      }
    })

  }
}
  


