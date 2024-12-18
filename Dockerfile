FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
ENTRYPOINT [ "streamlit", "run", "Apple_stock.py"]