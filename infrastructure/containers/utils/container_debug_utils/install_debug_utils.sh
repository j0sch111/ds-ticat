#!/bin/bash

# Update the package list
yum update -y

# Install debugging utilities
yum install -y vim nano htop strace gdb net-tools

# Clean up
yum clean all

echo "Debugging utilities installed successfully."
