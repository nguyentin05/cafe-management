function updateUI(data) {
    let items = document.getElementsByClassName("cartCounter");
    for (let item of items)
        item.innerText = data.total_quantity;

    let amounts = document.getElementsByClassName("cartAmount");
    for (let item of amounts)
        item.innerText = data.total_amount.toLocaleString();
}

function addToCart(id, name, price, image) {
    event.preventDefault()

    fetch('/api/customer/cart/add', {
        method: 'post',
        body: JSON.stringify({
            'id': id,
            'name': name,
            'price': price,
            'image': image
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        updateUI(data);
    })
}

function pay() {
    const addressInput = document.getElementById('address');
    const address = addressInput.value.trim();

    if (!address) {
        alert("Vui lòng nhập dia chi!");
        return;
    }

    if (confirm('u sure?') == true) {
        fetch('/api/customer/pay', {
            method: 'post',
            body: JSON.stringify({
                'address': address
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then(data => {
            if (data.code == 200)
                location.reload()
        })
    }
}
function updateCart(id) {
    fetch('/api/customer/cart/update/' + id, {
        method: 'put',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        updateUI(data);
    })
}
function deleteCart(id) {
    fetch('/api/customer/cart/delete/' + id, {
        method: 'delete',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        updateUI(data);
    })
}