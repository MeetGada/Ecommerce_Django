FROM python:3.12 AS builder

RUN mkdir /app

#setting the app as working directory
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install --no-cache-dir psycopg2==2.9.11


# Production Stage
FROM python:3.12-slim

RUN useradd -m -r appuser && \
   mkdir /app && \
   chown -R appuser /app

# Copy the Python dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

WORKDIR /app

COPY --chown=appuser:appuser . .

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

# Switch to non-root user
USER appuser

# Expose the application port
EXPOSE 8000

# Make entry file executable
RUN chmod +x  /app/startserver.sh

# Start the application using Gunicorn
CMD ["/app/startserver.sh"]

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# https://www.youtube.com/watch?v=1v3lqIITRJA