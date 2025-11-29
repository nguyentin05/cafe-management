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

function updateOrder() {
    fetch('api/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            order_id: document.getElementById('order-id').value,
            items: Array.from(document.querySelectorAll('#order-items-body tr'))
                .map(row => ({
                    dish_id: row.dataset.id,
                    quantity: parseInt(row.querySelector('.quantity').value)
                }))
        })
    })
}