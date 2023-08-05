# `adroit` - Ansible Docker Role Testing

Heavily opinionated tool for testing Ansible roles using Docker containers.

### Assumptions and limitations

These are the current assumptions about your Ansible codebase which might prevent you from using Adroit. They are subject to change or improve.

- You only deploy (or only want to test) on modern systems with systemd as their init system.
- You have a `base` role which other roles can build upon. (If you don't need this, you can just have an empty `roles/base` directory).
- With the exception of depending on the base role, your Ansible roles are atomic, indepentent, and can be applied individually. `include_role` and dependencies defined in `meta` should still work, though.

Feel free to open a Github issue about any limitations that prevent you from using Adroit.

### How it works

1. Adroit builds a *core image* based on your distro of choice.
2. A container based on the core image is created. The `base` role will be applied to the container, and it is saved as the *base image*.
3. For each role you want to test, a container based on the base image is started, and the role under test will be applied.

Adroit will check if the role playbook fails, and will also run the playbook a second time to test for idempotency - if there are any changes on the second run, we consider it a failure.

### Precautions

To properly test Ansible using Docker containers, systemd needs to be running inside the containers. This requires the containers to run in privileged mode. There is a security risk involved here, check your base images and playbooks accordingly.

## Usage

In a virtualenv or whatever you prefer: `pip install adroit`

In the root directory of your Ansible tree structure, which should at least contain a `roles` directory, run this command:

```bash
adroit -d debian:stretch myrole
```

Where `debian:stretch` is the image you want to base your tests on. Currently supported are Debian, Ubuntu and CentOS.

### Customizing your roles for testing

Certain tasks simply cannot be ran inside a Docker container - for example, mounting `/proc` with `hidepid=2`. You should add a `when` clause to these tasks. Example:

```yaml
- when: ansible_virtualization_type != 'docker'
  import_tasks: configure_network.yml
```

If you need certain variables to be set which aren't in `defaults` or `vars` but should be set during testing, you can create a file like `roles/myrole/testing/test_vars.yml` and it will be applied when testing that particular role.

## License

The contents of this repository is released under the [MIT license](http://opensource.org/licenses/MIT). See the LICENSE file included for details.
