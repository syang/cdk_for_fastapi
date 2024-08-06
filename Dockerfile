# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install pipenv
RUN pip install poetry

# Copy only the necessary files
COPY ../pyproject.toml ../poetry.lock ./
COPY . .

# Install dependencies using pipenv
RUN poetry install --no-root

# Set the PYTHONPATH to include the drg_service directory
ENV PYTHONPATH=/usr/src/app

# Make port 80 available to the world outside this container
EXPOSE 80

# Use pipenv to run the application using Uvicorn within the virtual environment
CMD ["poetry", "run", "uvicorn", "fastapi_app.main:app", "--host", "0.0.0.0", "--port", "80"]