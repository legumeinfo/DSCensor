FROM python:3.11.1-slim-buster

# install gcc and other build requirements
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

ADD . /app

WORKDIR /app

# checkout set tag later after fetch
RUN git remote add github-upstream https://github.com/legumeinfo/DSCensor.git
RUN git fetch github-upstream
RUN git checkout github-upstream/openapi

# install the package dependencies
RUN pip3 install --no-cache-dir -r requirements.txt
RUN python ./LIS-autocontent/setup.py install

# populate objects for graphDB
RUN lis-autocontent populate-dscensor --from_github ./datastore-metadata/ --taxa_list ./jekyll-legumeinfo/_data/taxon_list.yml --nodes_out ./autocontent

# install (and implicitly build) the package

ENTRYPOINT ["python", "-m", "aiohttp.web", "dscensor.app:create_app"]
