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
            const cost = parseInt(selectedOption.dataset.cost);

            elements.name.value = name;
            elements.unit.value = unit;
            elements.cost.value = cost.toLocaleString();

            elements.quantity.focus();
        }
    } else {
        elements.name.value = '';
        elements.unit.value = '';
        elements.cost.value = '';
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
        cost: row.querySelector('#costInput'),
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
            'name': elements.name.value,
            'unit': elements.unit.value,
            'cost': parseInt(elements.cost.value.replace(/,/g,'')),
            'quantity': parseInt(elements.quantity.value)
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
                location.reload();
            }
        }).catch(err => console.error(err));
    }
}
function saveGoodsReceipt() {
    if(confirm('Are you sure?')) {
        fetch('/api/employee/goods-receipt/save', {
        method: 'post',
        headers: {
            'Content-Type': 'application/json'
        }
        }).then(res => res.json()).then(data => {
        if (data.code == 200) {
            alert("Tạo đơn thành công!");
            location.reload();
        }
        }).catch(err => console.error(err));
    }
}