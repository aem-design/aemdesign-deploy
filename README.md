AEM Design Deploy
=================

Repository for deploying components to target Services using Ansible

Playbooks
=========
Description for playbooks

```
playbooks/service/author.yml                  # prepare host for author container
playbooks/service/dispatcher.yml              # prepare host for dispatcher container
playbooks/docker/command.yml                  # reusable playbook for running docker commands
playbooks/docker/container-remove.yml         # remove aem and solr containers
playbooks/service/esb.yml                     # build mule esb image
vm-localdev.yml                               # setup load dev vm with all applicaiton services
playbooks/service/management.yml              # build docker images nexus, jenkins, management services
playbooks/operation/backup-aem.yml            # run backup job on author and publish instances
playbooks/operation/restart-author.yml        # restart author instance
playbooks/operation/restart-publish.yml     # restart publish instance
playbooks/operation/restore-aem.yml           # restore aem instance from backup
playbooks/service/publish.yml               # prepare host for publish container
playbooks/service/security.yml                # rotate ssh keys on host
site.yml                                      # deploy application stack
```

Directory Layout
================

Directory structure and purpose

```
inventory/
    production            # inventory file for production servers
    localdev              # inventory file for local dev vm
    staging               # inventory file for staging environment

group_vars/
   group1                 # here we assign variables to particular groups
   group2                 # ""

host_vars/
   hostname1              # if systems need specific variables, put them here
   hostname2              # ""

library/                  # if any custom modules, put them here (optional)
filter_plugins/           # if any custom filter plugins, put them here (optional)

site.yml                  # master playbook

playbooks/                # folder for sub playbooks that are included in site.yml
    service/              # make subflders to keep root clean
        author.yml        # playbook for author tier, *** NOTE: need to explicitly include vars from group_vars ***
        publish.yml       # playbook for publish tier, *** NOTE: need to explicitly include vars from group_vars ***
        nexus.yml         # playbook for nexus tier, *** NOTE: need to explicitly include vars from group_vars ***

roles/
    common/               # this hierarchy represents a "role"
        tasks/            #
            main.yml      #  <-- tasks file can include smaller files if warranted
        handlers/         #
            main.yml      #  <-- handlers file
        templates/        #  <-- files for use with the template resource
            ntp.conf.j2   #  <------- templates end in .j2
        files/            #
            bar.txt       #  <-- files for use with the copy resource
            foo.sh        #  <-- script files for use with the script resource
        vars/             #
            main.yml      #  <-- variables associated with this role
        defaults/         #
            main.yml      #  <-- default lower priority variables for this role
        meta/             #
            main.yml      #  <-- role dependencies

    aem/              # same kind of structure as "common" was above, done for the webtier role
    jenkins/          # ""
    nexus/            # ""
    ...
```

Debug
=======

add base images to local registry

```bash
docker tag docker.io/java:8-jdk 192.168.27.2:5000/docker.io/java:8-jdk && docker push 192.168.27.2:5000/docker.io/java
docker tag docker.io/debian:jessie 192.168.27.2:5000/docker.io/debian:jessie && docker push 192.168.27.2:5000/docker.io/debian
docker tag docker.io/ubuntu:14.04 192.168.27.2:5000/docker.io/ubuntu:14.04 && docker push 192.168.27.2:5000/docker.io/ubuntu
docker tag docker.io/centos:centos7 192.168.27.2:5000/docker.io/centos:centos7 && docker push 192.168.27.2:5000/docker.io/centos
docker tag docker.io/alpine:latest 192.168.27.2:5000/docker.io/alpine:latest && docker push 192.168.27.2:5000/docker.io/alpine
```

remove all of the build images

```bash
docker rmi  192.168.27.2:5000/aemdesign/jenkins aemdesign/jenkins aemdesign/jenkins-base 192.168.27.2:5000/aemdesign/jenkins-base \
            192.168.27.2:5000/aemdesign/jenkins-data aemdesign/jenkins-data aemdesign/gitlab 192.168.27.2:5000/aemdesign/gitlab \
            192.168.27.2:5000/aemdesign/gitlab-data aemdesign/gitlab-data aem 192.168.27.2:5000/aem \
            192.168.27.2:5000/aem-data aem-data aem-dispatcher 192.168.27.2:5000/aem-dispatcher aem-dispatcher-data \
            192.168.27.2:5000/aem-dispatcher-data 192.168.27.2:5000/aem-base aem-base aem-apache 192.168.27.2:5000/aem-apache
```

delete publish container container and volumes

```bash
docker rm publish-dispatcher -f; \
docker rm publish -f; \
docker volume rm publish-repository publish-logs publish-backup publish-dispatcher-repository publish-dispatcher-cache publish-dispatcher-logs;
```

delete author and author-dispatcher container and volumes

```bash
docker rm author-dispatcher -f; \
docker rm author -f; \
docker volume rm author-repository author-logs author-backup author-dispatcher-repository author-dispatcher-cache author-dispatcher-logs;
```

delete author container and volumes

```bash
docker rm author && \
convoy umount author-backup && \
convoy umount author-logs && \
convoy umount author-repository && \
docker volume rm author-backup && \
docker volume rm author-logs && \
docker volume rm author-repository
```


delete author and publish and all dispatcher containers, images and volumes

```bash
docker rm author-dispatcher -f; \
docker rm publish-dispatcher -f; \
docker rm author -f; \
docker rm publish -f; \
docker rmi \
aemdesign/dispatcher  192.168.27.2:5000/aemdesign/dispatcher \
aemdesign/aem:6.2           192.168.27.2:5000/aemdesign/aem:6.2 \
aemdesign/aem-base          192.168.27.2:5000/aemdesign/aem-base; \
docker volume rm    author-repository author-logs author-backup \
                    publish-repository publish-logs publish-backup \
                    author-dispatcher-repository author-dispatcher-cache author-dispatcher-logs \
                    publish-dispatcher-repository publish-dispatcher-cache publish-dispatcher-logs;
```

General Usage Commands
======================

1. run playbooks without image build

```bash
./site-localdev --skip-tags docker-image
```
or
``` bash
ansible-playbook -i inventory/localdev site.yml --skip-tags=docker-image
```

2. enable playbook debug tasks and task outputs, they are there but have no_log=true so they do not print outputs

```bash
./site-localdev debug_hide=false
```

3. debug playbook by running ansible debug, very very very very verbose

```bash
./site-localdev -vvvvv
```

4. deploy to another server using the site playbook and another ssh key

```bash
ansible-playbook site.yml -i inventory/localdev --extra-vars "ansible_host=54.206.123.220 ansible_ssh_user=devops ansible_ssh_private_key_file={{ inventory_dir  }}/../../aemdesign-vm/keys/current/devops docker_volume_driver=local"
```
5. to run a specific playbook within the parent site.yml, use the `--limit` or `-l` flag to specify which playbook `hosts` to run.

```bash
ansible-playbook site.yml --inventory-file=./inventory/localdev -l dispatcher-publish
```

6. to limit playbook run to a specific host

```bash
./site-localdev --limit selenium-grid*
```