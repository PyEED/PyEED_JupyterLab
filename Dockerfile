FROM jupyter/datascience-notebook

# Install packages
RUN pip install --upgrade pip
RUN pip install git+https://github.com/FAIRChemistry/chromatopy.git
