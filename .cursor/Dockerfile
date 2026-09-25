# Cloud Agent development base image for the Enterprise Agent Platform.
# Provides the stable system toolchain the project pins: Python 3.14,
# PostgreSQL 16, and Terraform. Project Python dependencies are installed
# after checkout by .cursor/install.sh (they track requirements.txt).
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

# Base utilities needed to add repositories and build Python extensions.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        wget \
        gnupg \
        git \
        sudo \
        lsb-release \
        software-properties-common \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# Python 3.14 (matches the project's Dockerfile and CI) via deadsnakes.
RUN add-apt-repository -y ppa:deadsnakes/ppa \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        python3.14 \
        python3.14-venv \
        python3.14-dev \
    && rm -rf /var/lib/apt/lists/*

# PostgreSQL 16 (matches docker-compose and CI). The package's post-install
# step creates the default "16 main" cluster; .cursor/start.sh starts it.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-16 \
        postgresql-client-16 \
    && rm -rf /var/lib/apt/lists/*

# Terraform (matches the infra CI checks).
RUN wget -qO - https://apt.releases.hashicorp.com/gpg \
        | gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" \
        > /etc/apt/sources.list.d/hashicorp.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends terraform \
    && rm -rf /var/lib/apt/lists/*

# The ubuntu:24.04 image ships an "ubuntu" user (uid 1000); grant it
# passwordless sudo so start.sh can manage the PostgreSQL cluster.
RUN echo "ubuntu ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/ubuntu \
    && chmod 0440 /etc/sudoers.d/ubuntu

USER ubuntu
