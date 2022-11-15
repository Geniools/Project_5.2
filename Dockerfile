FROM ubuntu:20.04
# Update the image
RUN apt update && apt upgrade -y
# Install the required packages
RUN apt install -y python3 python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install flask

# Copy the application files
COPY . /app
# Set the working directory
WORKDIR /app
# Expose the port
EXPOSE 5000
# Run the application
CMD ["python3", "main/main.py"]
