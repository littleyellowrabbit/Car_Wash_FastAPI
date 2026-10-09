# 1. 使用官方輕量化 Python 鏡像（節省空間與提升安全性）
FROM python:3.14-slim

# 2. 設定容器內的工作目錄（後續指令都會在此目錄執行）
WORKDIR /app

# 3. 複製套件清單並安裝
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 複製您的程式碼與設定檔資料夾
COPY main.py .
COPY library/ ./library/

# 5. 在容器內建立一個專門放 SQL 資料庫的資料夾
RUN mkdir -p /app/data

# 6. 宣告容器開放 8000 連接埠
EXPOSE 8000

# 7. 啟動指令（透過 Uvicorn 啟動，注意 host 必須是 0.0.0.0）
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]