FROM python:3.10-slim
WORKDIR /app
COPY .gitignore Apple_stock.py README.md requirements.txt /app/
COPY pages/Tips.py /app/pages/
RUN pip install -r requirements.txt
ENTRYPOINT [ "streamlit", "run", "Apple_stock.py"]