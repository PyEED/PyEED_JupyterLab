FROM jupyter/datascience-notebook

# Install packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt