#!/bin/bash

# Install wget (if not already installed)
sudo apt-get update
sudo apt-get install wget -y

# Download the Google Chrome package
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

# Install the package
sudo dpkg -i google-chrome-stable_current_amd64.deb

# Resolve dependencies
sudo apt-get install -f -y

# Remove the downloaded package (optional)
rm google-chrome-stable_current_amd64.deb

