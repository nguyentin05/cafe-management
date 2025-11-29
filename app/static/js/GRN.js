document.addEventListener('DOMContentLoaded', function() {
    flatpickr(".datepicker", {
        dateFormat: "d/m/Y",
        defaultDate: new Date()
    });

    const ingredientsData = [
        { id: 'sugar', name: 'Đường', unit: 'kg' },
        { id: 'milk', name: 'Sữa tươi', unit: 'lít' },
        { id: 'coffee_beans', name: 'Hạt cà phê', unit: 'kg' },
        { id: 'syrup_vanilla', name: 'Syrup Vani', unit: 'chai' },
        { id: 'ice_cubes', name: 'Đá viên', unit: 'bao' },
        { id: 'cup_small', name: 'Ly nhỏ', unit: 'cái' },
    ];

    let storedGRNs = [
        {
            id: 'GRN-20231026001',
            date: '26/10/2023',
            supplier: 'NCC A',
            items: [{ ingredientId: 'sugar', name: 'Đường', unit: 'kg', quantity: 10 }]
        },
        {
            id: 'GRN-20231027002',
            date: '27/10/2023',
            supplier: 'NCC B',
            items: [{ ingredientId: 'coffee_beans', name: 'Hạt cà phê', unit: 'kg', quantity: 20 }]
        },
    ];

    const grnDateInput = document.getElementById('grnDate');
    const grnCodeInput = document.getElementById('grnCode');
    const supplierNameInput = document.getElementById('supplierName');
    const addIngredientRowBtn = document.getElementById('addIngredientRowBtn');
    const ingredientRowsContainer = document.getElementById('ingredientRowsContainer');
    const totalQuantitySpan = document.getElementById('totalQuantity');
    const saveGRNBtn = document.getElementById('saveGRNBtn');
    const filterStartDateInput = document.getElementById('filterStartDate');
    const filterEndDateInput = document.getElementById('filterEndDate');
    const filterGRNsBtn = document.getElementById('filterGRNsBtn');
    const grnResultsContainer = document.getElementById('grnResultsContainer');

    let currentGRNItems = [];

    function generateUniqueRowId() {
        return 'row_' + Date.now() + '_' + Math.floor(Math.random() * 1000);
    }

    function calculateTotalQuantity() {
        let totalQty = 0;
        currentGRNItems.forEach(item => {
            totalQty += parseInt(item.quantity) || 0;
        });
        totalQuantitySpan.textContent = totalQty;
    }

    function getIngredientOptionsHtml(selectedId = '') {
        return `
            <option value="">Chọn nguyên liệu...</option>
            ${ingredientsData.map(ing => `
                <option value="${ing.id}" ${selectedId === ing.id ? 'selected' : ''} data-unit="${ing.unit}">
                    ${ing.name}
                </option>
            `).join('')}
        `;
    }

    function renderIngredientRow(item = {}) {
        const rowId = item.rowId || generateUniqueRowId();
        const selectedIngredient = ingredientsData.find(ing => ing.id === item.ingredientId);
        const unitDisplay = selectedIngredient ? selectedIngredient.unit : '';
        const quantity = item.quantity || 1;

        const newRow = document.createElement('div');
        newRow.classList.add('d-flex', 'align-items-center', 'py-2', 'border-bottom', 'ingredient-row');
        newRow.dataset.rowId = rowId;

        newRow.innerHTML = `
            <div style="width: 40%;">
                <select class="form-select ingredient-select">
                    ${getIngredientOptionsHtml(item.ingredientId)}
                </select>
            </div>
            <div style="width: 20%;" class="text-center">
                <div class="input-group input-group-sm mx-auto qty-input-group">
                    <button class="btn btn-outline-secondary btn-qty-minus" type="button">-</button>
                    <input type="number" class="form-control text-center qty-input" value="${quantity}" min="1">
                    <button class="btn btn-outline-secondary btn-qty-plus" type="button">+</button>
                </div>
            </div>
            <div style="width: 20%; text-align: center;">
                <span class="unit-display">${unitDisplay}</span>
            </div>
            <div style="width: 20%; text-align: right;">
                <button class="btn btn-sm btn-outline-danger remove-item-btn"><i class="fas fa-times"></i></button>
            </div>
        `;

        ingredientRowsContainer.appendChild(newRow);

        currentGRNItems.push({
            rowId: rowId,
            ingredientId: item.ingredientId || '',
            name: selectedIngredient ? selectedIngredient.name : '',
            unit: unitDisplay,
            quantity: quantity
        });

        const selectElement = newRow.querySelector('.ingredient-select');
        const qtyInputElement = newRow.querySelector('.qty-input');
        const removeButton = newRow.querySelector('.remove-item-btn');
        const unitSpan = newRow.querySelector('.unit-display');
        const btnMinus = newRow.querySelector('.btn-qty-minus');
        const btnPlus = newRow.querySelector('.btn-qty-plus');

        selectElement.addEventListener('change', function() {
            const selectedOption = this.options[this.selectedIndex];
            const newIngredientId = this.value;
            const newUnit = selectedOption.dataset.unit || '';
            const newName = selectedOption.textContent.trim();

            unitSpan.textContent = newUnit;

            const itemIndex = currentGRNItems.findIndex(i => i.rowId === rowId);
            if (itemIndex > -1) {
                currentGRNItems[itemIndex].ingredientId = newIngredientId;
                currentGRNItems[itemIndex].name = newName;
                currentGRNItems[itemIndex].unit = newUnit;
            }
            calculateTotalQuantity();
        });
        qtyInputElement.addEventListener('input', function() {
            let value = parseInt(this.value);
            if (isNaN(value) || value < 1) {
                value = 1;
                this.value = 1;
            }
            const itemIndex = currentGRNItems.findIndex(i => i.rowId === rowId);
            if (itemIndex > -1) {
                currentGRNItems[itemIndex].quantity = value;
            }
            calculateTotalQuantity();
        });
        btnMinus.addEventListener('click', function() {
            let value = parseInt(qtyInputElement.value);
            if (!isNaN(value) && value > 1) {
                qtyInputElement.value = value - 1;
                qtyInputElement.dispatchEvent(new Event('input')); // Trigger input event
            }
        });
        btnPlus.addEventListener('click', function() {
            let value = parseInt(qtyInputElement.value);
            if (isNaN(value)) {
                value = 0;
            }
            qtyInputElement.value = value + 1;
            qtyInputElement.dispatchEvent(new Event('input')); // Trigger input event
        });
        removeButton.addEventListener('click', function() {
            removeIngredientRow(rowId);
        });

        calculateTotalQuantity();
    }

    function removeIngredientRow(rowIdToRemove) {
        const rowElement = ingredientRowsContainer.querySelector(`[data-row-id="${rowIdToRemove}"]`);
        if (rowElement) {
            rowElement.remove();
            currentGRNItems = currentGRNItems.filter(item => item.rowId !== rowIdToRemove);
            calculateTotalQuantity();
        }
    }

    function renderGRNList(grns) {
        grnResultsContainer.innerHTML = '';
        if (grns.length === 0) {
            grnResultsContainer.innerHTML = `<div class="alert alert-warning text-center">Không tìm thấy GRN nào trong khoảng thời gian này.</div>`;
            return;
        }
        grns.forEach(grn => {
            const grnElement = document.createElement('div');
            grnElement.classList.add('grn-list-item', 'mb-2');
            grnElement.innerHTML = `
                <div><strong>Mã GRN:</strong> ${grn.id}</div>
                <div><strong>Ngày:</strong> ${grn.date}</div>
                <div><strong>NCC:</strong> ${grn.supplier}</div>
                <div class="grn-details mt-2 border-top pt-2">
                    <small class="text-muted">Chi tiết:</small>
                    <ul>
                        ${grn.items.map(item => `
                            <li>${item.name}: ${item.quantity} ${item.unit}</li>
                        `).join('')}
                    </ul>
                </div>
            `;
            grnResultsContainer.appendChild(grnElement);
        });
    }
    function resetGRNForm() {
        flatpickr(grnDateInput, {}).setDate(new Date(), true);

        const now = new Date();
        const ymdhis = flatpickr.formatDate(now, "YmdHis");
        grnCodeInput.value = 'GRN-' + ymdhis;

        supplierNameInput.value = '';
        ingredientRowsContainer.innerHTML = '';
        currentGRNItems = [];
        calculateTotalQuantity();
        renderIngredientRow();
    }

    // --- Event Listeners ---
    addIngredientRowBtn.addEventListener('click', function() {
        renderIngredientRow();
    });

    saveGRNBtn.addEventListener('click', function() {
        const grnDate = grnDateInput.value;
        const grnCode = grnCodeInput.value;
        const supplierName = supplierNameInput.value;

        if (!grnDate || !grnCode || !supplierName.trim()) {
            alert('Vui lòng điền đầy đủ thông tin GRN (Ngày, Mã, NCC)!');
            return;
        }

        if (currentGRNItems.length === 0) {
            alert('Vui lòng thêm ít nhất một nguyên liệu vào GRN!');
            return;
        }

        const isValid = currentGRNItems.every(item => item.ingredientId && item.quantity > 0);
        if (!isValid) {
            alert('Vui lòng chọn nguyên liệu và nhập số lượng hợp lệ cho tất cả các dòng!');
            return;
        }

        const newGRN = {
            id: grnCode,
            date: grnDate,
            supplier: supplierName,
            items: currentGRNItems.map(item => ({
                ingredientId: item.ingredientId,
                name: item.name,
                unit: item.unit,
                quantity: item.quantity
            }))
        };

        storedGRNs.push(newGRN);
        alert('Lưu GRN thành công: ' + newGRN.id);

        resetGRNForm();
    });

    filterGRNsBtn.addEventListener('click', function() {
        const startDateStr = filterStartDateInput.value;
        const endDateStr = filterEndDateInput.value;

        if (!startDateStr || !endDateStr) {
            alert('Vui lòng chọn cả "Từ ngày" và "Đến ngày" để lọc!');
            return;
        }

        const parseDate = (dateStr) => {
            const [day, month, year] = dateStr.split('/').map(Number);
            return new Date(year, month - 1, day);
        };

        const startDate = parseDate(startDateStr);
        startDate.setHours(0, 0, 0, 0);
        const endDate = parseDate(endDateStr);
        endDate.setHours(23, 59, 59, 999);

        const filteredGRNs = storedGRNs.filter(grn => {
            const grnDate = parseDate(grn.date);
            grnDate.setHours(12, 0, 0, 0);
            return grnDate >= startDate && grnDate <= endDate;
        });

        renderGRNList(filteredGRNs);
    });
    resetGRNForm();
});