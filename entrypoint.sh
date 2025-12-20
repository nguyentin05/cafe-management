#!/bin/bash
set -e

DB_HOST="mysql-db"
DB_PORT=3306

echo "Đang kiểm tra kết nối tới MySQL ($DB_HOST:$DB_PORT)..."

python << END
import socket
import time
import sys

host = "$DB_HOST"
port = $DB_PORT
timeout = 600
start_time = time.time()

while True:
    try:
        with socket.create_connection((host, port), timeout=1):
            break
    except (OSError, ConnectionRefusedError):
        if time.time() - start_time > timeout:
            print("Quá thời gian chờ MySQL!")
            sys.exit(1)
        time.sleep(2)
END

echo "Đang chạy init_db.py..."
python init_db.py

echo "Đang khởi động Server..."
exec python run.py