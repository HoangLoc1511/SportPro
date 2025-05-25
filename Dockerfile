FROM python:3.11-alpine

RUN apk add --no-cache curl gnupg

# Cài ODBC Driver
RUN curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/msodbcsql17_17.10.6.1-1_amd64.apk && \
    curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/mssql-tools_17.10.1.1-1_amd64.apk && \
    apk add --allow-untrusted msodbcsql17_17.10.6.1-1_amd64.apk && \
    apk add --allow-untrusted mssql-tools_17.10.1.1-1_amd64.apk && \
    rm msodbcsql17_17.10.6.1-1_amd64.apk mssql-tools_17.10.1.1-1_amd64.apk

RUN apk add --no-cache build-base python3-dev unixodbc-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apk del build-base

COPY . /app
WORKDIR /app

CMD ["gunicorn", "app:app", "-b", "0.0.0.0:10000"]
