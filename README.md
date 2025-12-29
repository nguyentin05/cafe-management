# Quản lý quán coffee

---
<div align="center">
    <img src="./images/cafe-architecture.png" alt="Kiến trúc hệ thống" width="100%">
    <br>
    <i>System Architecture</i>
</div>

---
## 🛠 Tech Stack

Dự án được xây dựng dựa trên các công nghệ và thư viện hiện đại để đảm bảo hiệu năng và khả năng mở rộng:

### Backend & Database
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)

### Frontend & UI
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![Bootstrap 5](https://img.shields.io/badge/bootstrap-%23563D7C.svg?style=for-the-badge&logo=bootstrap&logoColor=white)
![Chart.js](https://img.shields.io/badge/chart.js-F5788D.svg?style=for-the-badge&logo=chart.js&logoColor=white)

### DevOps & Tools
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Astah](https://img.shields.io/badge/Astah-UML-blue?style=for-the-badge)

### Services
![Cloudinary](https://img.shields.io/badge/Cloudinary-3448C5?style=for-the-badge&logo=cloudinary&logoColor=white)
![MoMo](https://img.shields.io/badge/MoMo-%23A50064.svg?style=for-the-badge&logo=momo&logoColor=white)

---

## 🛡️ Role-Based Access Control (RBAC)

```text
USER_ROLES
├── Admin
├── Customer
└── Employee
    ├── Manager
    ├── Cashier
    └── Waiter
```
---

## 📐 System Modeling

Hệ thống được phân tích và thiết kế chi tiết bằng công cụ **Astah**. Các tài liệu thiết kế bao gồm:

### 1. Structure Diagram
* **1.1. Use Case Diagram**
* **1.2. Class Diagram**
* **1.3. Object Diagram**
* **1.4. Package Diagram**
* **1.5. Implementation Diagram**
    * 1.5.1. Component Diagram
    * 1.5.2. Deploy Diagram

### 2. Interaction Diagram
* **2.1. Sequence Diagram**
* **2.2. Community Diagram**

### 3. Flowchart
* **3.1. Activity Diagram**
* **3.2. State Diagram**

### 4. Database
* **Entity Relationship Diagram (ERD)**

---

## 📂 Project Structure

```text
my-project/
├── app/
│   ├── controllers/
│   ├── daos/
│   ├── models/
│   ├── static/
│   ├── templates/
│   └── ...
│
├── docker-compose.yml
├── auto_submit_report.py
├── Dockerfile
├── entrypoint.sh
├── requirements.txt
├── run.py
├── initdb.py
├── .env
└── ...
```
[🔗 Link báo cáo](https://docs.google.com/document/d/15nWI9YdeIARDgWQJ-SCU5-yRNv5mMneK1sZlB87JABA/edit?usp=sharing)
 
[🔗 Link web](https://trongtin2005.pythonanywhere.com/)(có thể lúc bạn xem nó đã die do kinh phí ko cho phép:D)

