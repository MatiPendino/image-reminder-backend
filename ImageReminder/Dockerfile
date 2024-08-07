# Use the official Python base image
FROM python:3.12

ENV PYTHONBUFFERED=1

# Set the working directory
WORKDIR /imagereminder

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

# Run the runserver command
CMD python manage.py runserver 0.0.0.0:8000