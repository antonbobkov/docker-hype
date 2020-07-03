#!/bin/bash

sudo apt-get update -y

rebar3 local upgrade

cd ~/emacs_configs && git pull

cd ~/potato_game && git pull

