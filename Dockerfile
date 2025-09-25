#Use official python image as base
FROM python:3.13

#Set Environment Variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#Set working directory inside the container
WORKDIR /app

#Copy requirements.txt and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

#Copy the entire project into the container
COPY . /app/

# Expose the port Django runs on
EXPOSE 8000

# Run Django development server
CMD ["gunicorn", "jobportal.wsgi:application", "--bind", "0.0.0.0:8000"]
