FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

WORKDIR /usr/app

RUN mkdir -p input output joined

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Install additional dependencies
RUN apt-get -y update --fix-missing && \
    apt-get -y upgrade && \
    apt-get install -y ffmpeg

# Copy the application code
COPY . .

EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py

# Run the Flask application
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
