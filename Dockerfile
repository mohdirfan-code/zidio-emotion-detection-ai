# Dockerfile
FROM python:3.10-slim

# Prevents Python from buffering stdout/stderr (logs show instantly)
ENV PYTHONUNBUFFERED=1

# Install OS dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 libxext6 libgl1-mesa-glx \
    curl git \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Upgrade pip and install wheel support for faster builds
RUN pip install --upgrade pip setuptools wheel

# Copy only requirements first (layer caching)
COPY requirements.txt .

# Install Python dependencies from minimal file
RUN pip install --no-cache-dir --prefer-binary -r requirements.txt

# Copy entire app codebase
COPY . .

# Expose backend + dashboard ports
EXPOSE 8000 8501

# Start both services
CMD ["bash", "start.sh"]
