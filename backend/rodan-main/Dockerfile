FROM ddmal/rodan-python3-celery:nightly

# Install OpenJPEG dependencies.
RUN \
  # flip this to trigger a new layer because the scripts are cached.
  set -x \
  && mkdir /vendor || echo "Already exists" \
  && apt update \
  && apt -q install -y \
  libopenjp2-7 \
  libopenjp2-7-dev \
  libopenjp2-tools \
  wget
  # git gcc build-essential

# We need make to compile Grok.
RUN apt-get install -y make

# Install Grok
WORKDIR /vendor
RUN wget --no-check-certificate https://cmake.org/files/v3.17/cmake-3.17.0-Linux-x86_64.tar.gz
RUN tar -xzf cmake-3.17.0-Linux-x86_64.tar.gz
# RUN /vendor/cmake-3.17.0-Linux-x86_64/bin/cmake --help

RUN git clone https://github.com/raviraina/grok.git
WORKDIR /vendor/grok

RUN git checkout 4932d86b19d9008a28ae898035cfa43340e636e6
RUN /vendor/cmake-3.17.0-Linux-x86_64/bin/cmake -DBUILD_THIRDPARTY=ON .
# TODO: ISSUE
RUN make -j3

# This script gets the gpu jobs into celery
# WORKDIR /
COPY ../../scripts/install_gpu_rodan_jobs /opt/install_gpu_rodan_jobs
COPY ../../scripts/start /run/
RUN set -e \
  && chmod +x /opt/install_gpu_rodan_jobs \
  && chown www-data /opt/install_gpu_rodan_jobs \
  # This script starts Rodan
  && chmod +x /run/start \
  && chown www-data /run/start

RUN /opt/install_gpu_rodan_jobs

# # Add entrypoint
COPY ../../scripts/entrypoint /opt/entrypoint
RUN chmod +x /opt/entrypoint \
  && chown www-data /opt/entrypoint

# # Substitute the build hash for our actual build hash
RUN sed -i "s/__build_hash__ = \"local\"/__build_hash__ = \"${BUILD_HASH}\"/" /code/Rodan/rodan/__init__.py

# # Change the concurrency
RUN sed -i "s/concurrency=10/concurrency=6/g" /run/start-celery
RUN sed -i "s/max-tasks-per-child=1/max-tasks-per-child=5/g" /run/start-celery

# ENTRYPOINT ["/opt/entrypoint"]
