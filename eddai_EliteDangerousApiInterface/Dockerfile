# Use an official Miniconda3 image from ContinuumIO as the base image
FROM continuumio/miniconda3:latest

# Set the environment variable APP_HOME to /app
ENV APP_HOME=/app
# Configure PROJ_LIB environment variable for GDAL
ENV PROJ_LIB=/opt/conda/share/proj
# Create the /app directory
RUN mkdir $APP_HOME
# Set the working directory to /app
WORKDIR $APP_HOME

# Copy the environment.yml file to a temporary location in the container
COPY ./environment.yml /tmp/conda-tmp/
# Update the base conda environment using the environment.yml file
RUN umask 0002 && /opt/conda/bin/conda env update -n base -f /tmp/conda-tmp/environment.yml
# Verify PROJ data files are installed, install if needed
RUN if [ ! -d "/opt/conda/share/proj" ]; then \
        conda install -y -c conda-forge proj-data; \
    fi
# Create directory if it doesn't exist and set permissions
RUN mkdir -p /opt/conda/share/proj && chmod -R 755 /opt/conda/share/proj

# Copy the entire eddai_EliteDangerousApiInterface directory to /app
COPY . $APP_HOME

# Create a system group named 'app' and a system user named 'app' within that group
RUN addgroup --system app && adduser --system --group app
# Change the ownership of the /app directory to the 'app' user and group
RUN chown -R app:app $APP_HOME
# Ensure the entrypoint script is executable
RUN chmod +x $APP_HOME/entrypoint.sh

# Switch to the 'app' user for running subsequent commands
USER app

ENTRYPOINT [ "./entrypoint.sh" ]