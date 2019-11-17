FROM continuumio/miniconda3

# clean up impage
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Do not run as root
RUN groupadd -r myuser && useradd -r -g myuser myuser

WORKDIR /app

# Install requirements
COPY environment.yml /app/environment.yml
RUN conda config --add channels conda-forge \
    && conda env create -n ChessEngine -f environment.yml \
    && rm -rf /opt/conda/pkgs/* 

# Expose port 5000
EXPOSE 5000 5000

# activate the classifierTools environment
ENV PATH /opt/conda/envs/ChessEngine/bin:$PATH

# copy over python files and dataset
COPY . .

CMD ['bash', 'conda activate ChessEngine']

CMD [ "pytest", "test_server.py" ]

CMD [ "python3", "server.py" ]

