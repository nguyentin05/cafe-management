function updateRowTotal(input) {

    row = input.closest('tr');
    const price = parseInt(row.dataset.price);
    let quantity = parseInt(input.value);

    if (isNaN(quantity) || quantity < 1) {
        quantity = 1;
        input.value = 1;
    }

    const amount = row.querySelector('.amount');

    amount.value = (price * quantity).toLocaleString();

    updateGrandTotal();
}
function removeRow(btn) {
    if (confirm("Bạn muốn xóa món này?") == true) {
        btn.closest('tr').remove();
        updateGrandTotal();
    }
}
function addDish() {
    const select = document.getElementById('dishSelect');

    if (select.value) {
        const option = select.options[select.selectedIndex];
        const id = option.value;
        const name = option.textContent;
        const price = parseInt(option.dataset.price);

        const existingRow = document.querySelector(`tr[data-id="${id}"]`);

        if (existingRow) {
            const input = existingRow.querySelector('.quantity');
            input.value = parseInt(input.value) + 1;
            updateRowTotal(input);
        } else {
            const tbody = document.getElementById('order-items-body');
            const newRow = document.createElement('tr');
            newRow.dataset.id = id;
            newRow.dataset.price = price;

            newRow.innerHTML = `
                <td>${name}</td>
                <td>
                    <input type="number" class="form-control form-control-sm text-center quantity"
                           value="1" min="1" onblur="updateRowTotal(this)">
                </td>
                <td>
                    <input type="text" class="form-control text-end price"
                           placeholder="${price.toLocaleString()}" disabled>
                </td>
                <td>
                    <input type="text" class="form-control fw-semibold text-end amount"
                           placeholder="${price.toLocaleString()}" disabled>
                </td>
                <td class="text-center">
                    <button type="button" class="btn btn-sm btn-outline-danger"
                            onclick="removeRow(this)">X
                    </button>
                </td>
            `;
            tbody.appendChild(newRow);
            updateGrandTotal();
        }
        select.selectedIndex = 0;
    }
    else {
        alert("Vui lòng chọn một món ăn!");
        return;
    }

}
function updateGrandTotal() {
    let total = 0;
    document.querySelectorAll('#order-items-body tr').forEach(row => {
        const price = parseInt(row.dataset.price);
        const quantityInput = row.querySelector('.quantity');
        const quantity = parseInt(quantityInput.value) || 0;
        total += price * quantity;
    });
    document.getElementById('grand-total').innerText = total.toLocaleString();
}

document.addEventListener("DOMContentLoaded", function() {
    updateGrandTotal();
});

function updateOrder(id) {
    const tableInput = document.getElementById('tableNumber');
    let table = null;
    if (tableInput) {
        table = tableInput.value;

        if (!table) {
            alert("Vui lòng nhập số bàn!");
            return;
        }
    }

    const orderNoteInput = document.getElementById('orderNote');
    const orderNote = orderNoteInput.value;

    const items = [];
    const rows = document.querySelectorAll('#order-items-body tr');

    if (rows.length === 0) {
        alert("Đơn hàng phải có ít nhất 1 món!");
        return;
    }

    rows.forEach(row => {
        items.push({
            id: row.dataset.id,
            price: parseInt(row.dataset.price),
            quantity: parseInt(row.querySelector('.quantity').value)
        });
    })

    fetch('/api/employee/orders/update/' + id, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'table': table,
            'note': orderNote,
            'items': items
        })
    }).then(res => res.json()).then(data => {
        if (data.code == 200) {
            alert('Cập nhật thành công!');
            location.reload();
        }
        else if (data.code == 400) {
            alert(data.message);
        }
    }).catch(err => console.log(err));
}