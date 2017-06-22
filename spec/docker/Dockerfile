FROM ubuntu:16.10

MAINTAINER glrh11 <glrh11.com>

RUN apt-get clean
RUN apt-get update
RUN apt-get install -y \
    git \
    python-dev \
    vim \
    python-pip \
    libssl-dev \
    swig \
    libffi-dev \
    sudo
#    && rm -rf /var/lib/apt/lists/*

RUN useradd -ms /bin/bash runtime && echo "runtime:wocao" | chpasswd && adduser runtime sudo

ADD ./requirements.txt /home/runtime/requirement.txt

RUN pip install -i https://pypi.douban.com/simple/ -r /home/runtime/requirement.txt

ADD ./entrypoint /home/runtime/entrypoint

# code inner dir: /home/runtime/read_in_life_api

RUN chown -R runtime:runtime /home/runtime

WORKDIR /home/runtime
USER runtime

EXPOSE 8000

ENTRYPOINT ["/home/runtime/entrypoint"]