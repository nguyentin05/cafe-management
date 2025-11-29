document.addEventListener('DOMContentLoaded', function() {
    initMaterialSelect();
});

function updateMaterialInfo(value) {

    const elements = getElements(document.getElementById('materialSelect'));

    if (value) {

        const selectedOption = elements.select.querySelector(`option[value="${value}"]`);

        if (selectedOption) {

            const name = selectedOption.textContent;
            const unit = selectedOption.dataset.unit;
            const price = parseInt(selectedOption.dataset.price);

            elements.name.value = name;
            elements.unit.value = unit;
            elements.price.value = price;

            elements.quantity.focus();
        }
    } else {
        elements.name.value = '';
        elements.unit.value = '';
        elements.price.value = '';
    }
}

function initMaterialSelect() {
    if (document.getElementById("materialSelect")) {
        new TomSelect("#materialSelect", {
            create: false,
            sortField: {
                field: "text",
                direction: "asc"
            },
            placeholder: "Nhập tên nguyên liệu...",
            plugins: ['clear_button'],
            onChange: updateMaterialInfo
        });
    }
    return;
}

function getElements(obj) {
    const row = obj.closest('.row');

    return {
        row: row,
        select: row.querySelector('#materialSelect'),
        name : row.querySelector('#materialName'),
        unit: row.querySelector('#unitInput'),
        price: row.querySelector('#priceInput'),
        quantity: row.querySelector('#quantityInput ')
    }
}

function addToSession(obj) {
    const elements = getElements(obj);

    if (!elements.select.value) {
        alert("Vui long chọn nguyen lieu!");
        return;
    }

    if (!elements.quantity.value || elements.quantity.value <= 0) {
        alert("Vui long nhap số lượng!");
        elements.quantity.focus();
        return;
    }

    fetch('/api/employee/goods-receipt/add', {
        method: 'post',
        body: JSON.stringify({
            'id': elements.select.value,
            'quantity': parseInt(elements.quantity.value),
            'price': parseInt(elements.price.value),
            'name': elements.name.value,
            'unit': elements.unit.value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json())
    .then(data => {
        if (data.code == 200) {
            if(elements.select.tomselect) {
            elements.select.tomselect.clear();
            }
              elements.quantity.value = '';
              location.reload();
        }
    })
}
function deleteSession(id) {
    if(confirm('Are you sure?')) {
        fetch('/api/employee/goods-receipt/delete/' + id, {
            method: 'delete',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then(data => {
            if (data.code == 200) {
                alert('xoa thanh cong')
                location.reload();
            }
        }).catch(err => console.error(err));
    }
}

function saveGoodsReceipt() {

}