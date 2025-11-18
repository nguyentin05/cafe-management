function updateUI(data) {
    let items = document.getElementsByClassName("cartCounter");
    for (let item of items)
        item.innerText = data.total_quantity;

    let amounts = document.getElementsByClassName("cartAmount");
    for (let item of amounts)
        item.innerText = data.total_amount.toLocaleString();
}

function addToCart(id, name, price) {
    event.preventDefault()

    fetch('/api/add-cart', {
        method: 'post',
        body: JSON.stringify({
            'id': id,
            'name': name,
            'price': price
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        updateUI(data);
    })
}