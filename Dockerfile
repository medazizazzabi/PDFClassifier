FROM python:3.8.10

WORKDIR /Neoplis

# Install dependencies including Tesseract and French language package
RUN apt-get update && apt-get install -y \
    poppler-utils \
    libgl1-mesa-dev \
    libgl1-mesa-glx \
    libglew-dev \
    libosmesa6-dev \
    software-properties-common \
    net-tools \
    wget \
    tesseract-ocr \
    tesseract-ocr-fra \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -f UTF-8 en_US.UTF-8

ENV LANG en_US.UTF-8 
ENV LANGUAGE en_US:en 
ENV LC_ALL en_US.UTF-8

COPY requirements.txt requirements.txt
COPY ./webapp ./webapp

RUN pip install -r requirements.txt

CMD ["sh", "-c", "cd webapp && python main.py"]