function nextStatus(id) {
    if (confirm("Bạn có chắc chắn muốn chuyển trạng thái đơn hàng?")==true) {
        fetch('/api/employee/orders/' + id + '/next', {
            method: 'put',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then(data => {
            if (data.code == 200) {
                alert("Chuyển trạng thái thành công");
                location.reload();
            }
            if (data.code == 403) {
                alert("Không có quyền thanh toán");
                location.reload();
            }
        }).catch(err => console.log(err))
    }
}
function cancelStatus(id) {
    if (confirm('Bạn có chắc chắn muốn hủy đơn hàng?') == true) {
        fetch('/api/employee/orders/' + id + '/cancel', {
            method: 'put',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then(data => {
            if (data.code == 200) {
                alert('Hủy đơn hàng thành công');
                location.reload();
            }
            if (data.code == 403) {
                alert('Không thể hủy đơn hàng đã Hoàn thành hoặc đã Hủy trước đó');
                location.reload();
            }
            if (data.code == 400) {
                alert("Không có quyền hủy đơn hàng");
                location.reload();
            }
        }).catch(err => console.log(err))
    }
}