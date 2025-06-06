# Copied from https://github.com/UCSD-E4E/fishsense-lite/blob/c545a0df7fe0be957b839bd41086b0aa64976d67/runtime/Dockerfile
FROM ghcr.io/ucsd-e4e/fishsense:cuda

SHELL ["/bin/bash", "-c"]

USER root
ARG GID=1001
ARG UID=1001
ARG CUDA_GROUP_ID=65533
RUN groupmod -g ${GID} ubuntu && usermod -u ${UID} -g ${GID} ubuntu && groupadd -g ${CUDA_GROUP_ID} cuda
RUN usermod -aG cuda ubuntu

RUN mkdir -p ~/.ssh && ssh-keyscan -H github.com >> ~/.ssh/known_hosts

RUN git clone --depth=1 https://github.com/UCSD-E4E/fishsense-lite.git /tmp/git_cache/fishsense-lite/; \
    cd /tmp/git_cache/fishsense-lite/ && git pull && cp -r ./ /tmp/fishsense-lite/

WORKDIR /tmp/fishsense-lite
RUN . ${HOME}/.cargo/env && pip install .

WORKDIR /app

# --- Reproduce the environment ---
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_IN_PROJECT=1
ENV POETRY_VIRTUALENVS_CREATE=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# You can comment the following two lines if you prefer to manually install
#   the dependencies from inside the container.
COPY pyproject.toml poetry.lock /app/

# Install the dependencies and clear the cache afterwards.
#   This may save some MBs.
RUN poetry install --no-root --without dev && rm -rf $POETRY_CACHE_DIR

COPY README.md /app/README.md
COPY fishsense_data_processing_worker /app/fishsense_data_processing_worker
RUN poetry install --only main

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"
ENV E4EFS_DOCKER=true

RUN mkdir -p /e4efs/config /e4efs/logs /e4efs/data /e4efs/cache && chown -R ubuntu:ubuntu /e4efs
COPY sql sql
USER ubuntu
ENTRYPOINT ["fsl_worker"]

