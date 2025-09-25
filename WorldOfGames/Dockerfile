# Set default values for environment variables
# image version can be changed by "docker build -t shaharco1804/score_flask --build-arg image_version={{new_image_version}}"
ARG image_name=python
ARG image_version=alpine

# Use an the image from variables
FROM ${image_name}:${image_version}

# Create app directory
WORKDIR /WorldOfGames

# Copy application files
COPY . /WorldOfGames/

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=MainScores.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Command to run the application
ENTRYPOINT ["python"]
CMD ["MainScores.py"]