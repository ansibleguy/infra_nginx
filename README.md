# Ansible Nginx Role

Role to configure a nginx webserver in one of three basic modes:
* proxy
* redirect
* serve

**Note:** this role currently only supports debian-based systems

**Tested:**
* Debian 11

## Functionality

This ansible role will do:
* Install nginx
* Configure certificates
  * Copy certificate files
  * Generate self-signed ones
  * _Use letsencrypt certbot (NOT YET AVAILABLE)_


## Usage

Just define the 'nginx' dictionary with all the keys you need.

Currently, this role does not support the configuration of multiple sites in one run.

For this you might need to loop its call.

All options can be found in the [main defaults file](https://github.com/ansibleguy/infra_nginx/blob/stable/defaults/main.yml)!

```yaml
nginx:
  mode: 'proxy'
  domain: 'some.guy.net'
  nginx_aliases:
    - 'another.guy.net'
  port_ssl: 8443
  port_plain: 8080
  proxy_port: 50000
```
