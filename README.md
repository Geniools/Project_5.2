# Project_5.2

An application which, provided a firmware file (binaries), can automatically emulate, and generate a report with
vulnerabilities found within the firmware.
*This application was developed part of Project 5.1 and Project 5.2 at NHL Stenden University of Applied Sciences*.

# Get started

## Prerequisites

- Ubuntu 20.04 (only system the application runs on)
- account with admin privileges (*sudo*)
- The following packages must be installed on the machine
    - git - ``sudo apt install git``
    - python 3.8 or higher - ``sudo apt install python3``
    - pip - ``sudo apt install python3-pip``
    - docker - ``sudo apt install docker.io``

## Installing

1. Clone the repository

```git clone –recurse-submodules https://github.com/Geniools/Project_5.2.git```

2. Switch the current working directory inside the project

``cd Project_5.2``

3. Install FAT (firmware analysis toolkit)

``sudo ./src/modules/emulation/fat/setup.sh``

4. Run the app

``python3 ./src/main.py``

An **ip address** together with a **port** will be displayed inside the terminal. Use them to access the application
inside
your favourite browser. (e.g. 127.0.0.1:5000)

## Usage

First of all a firmware file must be uploaded (zip files containing one are also accepted).
Pressing the *run* button after uploading the file will attempt to start the emulation process.
*NOTE: This is a very time-consuming process!*. The status will update based on the stage the emulation is in.

Once the emulation is completed the firmware can be scanned with all the modules available. This process is
started by pressing the *scan* button.

At the end of the scanning, a report in PDF format can be downloaded, containing the results fetched from
the previous processes.

# Known issues

- The application does not work as expected in a docker container. Running Dockerfile will make a docker container
  which will run successfully, though, during the emulation process, no ip address is generated, making scanning
  impossible.
- The report in the downloaded PDF file is meaningless. The application does not have a structured way of
  saving the results to the PDF file in a meaningful way.
- Routersploit is not integrated in the application as a module.
- Metasploit might not work as expected.


