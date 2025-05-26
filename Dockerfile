# Sử dụng Python image chính thức từ Docker Hub
FROM python:3.11-alpine

# Cài đặt curl và gnupg (cần thiết để tải và cài đặt ODBC driver)
RUN apk add --no-cache curl gnupg

# Cài đặt ODBC Driver và MSSQL Tools
RUN curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/msodbcsql17_17.10.6.1-1_amd64.apk && \
    curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/mssql-tools_17.10.1.1-1_amd64.apk && \
    apk add --allow-untrusted msodbcsql17_17.10.6.1-1_amd64.apk && \
    apk add --allow-untrusted mssql-tools_17.10.1.1-1_amd64.apk && \
    rm msodbcsql17_17.10.6.1-1_amd64.apk mssql-tools_17.10.1.1-1_amd64.apk

# Cài đặt build dependencies cho việc biên dịch pyodbc
RUN apk add --no-cache build-base python3-dev unixodbc-dev

# Copy requirements.txt vào container và cài đặt các dependencies Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Loại bỏ build dependencies để giảm kích thước image
RUN apk del build-base

# Copy toàn bộ mã nguồn vào container
COPY . /app

# Chuyển đến thư mục ứng dụng
WORKDIR /app

# Chạy ứng dụng Flask bằng Gunicorn
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:10000"]
