FROM ubuntu:20.04
# Update the image
RUN apt update && apt upgrade -y apt autoremove -y

# Install the required packages

RUN apt install -y python3-pip
RUN pip3 install --upgrade pip

# Copy the application files
COPY . /app
# Set the working directory
WORKDIR /app

# Install the required packages from requirements.txt
RUN pip3 install -r requirements.txt

# Expose the port
EXPOSE 5000
# Run the application
CMD ["python3", "src/main.py"]
