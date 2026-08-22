# Set default values for environment variables
# image version can be changed by "docker build -t shaharco1804/score_flask --build-arg image_version={{new_image_version}}"
# Pinned to 3.13 (mature, long support runway) rather than the floating
# "alpine" tag, which silently drifts to whatever Python minor is newest.
ARG image_name=python
ARG image_version=3.13-alpine

# Use an the image from variables
FROM ${image_name}:${image_version}

# Create app directory
WORKDIR /WorldOfGames

# Copy application files
COPY . /WorldOfGames/

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements

# Run as non-root
RUN adduser -D appuser && chown -R appuser:appuser /WorldOfGames
USER appuser

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=MainScores.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Command to run the application
ENTRYPOINT ["python"]
CMD ["MainScores.py"]