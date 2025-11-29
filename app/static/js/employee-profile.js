document.addEventListener('DOMContentLoaded', function() {
    const employeesData = [
        // Admin
        { id: 1, fullname: 'Nguyễn Văn A', email: 'vana.admin@example.com', avatar: 'https://i.pravatar.cc/150?img=1', phone: '0912345671', active: true, joined_date: '2023-01-15', user_role: 'ADMIN', employee_role: null, display_role: 'Admin', gender: 'Male', address: '123 Đường Nguyễn Huệ, Quận 1, TP. Hồ Chí Minh' },
        { id: 2, fullname: 'Trần Thị B', email: 'thib.manager@example.com', avatar: 'https://i.pravatar.cc/150?img=2', phone: '0912345672', active: true, joined_date: '2023-02-20', user_role: 'EMPLOYEE', employee_role: 'MANAGER', display_role: 'Manager', gender: 'Female', address: '456 Đường Lê Lợi, Quận 1, TP. Hồ Chí Minh' },
        { id: 3, fullname: 'Lê Văn C', email: 'vanc.waiter@example.com', avatar: 'https://i.pravatar.cc/150?img=3', phone: '0912345673', active: true, joined_date: '2023-03-10', user_role: 'EMPLOYEE', employee_role: 'WAITER', display_role: 'Waiter', gender: 'Male', address: '789 Đường Đồng Khởi, Quận 1, TP. Hồ Chí Minh' },
        { id: 4, fullname: 'Phạm Thị D', email: 'thid.cashier@example.com', avatar: 'https://i.pravatar.cc/150?img=4', phone: '0912345674', active: false, joined_date: '2023-04-01', user_role: 'EMPLOYEE', employee_role: 'CASHIER', display_role: 'Cashier', gender: 'Female', address: '101 Đường Pasteur, Quận 3, TP. Hồ Chí Minh' },
        { id: 5, fullname: 'Hoàng Văn E', email: 'vane.waiter@example.com', avatar: 'https://i.pravatar.cc/150?img=5', phone: '0912345675', active: true, joined_date: '2023-05-05', user_role: 'EMPLOYEE', employee_role: 'WAITER', display_role: 'Waiter', gender: 'Male', address: '202 Đường Lý Tự Trọng, Quận 1, TP. Hồ Chí Minh' },
        { id: 6, fullname: 'Nguyễn Thị F', email: 'thif.manager@example.com', avatar: 'https://i.pravatar.cc/150?img=6', phone: '0912345676', active: true, joined_date: '2023-06-12', user_role: 'EMPLOYEE', employee_role: 'MANAGER', display_role: 'Manager', gender: 'Female', address: '303 Đường Hai Bà Trưng, Quận 1, TP. Hồ Chí Minh' },
        { id: 7, fullname: 'Trần Văn G', email: 'vang.cashier@example.com', avatar: 'https://i.pravatar.cc/150?img=7', phone: '0912345677', active: false, joined_date: '2023-07-01', user_role: 'EMPLOYEE', employee_role: 'CASHIER', display_role: 'Cashier', gender: 'Male', address: '404 Đường Cao Thắng, Quận 3, TP. Hồ Chí Minh' },
        { id: 8, fullname: 'Lê Thị H', email: 'thih.admin@example.com', avatar: 'https://i.pravatar.cc/150?img=8', phone: '0912345678', active: true, joined_date: '2023-08-18', user_role: 'ADMIN', employee_role: null, display_role: 'Admin', gender: 'Female', address: '505 Đường Điện Biên Phủ, Quận Bình Thạnh, TP. Hồ Chí Minh' },
        { id: 9, fullname: 'Phạm Văn I', email: 'vani.waiter@example.com', avatar: 'https://i.pravatar.cc/150?img=9', phone: '0912345679', active: true, joined_date: '2023-09-22', user_role: 'EMPLOYEE', employee_role: 'WAITER', display_role: 'Waiter', gender: 'Male', address: '606 Đường Trần Hưng Đạo, Quận 5, TP. Hồ Chí Minh' },
        { id: 10, fullname: 'Hoàng Thị K', email: 'thik.manager@example.com', avatar: 'https://i.pravatar.cc/150?img=10', phone: '0912345680', active: true, joined_date: '2023-10-30', user_role: 'EMPLOYEE', employee_role: 'MANAGER', display_role: 'Manager', gender: 'Female', address: '707 Đường Nguyễn Đình Chiểu, Quận 3, TP. Hồ Chí Minh' },
        { id: 11, fullname: 'Nguyễn Văn L', email: 'vanl.cashier@example.com', avatar: 'https://i.pravatar.cc/150?img=11', phone: '0912345681', active: true, joined_date: '2023-11-10', user_role: 'EMPLOYEE', employee_role: 'CASHIER', display_role: 'Cashier', gender: 'Male', address: '808 Đường Cách Mạng Tháng 8, Quận 3, TP. Hồ Chí Minh' },
        { id: 12, fullname: 'Trần Thị M', email: 'thim.waiter@example.com', avatar: 'https://i.pravatar.cc/150?img=12', phone: '0912345682', active: false, joined_date: '2023-12-01', user_role: 'EMPLOYEE', employee_role: 'WAITER', display_role: 'Waiter', gender: 'Female', address: '909 Đường Sư Vạn Hạnh, Quận 10, TP. Hồ Chí Minh' },
        { id: 13, fullname: 'Lê Văn N', email: 'vann.admin@example.com', avatar: 'https://i.pravatar.cc/150?img=13', phone: '0912345683', active: true, joined_date: '2024-01-05', user_role: 'ADMIN', employee_role: null, display_role: 'Admin', gender: 'Male', address: '111 Đường Trương Định, Quận 3, TP. Hồ Chí Minh' },
        { id: 14, fullname: 'Phạm Thị P', email: 'thip.manager@example.com', avatar: 'https://i.pravatar.cc/150?img=14', phone: '0912345684', active: true, joined_date: '2024-02-14', user_role: 'EMPLOYEE', employee_role: 'MANAGER', display_role: 'Manager', gender: 'Female', address: '222 Đường Võ Văn Tần, Quận 3, TP. Hồ Chí Minh' },
        { id: 15, fullname: 'Hoàng Văn Q', email: 'vanq.cashier@example.com', avatar: 'https://i.pravatar.cc/150?img=15', phone: '0912345685', active: true, joined_date: '2024-03-20', user_role: 'EMPLOYEE', employee_role: 'CASHIER', display_role: 'Cashier', gender: 'Male', address: '333 Đường Ba Tháng Hai, Quận 10, TP. Hồ Chí Minh' }
    ];

    let filteredEmployees = [...employeesData];
    let currentPage = 1;
    let rowsPerPage = parseInt(document.getElementById('rowsPerPage').value);

    const employeeTableBody = document.getElementById('employeeTableBody');
    const paginationElement = document.getElementById('pagination');
    const entriesInfoElement = document.getElementById('entriesInfo');
    const searchInput = document.getElementById('searchInput');
    const statusFilter = document.getElementById('statusFilter');
    const rowsPerPageSelect = document.getElementById('rowsPerPage');

    function renderTable() {
        employeeTableBody.innerHTML = ''; // Xóa nội dung bảng cũ
        const start = (currentPage - 1) * rowsPerPage;
        const end = start + rowsPerPage;
        const paginatedItems = filteredEmployees.slice(start, end);

        if (paginatedItems.length === 0) {
            employeeTableBody.innerHTML = `<tr><td colspan="11" class="text-center py-4">Không tìm thấy nhân viên nào.</td></tr>`;
            entriesInfoElement.textContent = `0-0 trên ${filteredEmployees.length} mục`;
            renderPagination(0);
            return;
        }

        paginatedItems.forEach(employee => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td class="ps-4"><input type="checkbox" class="form-check-input"></td>
                <td>${employee.id}</td>
                <td>
                    <div class="d-flex align-items-center">
                        <img src="${employee.avatar}" class="employee-avatar me-2" alt="Avatar">
                        <span>${employee.fullname}</span>
                    </div>
                </td>
                <td>${employee.display_role}</td> {# Sử dụng display_role để hiển thị vai trò #}
                <td>${employee.email}</td>
                <td>${employee.phone}</td>
                <td>${employee.joined_date}</td>
                <td><span class="badge ${employee.active ? 'bg-success status-active' : 'bg-danger status-inactive'} rounded-pill">${employee.active ? 'Active' : 'Inactive'}</span></td>
                <td>${employee.gender || 'N/A'}</td>
                <td>${employee.address || 'N/A'}</td>
                <td class="text-center">
                    <button class="btn btn-sm btn-action rounded-circle"><i class="fas fa-eye"></i></button>
                    <button class="btn btn-sm btn-action rounded-circle"><i class="fas fa-pencil-alt"></i></button>
                    <button class="btn btn-sm btn-action rounded-circle"><i class="fas fa-trash-alt"></i></button>
                </td>
            `;
            employeeTableBody.appendChild(row);
        });

        const currentStart = filteredEmployees.length === 0 ? 0 : start + 1;
        const currentEnd = Math.min(end, filteredEmployees.length);
        entriesInfoElement.textContent = `${currentStart}-${currentEnd} trên ${filteredEmployees.length} mục`;

        renderPagination(filteredEmployees.length);
    }

    function renderPagination(totalItems) {
        paginationElement.innerHTML = ''; // Xóa phân trang cũ
        const totalPages = Math.ceil(totalItems / rowsPerPage);

        if (totalPages <= 1) return;

        const prevLi = document.createElement('li');
        prevLi.classList.add('page-item', 'prev-page');
        if (currentPage === 1) prevLi.classList.add('disabled');
        prevLi.innerHTML = `<a class="page-link" href="#" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a>`;
        prevLi.addEventListener('click', function(e) {
            e.preventDefault();
            if (currentPage > 1) {
                currentPage--;
                renderTable();
            }
        });
        paginationElement.appendChild(prevLi);

        for (let i = 1; i <= totalPages; i++) {
            const pageLi = document.createElement('li');
            pageLi.classList.add('page-item');
            if (i === currentPage) pageLi.classList.add('active');
            pageLi.innerHTML = `<a class="page-link" href="#">${i}</a>`;
            pageLi.addEventListener('click', function(e) {
                e.preventDefault();
                currentPage = i;
                renderTable();
            });
            paginationElement.appendChild(pageLi);
        }
        const nextLi = document.createElement('li');
        nextLi.classList.add('page-item', 'next-page');
        if (currentPage === totalPages) nextLi.classList.add('disabled');
        nextLi.innerHTML = `<a class="page-link" href="#" aria-label="Next"><span aria-hidden="true">&raquo;</span></a>`;
        nextLi.addEventListener('click', function(e) {
            e.preventDefault();
            if (currentPage < totalPages) {
                currentPage++;
                renderTable();
            }
        });
        paginationElement.appendChild(nextLi);
    }

    function applyFilters() {
        const searchTerm = searchInput.value.toLowerCase();
        const status = statusFilter.value;

        filteredEmployees = employeesData.filter(employee => {
            const matchesSearch = employee.fullname.toLowerCase().includes(searchTerm) ||
                                  employee.email.toLowerCase().includes(searchTerm) ||
                                  employee.phone.includes(searchTerm) ||
                                  (employee.display_role && employee.display_role.toLowerCase().includes(searchTerm)) ||
                                  (employee.address && employee.address.toLowerCase().includes(searchTerm));

            const matchesStatus = status === '' ||
                                  (status === 'true' && employee.active === true) ||
                                  (status === 'false' && employee.active === false);

            return matchesSearch && matchesStatus;
        });
        currentPage = 1;
        renderTable();
    }

    // Event Listeners
    searchInput.addEventListener('input', applyFilters);
    statusFilter.addEventListener('change', applyFilters);
    rowsPerPageSelect.addEventListener('change', function() {
        rowsPerPage = parseInt(this.value);
        currentPage = 1;
        renderTable();
    });
    renderTable();
});