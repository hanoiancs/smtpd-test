# smtpd-test

## Giới thiệu:

`smtp-test` là hệ thống bao gồm 1 SMTP Server và Web UI phục vụ cho việc test gửi email.
## Cài đặt:
### Yêu cầu:
    0. Ubuntu 20.04 (python3)
    1. Python: 3.8
    2. MongoDB: 4.x
### Cài đặt MongoDB với `docker-compose`:

File `docker-compose.yml`

```
version: "3"
services:
  mongodb-4.4:
    image: mongo:4.4
    container_name: mongo-4.4
    restart: always
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: <place-your-password-here>
    volumes:
      - ./data:/data/db
    ports:
      - 127.0.0.1:27017:27017
```

### Clone code từ git:

```bash
git clone https://github.com/hanoiancs/smtpd-test.git
```

### Setup python venv:

```bash
cd smtpd-test
# Cài đặt gói python3-venv (nếu chưa có):
sudo apt install python3-venv
# Tạo mội trường python cho project:
python3 -m venv venv
# Active môi trường python:
source ./venv/bin/activate
```
### Cài đặt smtpd-test:


```bash
# Cài các gói cần thiết (Gặp lỗi `error: invalid command 'bdist_wheel'` bỏ qua không sao hết xD)
python -m pip install -r ./requirements.txt
```

### Cấu hình:

Tạo file `.env` với nội dung như sau: 

```env
FLASK_APP=flaskr
FLASK_ENV=development

SMTP_SERVER_HOSTNAME=127.0.0.1
SMTP_SERVER_PORT=8025
SMTP_SERVER_AUTH_REQUIRED=true
SMTP_SERVER_AUTH_REQUIRE_TLS=false

DB_MONGO_HOST=127.0.0.1
DB_MONGO_PORT=27017
DB_MONGO_USER=root
DB_MONGO_PASSWORD=<your-mongodb-password-here>
DB_MONGO_DATABASE=smtp_server
DB_MONGO_AUTHENTICATION_DATABASE=admin
```

###  Chạy SMTP server:

```bash 
python smtpd.py
```

### Chạy Web UI:
Mở 1 tab terminal mới, thực hiện lại bước `Setup python venv`.
WebUI sẽ mặc định chạy ở địa chỉ http://127.0.0.1:5000
```bash
flask run
```

### Tạo SMTP auth:

Command dưới đây sẽ tạo 1 cặp username/password để kết nối tới smtp server với username là `hello` và password ngẫu nhiên (được in ra sau khi script chạy xong):

```bash 
flask auth create hello 
```

Giả sử output là:
```
Inserted new client: 60865de8b5a0170b75928f26
User: hello
Password: wDmCv7h8DIpJh3EL
```
### Setup Laravel `.env` file:

```bash
MAIL_MAILER=smtp
MAIL_HOST=127.0.0.1
MAIL_PORT=8025
MAIL_USERNAME=hello
MAIL_PASSWORD=wDmCv7h8DIpJh3EL
MAIL_ENCRYPTION=null
MAIL_FROM_ADDRESS=sender@example.com
MAIL_FROM_NAME="${APP_NAME}"
```