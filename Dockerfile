# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /code

# Copy the requirements file and install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the project code
COPY . /code/
RUN mkdir db

RUN chown -R $USER:$USER .

# Set the entrypoint command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]