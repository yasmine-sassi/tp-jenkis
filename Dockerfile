FROM python:3.12-alpine

# Utilisateur non-root
RUN adduser -D appuser

WORKDIR /app

# Copier requirements EN PREMIER (cache Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code ENSUITE
COPY app.py .

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 5000

CMD ["python", "app.py"]