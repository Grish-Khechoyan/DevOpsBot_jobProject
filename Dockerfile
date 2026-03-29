FROM python:3.12-alpine AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt
FROM python:3.12-alpine AS runtime
WORKDIR /app
COPY --from=builder /install /usr/local
COPY . .
ENV PORT=8000
EXPOSE 8000
CMD ["python", "app.py"]
