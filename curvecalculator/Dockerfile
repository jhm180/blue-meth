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

#ENV DB_HOST db-proxy
#ENV DB_NAME dvt-db-staging
#ENV DB_USER pgadminuser
#ENV DB_PW BBIgbGkD5IIDHfGx
#ENV DB_UPLOAD_TOGGLE False
#ENV VM_NAME JHMLaptop
#ENV SUCCESS_EMAIL_TOGGLE EmailOn 
#ENV FAIL_EMAIL_TOGGLE EmailOn 
#ENV GOOGLE_APPLICATION_CREDENTIALS = "/Users/joemellet/src/devutils/wpdvt-228113-ddc6feae2593.json"

# Make port 80 available to the world outside this container
EXPOSE 8080


# Run app.py when the container launches
CMD ["python", "curvecalc.py"]