# Set default values for environment variables
# image version can be changed by "docker build -t shaharco1804/score_flask --build-arg image_version={{new_image_version}}"
ARG image_name=python
ARG image_version=3.10-alpine

# Use an the image from variables
FROM ${image_name}:${image_version}

RUN mkdir "WorldOfGames"
VOLUME /WorldOfGames
WORKDIR /WorldOfGames
COPY requirements /requirements
RUN pip install --upgrade pip
RUN pip install -r /requirements
CMD ["python", "MainScores.py"]