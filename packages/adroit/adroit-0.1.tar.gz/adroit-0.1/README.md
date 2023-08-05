# `adroit` - Ansible Docker Role Testing

Heavily opinionated tool for testing ansible roles using docker containers.

The tool will create a base image with the base role installed. This image
will be used for testing all roles.

For every role being tested, a docker container will be spun up, and an ad-hoc
playbook including only the one role will be ran twice: Once to verify that all
the tasks succeeded, then once again to ensure that the role is idempotent -
that is, that no new changes were introduced on the second run.
