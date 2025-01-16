FROM python:3.12

# Install system dependencies and development tools
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    fontconfig \
    git \
    unzip \
    wget \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# LSD
WORKDIR /usr/local/lsd
ENV LSD_VERSION 1.1.5
ADD https://github.com/lsd-rs/lsd/releases/download/v${LSD_VERSION}/lsd-musl_${LSD_VERSION}_amd64.deb /usr/local/lsd/lsd.deb
RUN dpkg -i ./lsd.deb
RUN rm ./lsd.deb

# USER
ARG USERNAME=nonroot
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
  && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
  && chown -R $USER_UID:$USER_GID /home/$USERNAME

USER $USERNAME