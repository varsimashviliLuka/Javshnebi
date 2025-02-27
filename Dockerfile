# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Give execute permissions to the startup script
RUN chmod +x flask_app.sh

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the port Flask runs on
EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

