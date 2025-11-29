function nextStatus(id) {
    if (confirm("Are you sure?")==true) {
        fetch('/api/employee/orders/next/' + id, {
            method: 'put',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then(data => {
            if (data.code == 200) {
                alert("Chuyen trang thai thành công!");
                location.reload();
            }
            if (data.code == 403) {
                alert("Ban khong co quyen thanh toan");
                location.reload();
            }
        }).catch(err => console.log(err))
    }
}
function cancelStatus(id) {
    if (confirm('Are you sure?') == true) {
        fetch('/api/employee/orders/cancel/' + id, {
            method: 'put',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then(data => {
            if (data.code == 200) {
                alert("Huy don hang thanh cong");
                location.reload();
            }
            if (data.code == 403) {
                alert('Không thể hủy đơn hàng đã Hoàn thành hoặc đã Hủy trước đó!');
                location.reload();
            }
            if (data.code == 400) {
                alert("Khong co quyen huy don hang");
                location.reload();
            }
        }).catch(err => console.log(err))
    }
}