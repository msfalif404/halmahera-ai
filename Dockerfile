# Builder stage
FROM python:3.12-slim as builder

WORKDIR /app

COPY requirements.txt .

# Install dependencies to user directory
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.12-slim as runtime

WORKDIR /app

# Copy only necessary artifacts from builder stage
COPY --from=builder /root/.local /root/.local

# Add .local bin to PATH
ENV PATH=/root/.local/bin:$PATH \
    PYTHONPATH=/app

# Copy application code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]