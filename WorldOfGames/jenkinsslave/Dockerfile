# Set default values for environment variables
# image version can be changed by "docker build --build-arg image_version={{new_image_version}}"
ARG image_name=ubuntu
ARG image_version=22.04
ARG packages='python3 python3-pip wget unzip telnet iputils-ping git'
# Pinned Docker CLI / Compose versions: the bundled CLI (20.10.13, API 1.41) is
# too old for current Docker daemons (min supported API 1.44+). These static
# binaries replace it so `docker`/`docker-compose` calls against the mounted
# host socket keep working regardless of what the base image ships.
ARG docker_cli_version=27.3.1
ARG docker_compose_version=2.29.7
ARG gitleaks_version=8.21.2

# Use an the image from variables
FROM ${image_name}:${image_version}
ARG packages
ARG docker_cli_version
ARG docker_compose_version
ARG gitleaks_version
RUN apt-get update -y
RUN apt -f install -y
RUN apt-get install -y ${packages} ca-certificates curl
RUN apt-get update -y
COPY requirements requirements
RUN pip3 install -r requirements

RUN rm -f /usr/local/bin/docker /usr/local/bin/docker-compose && \
    curl -fsSL "https://download.docker.com/linux/static/stable/x86_64/docker-${docker_cli_version}.tgz" -o /tmp/docker-cli.tgz && \
    tar -xzf /tmp/docker-cli.tgz -C /tmp && \
    mv /tmp/docker/docker /usr/local/bin/docker && \
    rm -rf /tmp/docker /tmp/docker-cli.tgz && \
    curl -fsSL "https://github.com/docker/compose/releases/download/v${docker_compose_version}/docker-compose-linux-x86_64" -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker /usr/local/bin/docker-compose && \
    docker --version && docker-compose --version

RUN curl -fsSL "https://github.com/gitleaks/gitleaks/releases/download/v${gitleaks_version}/gitleaks_${gitleaks_version}_linux_x64.tar.gz" -o /tmp/gitleaks.tar.gz && \
    tar -xzf /tmp/gitleaks.tar.gz -C /usr/local/bin gitleaks && \
    rm -f /tmp/gitleaks.tar.gz && \
    chmod +x /usr/local/bin/gitleaks && \
    gitleaks version