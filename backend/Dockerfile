FROM python:3.11
RUN mkdir -p /app/
WORKDIR /app/
COPY .. /app/
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "start_app:app"]