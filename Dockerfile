FROM ubuntu:20.04

# Update the image
RUN apt update && apt upgrade -y && apt autoremove -y
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata
RUN #apt install -y python3-pip python3-pexpect unzip busybox-static fakeroot kpartx snmp uml-utilities util-linux vlan qemu-system-arm qemu-system-mips qemu-system-x86 qemu-utils lsb-core wget tar



# Install the required packages
RUN apt install sudo -y
RUN apt install git -y
RUN apt install -y python3-pip
RUN pip3 install --upgrade pip

# Copy the application files
COPY . /app

# Set the working directory
WORKDIR /app/src/modules/emulation/fat/

RUN ./setup.sh

ENV PYTHONPATH=/app
WORKDIR /app

# Install the required packages from requirements.txt
RUN pip3 install -r requirements.txt

# Expose the port
EXPOSE 5000
EXPOSE 80

# Run the application
CMD ["python3", "src/main.py"]
