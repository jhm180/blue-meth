# Use an official Python runtime as a parent image
FROM python:3.7-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY src/requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt
# RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY src /app

# Make port 80 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV NAME World
# ENV GOOGLE_APPLICATION_CREDENTIALS = "/Users/joemellet/downloads/wpdvt-228113-ddc6feae2593.json"

# Run app.py when the container launches
CMD ["python", "sendemail.py"]