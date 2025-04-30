FROM python:3.11-slim
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=UTF-8
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libomp-dev \
    libssl-dev \
    libffi-dev \
    apt-utils \
    net-tools \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*
COPY requirements.txt ./
RUN pip3 install -r ./requirements.txt
COPY ltr.py ./
COPY entrypoint.sh ./
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]