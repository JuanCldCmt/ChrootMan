# ChrootMan - Chroot Manager

Manage chroots in cli, with ease.

# Development Roadmap

- [x] v0.1 yaml processing, args processing
  - [x] config file
  - [x] args processing
- [x] v0.2 basic feature complete
  - [x] `info` show info
  - [x] `mount` mounts the chroot
  - [x] `unmount` unmount the chroot
  - [x] `login` enter shell for the chroot
- [ ] v0.3 advanced features
  - [ ] automatic distro detection
    - [ ] `update` update software on target chroot
    - [ ] `conf-update` automatic config generation, based on what's in `~/.local/var/chroot/`
    - [ ] `launch` mount chroot, launch program, and unmount after program closed in another background process.
  - [ ] Colorful output and debug info
  - [ ] `install` download and install chroots from presets
