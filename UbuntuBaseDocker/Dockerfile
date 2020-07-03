
FROM ubuntu:18.04

MAINTAINER texfan@gmail.com

RUN bash -c "echo -ne 'y\nY\n' | unminimize" # optional i guess

RUN apt-get update -y

RUN apt-get install -y emacs git openssh-server openssh-client

RUN apt-get install -y sudo

RUN apt-get install -y erlang

RUN apt-get install -y net-tools

RUN apt-get install -y curl

RUN mkdir /run/sshd  # needed to run sshd directly
RUN echo 'PasswordAuthentication no' >> /etc/ssh/sshd_config
RUN echo 'PermitRootLogin no' >> /etc/ssh/sshd_config
RUN echo 'PubkeyAuthentication yes' >> /etc/ssh/sshd_config
RUN echo 'AuthorizedKeysFile .ssh/authorized_keys' >> /etc/ssh/sshd_config
RUN echo 'ClientAliveInterval 60' >> /etc/ssh/sshd_config

# RUN sed -ri 's/UsePAM yes/UsePAM no/g' /etc/ssh/sshd_config # seems to need PAM for public key connection

RUN useradd -ms /bin/bash anton

RUN echo 'anton ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers


USER anton

RUN mkdir ~/.ssh/

COPY config *_key* /home/anton/.ssh/
COPY update.sh /home/anton/
COPY *_add /home/anton/
COPY dot_emacs /home/anton/.emacs

RUN sudo chown anton ~/*
RUN sudo chown anton -R ~/.ssh  # copies owned by root

RUN cd ~ && cat bashrc_add >> .bashrc

RUN chmod 600 ~/.ssh/config  # git complains otherwise
RUN cat ~/.ssh/docker_anton_key.pub >> ~/.ssh/authorized_keys

# RUN git clone https://github.com/antonbobkov/potato_game.git ~/potato_game/


RUN git config --global user.email "texfan@gmail.com"
RUN git config --global user.name "anton_docker"

RUN wget -P ~/ https://s3.amazonaws.com/rebar3/rebar3 && chmod +x ~/rebar3
RUN ~/rebar3 local install

# ENV PATH="/home/anton/.cache/rebar3/bin:${PATH}"  # doesn't work?
RUN echo "export PATH=/home/anton/.cache/rebar3/bin:$PATH" >> ~/.bashrc


RUN git clone git@github.com:antonbobkov/emacs_configs.git ~/emacs_configs/
RUN emacs --script ~/emacs_configs/docker_emacs_package_install.el

RUN git clone git@github.com:antonbobkov/potato_game.git ~/potato_game/
RUN cd ~/potato_game/ && (~/rebar3 eunit || true) && (~/rebar3 dialyzer || true)

RUN rm ~/rebar3

USER root

ENTRYPOINT ["/usr/sbin/sshd", "-D"]
