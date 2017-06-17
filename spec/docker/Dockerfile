FROM registry.ahaflow.com:5000/solo/runtime-base

MAINTAINER Mush Mo <mush@pandorica.io>

# install
RUN apt-get update && apt-get install -y \
    git \
    python-dev \
    vim \
    python-pip \
    libssl-dev \
    swig \
    && rm -rf /var/lib/apt/lists/*
RUN apt-get install libffi-dev

ADD ./requirements.txt /home/runtime/requirement.txt

RUN pip install -r /home/runtime/requirement.txt

ADD ./code /home/runtime/sololive
ADD ./entrypoint /home/runtime/sololive/app/liveapi/entrypoint

RUN chown -R runtime:runtime /home/runtime

WORKDIR /home/runtime/sololive
USER runtime

EXPOSE 20000

ENTRYPOINT ["/home/runtime/sololive/app/liveapi/entrypoint"]

