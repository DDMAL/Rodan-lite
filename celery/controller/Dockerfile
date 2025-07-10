# FROM ddmal/rodan-python3-celery:nightly
FROM python:3.7.16-slim-buster

# We need make to compile Grok.
# RUN apt-get install -y make
# # Install OpenJPEG dependencies.
# RUN \
#   # flip this to trigger a new layer because the scripts are cached.
#   set -x \
#   && mkdir /vendor || echo "Already exists" \
#   && apt update \
#   && apt -q install -y \
#   libopenjp2-7 \
#   libopenjp2-7-dev \
#   libopenjp2-tools



# This script gets the gpu jobs into celery
# COPY ../../scripts/install_gpu_rodan_jobs /opt/install_gpu_rodan_jobs
# RUN set -e \
#   && chmod +x /opt/install_gpu_rodan_jobs \
#   && chown www-data /opt/install_gpu_rodan_jobs \
#   # This script starts Rodan
#   && chmod +x /run/start \
#   && chown www-data /run/start
# RUN /opt/install_gpu_rodan_jobs

COPY ../../scripts/start /run/


# Substitute the build hash for our actual build hash
# RUN sed -i "s/__build_hash__ = \"local\"/__build_hash__ = \"${BUILD_HASH}\"/" /code/Rodan/rodan/__init__.py

# Change the concurrency
# RUN sed -i "s/concurrency=10/concurrency=6/g" /run/start-celery
# RUN sed -i "s/max-tasks-per-child=1/max-tasks-per-child=5/g" /run/start-celery

