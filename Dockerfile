# SuitUp — offline, locally-runnable American Mah Jongg teaching app.
# Single self-contained Flask container (birdwatcher pattern), served on 8092.
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Dependencies first for better layer caching.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application source.
COPY . .

# SuitUp is served at http://localhost:8092 (product contract).
EXPOSE 8092

# Run the Flask app as a module so suitup/ stays a proper importable package.
CMD ["python3", "-m", "suitup.web.app"]
