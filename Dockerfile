FROM python:3.11-alpine

RUN apk add --no-cache curl gnupg

# Cài driver ODBC và MSSQL Tools
RUN curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/msodbcsql17_17.10.6.1-1_amd64.apk && \
    curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/mssql-tools_17.10.1.1-1_amd64.apk && \
    apk add --allow-untrusted msodbcsql17_17.10.6.1-1_amd64.apk && \
    apk add --allow-untrusted mssql-tools_17.10.1.1-1_amd64.apk && \
    rm msodbcsql17_17.10.6.1-1_amd64.apk mssql-tools_17.10.1.1-1_amd64.apk

# Cài công cụ build và thư viện cần thiết để build pyodbc
RUN apk add --no-cache --virtual .build-deps \
    build-base python3-dev unixodbc-dev

# Copy requirements.txt vào container
COPY requirements.txt .

# Cài python packages
RUN pip install --no-cache-dir -r requirements.txt

# Xóa bộ công cụ build sau khi cài xong để giảm dung lượng image
RUN apk del .build-deps

# Copy toàn bộ source code vào /app
COPY . /app

WORKDIR /app

# Lệnh chạy Gunicorn để khởi động app Flask
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:10000"]
