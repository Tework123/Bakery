FROM python:3.11
WORKDIR /app
COPY .. /app
RUN pip install -r requirements.txt
CMD ["gunicorn", "-b", ":5000", "start_app:app"]