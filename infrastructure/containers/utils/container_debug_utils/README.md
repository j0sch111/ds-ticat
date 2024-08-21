# Debug Utilities for AL2023 Docker Container
## Overview

This repository contains scripts to install and uninstall common debugging utilities on an Amazon Linux 2023 (AL2023) Docker container. These tools are essential for debugging, monitoring, and system administration tasks within the container.
Included Tools

    Text Editors: Vim,  Nano

    Htop
        Description: Htop is an interactive process viewer for Unix systems.
        Usage:
            Run: htop
            Navigate with arrow keys, kill process with F9

    Strace
        Description: Strace is a diagnostic, debugging, and instructional userspace utility for Linux.
        Usage:
            Trace a command: strace command
            Save output to a file: strace -o output.txt command

    GDB
        Description: GDB is the GNU Project debugger, allowing you to see what is going on inside a program while it executes.
        Usage:
            Start debugging: gdb program
            Run the program: run
            Set a breakpoint: break main
            Continue execution: continue

    Net-tools
        Description: Net-tools is a collection of programs for controlling the network subsystem of the Linux kernel.
        Usage:
            Display network configuration: ifconfig
            Check routing tables: route

### Installation
To install the debugging utilities, run the install_debug_utils.sh script:

```bash

./install_debug_utils.sh
```

### Uninstallation

To uninstall the debugging utilities, run the uninstall_debug_utils.sh script:

```bash
./uninstall_debug_utils.sh
```
