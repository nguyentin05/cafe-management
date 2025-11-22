function addItemRow() {
    const body = document.getElementById('order-items');
    const firstRow = body.querySelector('.order-item');

    if (!firstRow) return;

    const newRow = firstRow.cloneNode(true);

    const select = newRow.querySelector('.dish-select');
    const qtyInput = newRow.querySelector('.quantity');
    const priceInp = newRow.querySelector('.price');
    const amtInp = newRow.querySelector('.amount');

    if (select) select.selectedIndex = 0;
    if (qtyInput) qtyInput.value = 1;
    if (priceInp) priceInp.value = '';
    if (amtInp) amtInp.value = '';

    body.appendChild(newRow);
}
function getAndUpdateItem(obj) {
    const row = obj.closest('tr');
    if (!row) return null;

    const select = row.querySelector('.dish-select');

    if (!select || select.selectedIndex === 0) return null;

    const option = select.selectedOptions[0];

    if (!option.dataset.price) return null;

    const qtyInput = row.querySelector('.quantity');
    const priceInput = row.querySelector('.price');
    const amountInput = row.querySelector('.amount');

    const price = parseInt(option.dataset.price);
    let qty = parseInt(qtyInput.value);

    if (isNaN(qty) || qty < 1) {
        qty = 1;
        qtyInput.value = 1;
    }

    priceInput.value = price.toLocaleString();
    amountInput.value = (price * qty).toLocaleString();

    return {
        id: option.value,
        name: option.textContent.trim(),
        price: price,
        quantity: qty
    };
}

function addToDraft(obj) {
    const itemData = getAndUpdateItem(obj);
    if (!itemData) return;

    fetch('/api/add-draft', {
        method: 'post',
        body: JSON.stringify(itemData),
        headers: {
         'Content-Type': 'application/json'
         }
    })
    .then(res => res.json())
    .then(data => {
        console.log('Added:', data);
        if (typeof updateUI === 'function') updateUI(data);
    })
    .catch(err => console.error('Error add-draft:', err));
}

function updateToDraft(obj) {
    const itemData = getAndUpdateItem(obj);
    if (!itemData) return;

    fetch('/api/update-draft', {
        method: 'put',
        body: JSON.stringify({
            'id': itemData.id,
            'quantity': itemData.quantity
        }),
        headers: {
        'Content-Type': 'application/json'
        }
    })
    .then(res => res.json())
    .then(data => {
        console.log('Updated:', data);
        if (typeof updateUI === 'function') updateUI(data);
    })
    .catch(err => console.error('Error update-draft:', err));
}

function deleteToDraft(obj) {
    if (!confirm("Bạn có chắc muốn xóa món này?")) return;

    const row = obj.closest('.order-item');
    const select = row.querySelector('.dish-select');
    const idToRemove = select.value;

    const body = document.getElementById('order-items');
    const rows = body.querySelectorAll('.order-item');

    if (idToRemove) {
        fetch('/api/delete-draft/' + idToRemove, {
            method: 'delete',
            headers: {
            'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then(data => {
             if (typeof updateUI === 'function') updateUI(data);
        }).catch(err => console.error(err));
    }

    if (rows.length > 1) {
        row.remove();
    }
    else {
        if (select) select.selectedIndex = 0;
        const qtyInput = row.querySelector('.quantity');
        const priceInp = row.querySelector('.price');
        const amtInp = row.querySelector('.amount');
        
        if (qtyInput) qtyInput.value = 1;
        if (priceInp) priceInp.value = '';
        if (amtInp) amtInp.value = '';
    }
}

function complete() {
    const addressInput = document.getElementById('table');
    const table = addressInput.value;

    const orderNoteInput = document.getElementById('orderNote');
    const orderNote = orderNoteInput.value;

    if (confirm('u sure?') == true) {
        fetch('/api/complete', {
            method: 'post',
            body: JSON.stringify({
                'table': table,
                'note': orderNote
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