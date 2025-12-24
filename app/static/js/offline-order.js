let currentCounter = 0

function loadCounter() {
    currentCounter = parseInt(localStorage.getItem("draftCounter")) || 0
}

function saveCounter() {
    localStorage.setItem("draftCounter", currentCounter)
}

function getNextId() {
    currentCounter++
    saveCounter()
    return currentCounter
}

//khởi tạo draft nếu chưa có thì tạo mới
function getDraft() {
    return JSON.parse(localStorage.getItem("draft") || "{}")
}

//lưu draft va cập nhật UI
function saveDraft(draft) {
    localStorage.setItem("draft", JSON.stringify(draft))
    updateUI(draft)
}

//tính số lượng và tổng tiền
function countTotal(draft) {
    let totalQuantity = 0
    let totalAmount = 0

    Object.values(draft).forEach(item => {
        totalQuantity += item.quantity
        totalAmount += item.quantity * item.price
    })

    return { totalQuantity, totalAmount }
}

//
function updateUI(draft) {
    const { totalQuantity, totalAmount } = countTotal(draft)

    const sf = document.getElementById("service-fee")

    const serviceFeeRate = parseFloat(sf.dataset.fee)

    const serviceFee = totalAmount * serviceFeeRate

    const total = totalAmount + serviceFee

    document.querySelectorAll(".subtotal").forEach(element => {
        element.innerText = totalAmount.toLocaleString()
    })

    document.querySelectorAll(".quantity").forEach(element => {
        element.innerText = totalQuantity
    })

    document.querySelectorAll(".serviceFee").forEach(element => {
        element.innerText = serviceFee.toLocaleString()
    })

    document.querySelectorAll(".total").forEach(element => {
        element.innerText = total.toLocaleString()
    })
}


function addRow() {
    const template = document.getElementById("row-template")
    const row = template.content.firstElementChild.cloneNode(true)

    row.dataset.rowId = getNextId()

    row.querySelector(".dish-select").addEventListener("change", () => updateRowToDraft(row))
    row.querySelector(".quantity").addEventListener("blur", () => updateRowToDraft(row))
    row.querySelector(".btn-delete").addEventListener("click", () => deleteRow(row))

    return row
}


function addItemRow() {
    const body = document.getElementById("order-items")
    body.appendChild(addRow())
}
function updateRowToDraft(row) {
    const rowId = row.dataset.rowId
    const select = row.querySelector(".dish-select")
    const qty = row.querySelector(".quantity")

    if (!select.value) {
        return
    }

    const price = parseInt(select.selectedOptions[0].dataset.price)
    const quantity = parseInt(qty.value)

    if (isNaN(quantity) || quantity < 1) {
        quantity = 1
        input.value = 1
    }

    row.querySelector(".price").value = price.toLocaleString()
    row.querySelector(".amount").value = (price * quantity).toLocaleString()

    const draft = getDraft()

    draft[rowId] = {
        id: select.value,
        name: select.selectedOptions[0].textContent.trim(),
        price: price,
        quantity: quantity
    }
    saveDraft(draft)
}
function deleteRow(row) {
    if (confirm("Bạn có chắc muốn xóa món này?")) {
    const rowId = row.dataset.rowId
    let draft = getDraft()

    delete draft[rowId]
    saveDraft(draft)

    row.remove()

    if (document.querySelectorAll(".order-item").length === 0) {
        addItemRow()
    }
    }
}
function renderDraftFromStorage() {
    const body = document.getElementById("order-items")
    const draft = getDraft()

    body.innerHTML = ""

    Object.entries(draft).forEach(([rowId, item]) => {
        const row = addRow()

        row.dataset.rowId = rowId

        row.querySelector(".dish-select").value = item.id
        row.querySelector(".quantity").value = item.quantity
        row.querySelector(".price").value = item.price.toLocaleString()
        row.querySelector(".amount").value = (item.price * item.quantity).toLocaleString()

        body.appendChild(row)
    })

    updateUI(draft)

    if (Object.keys(draft).length === 0) {
        addItemRow()
    }
}
function complete() {
    const table = document.getElementById("table").value
    const note = document.getElementById("orderNote").value
    const draft = getDraft()

    if (!table) {
        alert("Vui lòng nhập số bàn!")
        return
    }

    if (Object.keys(draft).length === 0) {
        alert("Vui lòng chọn ít nhất 1 món!")
        return
    }

    if (confirm("Xác nhận tạo đơn?")) {
        fetch("/api/employee/complete", {
        method: "post",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            table: table,
            note: note,
            draft: draft
        })
    }).then(res => res.json()).then(data => {
        if (data.code === 200) {
            localStorage.removeItem("draft")
            alert("Tạo đơn thành công!")
            location.reload()
        }
        else if (data.code === 400) {
            alert(data.message)
            location.reload()
        }
        }).catch(err => console.error("Error:", err))
    }
}

document.addEventListener("DOMContentLoaded", () => {
    loadCounter()
    renderDraftFromStorage()
})
