# Commander

Commander is a powerful command-line interface (CLI) scraping tool designed for managing and interacting with multiple network devices simultaneously.

## Features

- **Blazingly Fast:** Commander is optimized for speed, allowing you to execute commands swiftly across your network devices.
- **Multi-threaded:** Leverage the efficiency of multi-threading to process commands concurrently, ensuring quick and efficient communication with all devices.
- **Secure by Design:** Prioritizing security, Commander stores sensitive connection information, such as passwords and IPs locally on your computer, in [Keepass](https://keepass.info), a renowned open-source password manager.

## Problem Statement

Networks, especially in large-scale environments, often face challenges in maintaining standardization. The complexity grows, making it challenging for networking and IT teams to enforce uniform configurations across devices. Without proper tools, networks may become scattered and prone to inconsistencies, or administrators may spend hours manually configuring each device.

While tools like [Ansible](https://www.ansible.com/), [Puppet](https://www.puppet.com/), and [Chef](https://www.chef.io/) are excellent for maintaining standardization, they come with a steep learning curve, additional infrastructure management, and setup complexities.

Commander aims to provide a simpler alternative, allowing users to swiftly execute commands across multiple devices without the overhead of a complex infrastructure.

## Installation

Install Commander with a simple pip command:

```bash
pip install NetworkCommander
```

## compile from source

if you want to compile from source you can do that with [poetry](https://python-poetry.org/https://python-poetry.org/).

first you have to make sure poetry is installed
```bash
poetry --version
```

## Usage
### Version Check

Check the version of Commander:

```bash
poetry --version
```

after you did that you can start the build.

```bash
poetry install
poetry build
```

a folder named dist will apper with the .tar.gz and .whl files.

```bash
pip install ./dist/path/to/.whl
```

after that you can fully use commander

```bash
commander version
```


### Initialization

Before using Commander, ensure it's initialized. Run the following command to generate the keepass database and provide the password for it:

```bash
commander init
```

## Device Management
### List Devices

List all devices under your command, optionally filtered by tags:

```bash
commander device list --tag <tag_name>
```

### Add Device

Add a new device to the database, specifying the device's password:

```bash
commander device add "router1(cisco_ios) -> root@1.1.1.1"
```

Alternatively, you can provide a file containing device strings:

```bash
commander device add --devices_file path/to/devices_file
```

### Remove Device

Remove one or more devices from the database:

```bash
commander device remove <device_name_1> <device_name_2> ...
```

## Tag Management
### Add Tag

Add a tag to devices for better segmentation:

```bash
commander device tag add <tag_name> <device_name_1> <device_name_2> ...
```
### Remove Tag

Remove a tag from devices:

```bash
commander device tag remove <tag_name> <device_name_1> <device_name_2> ...
```

### List Tags

List all tags applied to devices:

```bash
commander device tag list
```
## Device Connectivity
### Ping Devices

Test connectivity to devices:

```bash
commander device ping --tag <tag_name>
```
### Command Deployment

Deploy commands to devices, either to all or specific devices:

```bash
commander device deploy  --permision_level "configure_terminal" --tag <tag_name> --device <device_name_1> "<command_1>" "<command_2>" 
```
Specify the permission level for command execution using the -p or --permission_level option.
Output Folder (Optional)

Save command output to a specified folder:

```bash
commander device deploy "<command>" --output_folder <path/to/output_folder>
```

Conclusion

Commander provides a streamlined solution for scraping network devices, offering speed and simplicity without the complexities of traditional configuration management tools. Empower your networking and IT teams to enforce standardization across your network effortlessly.

Have a great experience with Commander!