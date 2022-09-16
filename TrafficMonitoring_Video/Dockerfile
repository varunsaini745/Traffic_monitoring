
FROM ubuntu:20.04
FROM python:3.9.12

WORKDIR /vehicle_code

COPY . /vehicle_code
RUN apt-get update && \
    apt-get install -yq --no-install-recommends \
    libkrb5-dev \
    libsm6 \
    libxext6 \
    ffmpeg \
    libfontconfig1 \
    libxrender1 \
    libgl1-mesa-glx && \
    rm -rf /var/lib/apt/lists/*
ENV PYTHONPATH "${PYTHONPATH}:/app/"

RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install --no-cache-dir pip install python-multipart
EXPOSE 8082

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8082"]

