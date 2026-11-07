FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
COPY README.md ./README.md

EXPOSE 8080
CMD ["sh", "-c", "streamlit run app/main.py --server.address 0.0.0.0 --server.port ${PORT} --server.enableCORS=false --server.enableXsrfProtection=false"]
