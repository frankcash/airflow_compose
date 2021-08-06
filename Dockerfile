FROM python:3.6-slim

# Never prompts the user for choices on installation/configuration of packages
ENV DEBIAN_FRONTEND=noninteractive \
    TERM=linux

# Airflow
ARG AIRFLOW_VERSION=2.1.0
ARG AIRFLOW_HOME=/usr/local/airflow
ENV AIRFLOW_GPL_UNIDECODE=yes \
    AIRFLOW_HOME=/usr/local/airflow

# Define en_US.
ENV LANGUAGE=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    LC_CTYPE=en_US.UTF-8 \
    LC_MESSAGES=en_US.UTF-8 \
    locale-gen=en_US.UTF-8 \
    locale-gen=es_CO.UTF-8

COPY requirements.txt ${AIRFLOW_HOME}/requirements.txt

RUN set -ex \
    && buildDeps=' \
        python3-dev \
        libkrb5-dev \
        libsasl2-dev \
        libssl-dev \
        libffi-dev \
        libblas-dev \
        liblapack-dev \
        libpq-dev \
        git \
    ' \
    && apt-get update -yqq \
    && apt-get upgrade -yqq \
    && apt-get install -yqq --no-install-recommends \
        $buildDeps \
        build-essential \
        python3-pip \
        python3-requests \
        default-libmysqlclient-dev \
        apt-utils \
        curl \
        rsync \
        netcat \
        locales \
    && sed -i 's/^# en_US.UTF-8 UTF-8$/en_US.UTF-8 UTF-8/g' /etc/locale.gen \
    && locale-gen \
    && update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 \
    && useradd -ms /bin/bash -d ${AIRFLOW_HOME} airflow \
    && pip install -U pip setuptools wheel \
    && pip install -r ${AIRFLOW_HOME}/requirements.txt \
    && apt-get purge --auto-remove -yqq $buildDeps \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/* \
        /usr/share/man \
        /usr/share/doc \
        /usr/share/doc-base

COPY script/entrypoint.sh /entrypoint.sh
COPY config/airflow.cfg ${AIRFLOW_HOME}/airflow.cfg
COPY airflow_home/ ${AIRFLOW_HOME}


RUN mkdir ${AIRFLOW_HOME}/temp
RUN chown -R airflow: ${AIRFLOW_HOME}

EXPOSE 8080 5555

USER airflow
WORKDIR ${AIRFLOW_HOME}
ENTRYPOINT ["/entrypoint.sh"]
CMD ["webserver"] # set default arg for entrypoint
