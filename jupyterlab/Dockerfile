FROM jupyter/datascience-notebook

# Copy the scripts into the container and set them as executable in one step
COPY --chmod=+x startup-script.sh /usr/local/bin/startup-script.sh
COPY --chmod=+x update_packages.py /usr/local/bin/update_packages.py

USER root

RUN apt-get update \
    && apt-get -y install libpq-dev gcc python3-dev\
    && pip install psycopg2

RUN pip install --upgrade pip \
    && pip install --upgrade h5py \
    && pip install --upgrade wheel \
    && pip install --upgrade typing-extensions \
    && pip install toml

# Use the custom startup script as the entrypoint
ENTRYPOINT ["/usr/local/bin/startup-script.sh"]