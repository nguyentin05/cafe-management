let currentCounter = 0;

document.addEventListener("DOMContentLoaded", function() {
    renderDraftFromStorage();
});

function getNextId() {
    return ++currentCounter;
}
function getDraft() {
    const draft = localStorage.getItem('draft');

    if (draft) {
        return JSON.parse(draft);
    }
    return {};
}
function saveDraft(draft) {
    localStorage.setItem('draft', JSON.stringify(draft));
    updateUI(draft);
}
function updateUI(draft) {
    const { totalQuantity, totalAmount } = countTotal(draft)
    let items = document.getElementsByClassName("draftCounter");
    for (let item of items)
        item.innerText = totalQuantity;

    let amounts = document.getElementsByClassName("draftAmount");
    for (let item of amounts)
        item.innerText = totalAmount.toLocaleString();
}
function countTotal(draft) {
    let totalQuantity = 0;
    let totalAmount = 0;

    if (draft) {
        Object.values(draft).forEach(item => {
            totalQuantity += item.quantity;
            totalAmount += item.quantity * item.price;
        });
    }
    return { totalQuantity, totalAmount };
}
function renderDraftFromStorage() {
    const draft = getDraft();
    const entries = Object.entries(draft);

    updateUI(draft);

    if (entries.length > 0) {
        const body = document.getElementById('order-items');
        const firstRow = body.querySelector('.order-item');

        body.innerHTML = '';

        entries.forEach(([rowId, item]) => {
        const row = firstRow.cloneNode(true);

        row.dataset.rowId = rowId;

        const select = row.querySelector('.dish-select');
        const quantityInput = row.querySelector('.quantity');
        const priceInput = row.querySelector('.price');
        const amountInput = row.querySelector('.amount');

        select.value = item.id;
        quantityInput.value = item.quantity;
        priceInput.value = item.price.toLocaleString();
        amountInput.value = (item.price * item.quantity).toLocaleString();

        body.appendChild(row);
        });
    }
}
function addItemRow() {
    const body = document.getElementById('order-items');
    const firstRow = body.querySelector('.order-item');

    if (!firstRow) {
        location.reload();
        return;
    }

    const row = firstRow.cloneNode(true);

    const select = row.querySelector('.dish-select');
    const quantityInput = row.querySelector('.quantity');
    const priceInput = row.querySelector('.price');
    const amountInput = row.querySelector('.amount');

    row.dataset.rowId = getNextId();

    select.selectedIndex = 0;
    quantityInput.value = 1;
    priceInput.value = '';
    amountInput.value = '';

    body.appendChild(row);
}
function getAndUpdateItem(obj) {
    const row = obj.closest('tr');

    let rowId = row.dataset.rowId;
    if (!rowId) {
        rowId = getNextId();
        row.dataset.rowId = rowId;
    }

    const select = row.querySelector('.dish-select');
    const quantityInput = row.querySelector('.quantity');
    const priceInput = row.querySelector('.price');
    const amountInput = row.querySelector('.amount');

    const option = select.selectedOptions[0];

    const price = parseInt(option.dataset.price);
    let quantity = parseInt(quantityInput.value);

    priceInput.value = price.toLocaleString();
    amountInput.value = (price * quantity).toLocaleString();

    return {
        rowId: rowId,
        item: {
            id: option.value,
            name: option.textContent,
            price: price,
            quantity: quantity
        }
    };
}

function addToDraft(obj) {
    const { rowId, item } = getAndUpdateItem(obj);

    if (rowId && item) {
        const draft = getDraft();

        draft[rowId] = item;

        saveDraft(draft);
    }

}
function updateToDraft(obj) {
    addToDraft(obj);
}
function deleteToDraft(obj) {
    if (confirm("Bạn có chắc muốn xóa món này?") == True) {
        const row = obj.closest('tr');
        const rowId = row.dataset.rowId;

        const draft = getDraft();

        if (rowId && rowId in draft) {
            delete draft[rowId];
            saveDraft(draft);
        }

        const body = document.getElementById('order-items');
        const rows = body.querySelectorAll('.order-item');
        const select = body.querySelector('.dish-select');

        if (rows.length > 1) {
            row.remove();
        } else {
            select.selectedIndex = 0;
            row.querySelector('.quantity').value = 1;
            row.querySelector('.price').value = '';
            row.querySelector('.amount').value = '';
        }
    }
}
function complete() {
    const tableInput = document.getElementById('table');
    const table = tableInput.value;

    if (!table) {
        alert("Vui lòng nhập số bàn!");
        return;
    }

    const orderNoteInput = document.getElementById('orderNote');
    const orderNote = orderNoteInput.value;

    const draft = getDraft();

    if (Object.keys(draft).length === 0) {
        alert("Vui lòng chọn món ăn!");
        return;
    }

    if (confirm('Xác nhận tạo đơn?') == true) {
        fetch('/api/employee/complete', {
            method: 'post',
            body: JSON.stringify({
                'draft': draft,
                'table': table,
                'note': orderNote
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then(data => {
            if (data.code == 200) {
                localStorage.removeItem('draft');
                alert("Tạo đơn thành công!");
                location.reload();
            } else {
                alert("Có lỗi xảy ra: " + (data.message || "Lỗi hệ thống"));
            }
        }).catch(err => console.error(err));
    }
}