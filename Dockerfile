FROM mcr.microsoft.com/playwright/python:latest

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install browsers (Playwright base image already has them, but keep to ensure)
RUN playwright install --with-deps

CMD ["pytest", "-q"]