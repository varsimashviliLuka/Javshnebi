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
        <td>${element.center_name_english}</td>
        <td>${element.category_name_english}</td>
        <td>${localStorage.getItem('user_email')}</td>
        <td>${element.email_sent_at}</td>
      `;
      tbody.appendChild(row);
    });

    })

}else {
    showAlert('alertPlaceholderSubscription', 'danger', 'გთხოვთ გაიაროთ ავტორიზაცია')
}
  }
  


