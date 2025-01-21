# Use the official Python image from the Docker Hub
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Install the dependencies listed in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Firefox, Geckodriver, and necessary dependencies
RUN apt-get update && apt-get install -y \
    firefox-esr \
    wget \
    unzip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Geckodriver
# RUN wget -q https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz \
#     && tar -xvzf geckodriver-v0.33.0-linux64.tar.gz \
#     && mv geckodriver /usr/bin/ \
#     && rm geckodriver-v0.33.0-linux64.tar.gz


# Install Firefox
RUN apt-get update && apt-get install -y \
    firefox-esr \
    wget \
    unzip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Geckodriver (ARM version)
RUN wget -q https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-linux-aarch64.tar.gz \
    && tar -xvzf geckodriver-v0.35.0-linux-aarch64.tar.gz \
    && mv geckodriver /usr/bin/


# Set environment variable to use Firefox with Selenium
ENV PATH="/usr/bin:$PATH"

# Copy the entire application code into the container
COPY . .

# Command to run the Flask application
CMD ["python", "main.py"]
