#!/bin/bash

# Uninstall debugging utilities
yum remove -y vim nano htop strace gdb net-tools

# Clean up
yum clean all

echo "Debugging utilities uninstalled successfully."
