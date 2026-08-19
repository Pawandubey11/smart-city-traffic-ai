FROM python:3.10-slim

# Install OpenCV system dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python data/create_sample_traffic_video.py

ENV PYTHONUNBUFFERED=1

CMD ["python", "edge/main.py", "--source", "data/sample_traffic.mp4"]
