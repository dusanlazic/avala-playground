FROM python:3.12-alpine
WORKDIR /app
COPY service.py /app/service.py
RUN pip install fastapi uvicorn
CMD ["uvicorn", "service:app", "--host", "0.0.0.0", "--port", "80"]