FROM jupyter/datascience-notebook

# Copy the scripts into the container and set them as executable in one step
COPY --chmod=+x startup-script.sh /usr/local/bin/startup-script.sh
COPY --chmod=+x update_packages.py /usr/local/bin/update_packages.py

RUN pip install --upgrade pip \
    && pip install toml

# Use the custom startup script as the entrypoint
ENTRYPOINT ["/usr/local/bin/startup-script.sh"]