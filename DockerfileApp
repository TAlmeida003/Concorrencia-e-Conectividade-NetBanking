# Used to build the image for the application
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app_1
COPY . .

RUN pip install Flask
RUN pip install requests

EXPOSE 3050

CMD ["python", "src/app"]