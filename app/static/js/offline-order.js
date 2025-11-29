let currentCounter = 0;

function loadCounter() {
    currentCounter = parseInt(localStorage.getItem("draftCounter")) || 0;
}
function saveCounter() {
    localStorage.setItem("draftCounter", currentCounter);
}
function getNextId() {
    currentCounter++;
    saveCounter();
    return currentCounter;
}
function getDraft() {
    return JSON.parse(localStorage.getItem("draft") || "{}");
}

function saveDraft(draft) {
    localStorage.setItem("draft", JSON.stringify(draft));
    updateUI(draft);
}
function countTotal(draft) {
    let totalQuantity = 0;
    let totalAmount = 0;

    Object.values(draft).forEach(item => {
        totalQuantity += item.quantity;
        totalAmount += item.quantity * item.price;
    });

    return { totalQuantity, totalAmount };
}
function updateUI(draft) {
    const { totalQuantity, totalAmount } = countTotal(draft);

    const sf = document.getElementById("service-fee");

    const serviceFeeRate = parseFloat(sf.dataset.fee);

    const serviceFee = totalAmount * serviceFeeRate;

    const total = totalAmount + serviceFee;

    document.querySelectorAll(".subtotal").forEach(el => {
        el.innerText = totalAmount.toLocaleString();
    });

    document.querySelectorAll(".quantity").forEach(el => {
        el.innerText = totalQuantity;
    });

    document.querySelectorAll(".serviceFee").forEach(el => {
        el.innerText = serviceFee.toLocaleString();
    });

    document.querySelectorAll(".total").forEach(el => {
        el.innerText = total.toLocaleString();
    });
}
function createRow() {
    const tpl = document.getElementById("row-template");
    const row = tpl.content.firstElementChild.cloneNode(true);

    row.dataset.rowId = getNextId();

    row.querySelector(".dish-select").addEventListener("change", () => updateRowToDraft(row));
    row.querySelector(".quantity").addEventListener("blur", () => updateRowToDraft(row));
    row.querySelector(".btn-delete").addEventListener("click", () => deleteRow(row));

    return row;
}
function addItemRow() {
    const body = document.getElementById("order-items");
    body.appendChild(createRow());
}
function updateRowToDraft(row) {
    const rowId = row.dataset.rowId;
    const select = row.querySelector(".dish-select");
    const qty = row.querySelector(".quantity");

    if (!select.value) {
        return;
    }

    const price = parseInt(select.selectedOptions[0].dataset.price);
    const quantity = parseInt(qty.value);

    if (isNaN(quantity) || quantity < 1) {
        quantity = 1;
        input.value = 1;
    }

    row.querySelector(".price").value = price.toLocaleString();
    row.querySelector(".amount").value = (price * quantity).toLocaleString();

    const draft = getDraft();

    draft[rowId] = {
        id: select.value,
        name: select.selectedOptions[0].textContent.trim(),
        price: price,
        quantity: quantity
    };
    saveDraft(draft);
}
function deleteRow(row) {
    if (!confirm("Bạn có chắc muốn xóa món này?")) return;

    const rowId = row.dataset.rowId;
    let draft = getDraft();

    delete draft[rowId];
    saveDraft(draft);

    row.remove();

    if (document.querySelectorAll(".order-item").length === 0) {
        addItemRow();
    }
}
function renderDraftFromStorage() {
    const body = document.getElementById("order-items");
    const draft = getDraft();

    body.innerHTML = "";

    Object.entries(draft).forEach(([rowId, item]) => {
        const row = createRow();

        row.dataset.rowId = rowId;

        row.querySelector(".dish-select").value = item.id;
        row.querySelector(".quantity").value = item.quantity;
        row.querySelector(".price").value = item.price.toLocaleString();
        row.querySelector(".amount").value = (item.price * item.quantity).toLocaleString();

        body.appendChild(row);
    });

    updateUI(draft);

    if (Object.keys(draft).length === 0) {
        addItemRow();
    }
}
function complete() {
    const table = document.getElementById("table").value;
    const note = document.getElementById("orderNote").value;
    const draft = getDraft();

    if (!table) {
        alert("Vui lòng nhập số bàn!");
        return;
    }

    if (Object.keys(draft).length === 0) {
        alert("Vui lòng chọn ít nhất 1 món!");
        return;
    }

    if (!confirm("Xác nhận tạo đơn?")) {
        return;
    }

    fetch("/api/employee/complete", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            table: table,
            note: note,
            draft: draft
        })
    })
        .then(res => res.json())
        .then(data => {
            if (data.code === 200) {
                localStorage.removeItem("draft");
                alert("Tạo đơn thành công!");
                location.reload();
            }
            else if (data.code === 400) {
                alert(data.message);
                location.reload();
            }
        })
        .catch(err => console.error("Error:", err));
}
document.addEventListener("DOMContentLoaded", () => {
    loadCounter();
    renderDraftFromStorage();
});
