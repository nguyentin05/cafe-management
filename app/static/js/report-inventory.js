document.addEventListener('DOMContentLoaded', function() {
    initInventorySelect()
})

function initInventorySelect() {
    if (document.getElementById("ingredientSearch")) {
        new TomSelect("#ingredientSearch", {
        create: false,
        sortField: {
            field: "text",
            direction: "asc"
        },
        placeholder: "Chọn hoặc gõ tên nguyên liệu...",
        plugins: ['clear_button']
    })
    }
    return
}
function addToReport(obj) {
    const row = obj.closest('.row')
    const select = row.querySelector('#ingredientSearch')
    const quantityInput = row.querySelector('#quantityInput')
    const value = select.value
    const option = select.selectedOptions[0]

    if (!option || !option.value) {
        alert('Vui lòng chọn nguyên liệu!')
        return
    }

    if (!quantityInput.value || quantityInput.value <= 0) {
        alert('Vui lòng nhập số lượng hợp lệ!')
        quantityInput.focus()
        return
    }

    fetch('/api/employee/report-inventory/add', {
    method: 'post',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        'id': option.value,
        'name': option.textContent,
        'cost': parseInt(option.dataset.cost),
        'unit': option.dataset.unit,
        'quantity': parseFloat(quantityInput.value)
    })
    }).then(res => res.json())
    .then(data => {
        if (data.code === 200) {
            location.reload()
        }
    }).catch(err => console.log(err))
}

function deleteReport(id) {
    if(confirm('Bạn có chắc chắn muốn xóa?')) {
        fetch('/api/employee/report-inventory/' + id + '/delete' , {
            method: 'delete',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then(data => {
            if (data.code == 200) {
                location.reload()
            }
        }).catch(err => console.error(err))
    }
}