# Set default values for environment variables
# image version can be changed by "docker build --build-arg image_version={{new_image_version}}"
ARG image_name=python
ARG image_version=3.10-alpine

# Use an the image from variables
FROM ${image_name}:${image_version}

RUN mkdir "WorldOfGames"
WORKDIR devops_expert/WorldOfGames
COPY requirements requirements
RUN pip install --upgrade pip
RUN pip install -r requirements
COPY . .
CMD ["python", "MainScores.py"]