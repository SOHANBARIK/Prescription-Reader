# 1. Use an official lightweight Python image
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Install system dependencies required for OpenCV and EasyOCR
# (libgl1 and libglib2.0 are needed for cv2 to work on Linux)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy the requirements file first (for better caching)
COPY requirements.txt .

# 5. Install Python dependencies
# We use --no-cache-dir to keep the image small
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of the application code
COPY . .

# 7. Expose the port (Render usually uses 10000, but we use an ENV variable)
ENV PORT=5000

# 8. Command to run the application
# We use "0.0.0.0" to allow external connections
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]