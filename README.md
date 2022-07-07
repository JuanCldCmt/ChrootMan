# ChrootMan - Chroot Manager

✨ Manage chroots in a breeze! 

## Features

🚀 mount, unmount file system, and execute commands in one go

🔥 Fully configurable through `yaml` configuration file

## Examples

🚧 Under construction 🚧

## Development Roadmap

- [x] v0.1 yaml processing, args processing
  - [x] config file
  - [x] args processing
- [x] v0.2 basic feature complete
  - [x] `info` show info
  - [x] `mount` mounts the chroot
  - [x] `unmount` unmount the chroot
  - [x] `login` enter shell for the chroot
- [ ] v0.3 advanced features
  - [x] PyPI file structure
  - [x] Install default config file when not found
  - [x] distro specific settings
    - [x] `update` update software on target chroot
    - [ ] `launch` mount chroot, launch program, and unmount after program closed in one go
    - [x] `list` lists available chroots
  - [x] Colorful output and debug info
  - [ ] `install` download and install chroots from presets
