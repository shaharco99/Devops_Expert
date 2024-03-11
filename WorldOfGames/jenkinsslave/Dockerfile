# Set default values for environment variables
# image version can be changed by "docker build --build-arg image_version={{new_image_version}}"
ARG image_name=linuxserver
ARG image_version=docker-compose
ARG packages='python3 pip wget unzip telnet iputils-ping'

# Use an the image from variables
FROM ${image_name}:${image_version}
RUN apt-get update -y
RUN apt -f install -y
RUN apt-get install -y ${packages}
RUN apt-get update -y
COPY requirements requirements
RUN telnet
RUN pip install -r requirements