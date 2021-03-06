[![Nginx](https://nginx.org/nginx.png)](https://nginx.org)

# Ansible Role - Nginx Webserver

Ansible Role to deploy one or multiple NGINX sites on a linux server.

[![Ansible Galaxy](https://img.shields.io/ansible/role/56760)](https://galaxy.ansible.com/ansibleguy/infra_nginx)
[![Ansible Galaxy Downloads](https://img.shields.io/badge/dynamic/json?color=blueviolet&label=Galaxy%20Downloads&query=%24.download_count&url=https%3A%2F%2Fgalaxy.ansible.com%2Fapi%2Fv1%2Froles%2F56760%2F%3Fformat%3Djson)](https://galaxy.ansible.com/ansibleguy/infra_nginx)

**Tested:**
* Debian 11

## Functionality

* **Package installation**
  * Ansible dependencies (_minimal_)
  * Nginx


* **Configuration**
  * Support for multiple sites/servers
  * Three **config-modes**:
    * proxy (_default_)
    * serve
    * redirect
  * Support for specific configurations using the 'config' and 'config_additions' parameters


  * **Default config**:
    * Disabled: <TLS1.2, unsecure ciphers, autoindex, servertokens
    * Security headers: HSTS, X-Frame, Referrer-Policy, Content-Type nosniff, X-Domain-Policy, XXS-Protection
    * Limits to prevent DDoS
    * Using a Self-Signed certificate
    * HTTP2 enabled with fallback to HTTP1.1
    * IPv6 support enabled


  * **SSL modes** (_for more info see: [CERT ROLE](https://github.com/ansibleguy/infra_certs)_)
    * **selfsigned** => Generate self-signed ones
    * **ca** => Generate a minimal Certificate Authority and certificate signed by it
    * **letsencrypt** => Uses the LetsEncrypt certbot
    * **existing** => Copy certificate files or use existing ones


  * **Default opt-ins**:
    * restricting methods to POST/GET/HEAD
    * status-page listener on localhost
    * Logging to syslog
    * http2


  * **Default opt-outs**:
    * proxy-mode caching

## Info

* **Note:** this role currently only supports debian-based systems


* **Note:** Most of this functionality can be opted in or out using the main defaults file and variables!


* **Note:** This role expects that the site's unencrypted 'server' will only redirect to its encrypted connection.


* **Note:** If you want all domain-names to get 'caught' by a site/server you need to add an underline '_' as alias or domain!<br>
This will also be done automatically if no domain is supplied.


* **Warning:** Not every setting/variable you provide will be checked for validity. Bad config might break the role!


* **Info:** To disable default settings and headers => just set their value to: ''

## Requirements

* Community collection and certificate role: ```ansible-galaxy install -r requirements.yml```


## Usage

### Config

Define the nginx dictionary as needed!

```yaml
nginx:
  config:
    client_max_body_size: '500m'
    ssl_session_timeout: '15m'
  
  sites:
    some_proxy:
      mode: 'proxy'
      domain: 'some.guy.net'
      aliases:
        - 'service.guy.net'

      port_ssl: 8443
      port_plain: 8080
      proxy:  # default proxy-target is localhost
        port: 50000  # target port
        
        cache:  # upstream content-caching
          enable: true

      ssl:
        mode: 'existing'  # pre-existing certificates to be copied to the target server

    guys_statics:
      mode: 'serve'
      domain: 'static.guy.net'
      serve:
        path: '/var/www/static'

      ssl:
        mode: 'ca'  # create minimal ca with signed server-certificate
      
      config:  # add settings as key-value pairs
        LimitRequestFields: 10
      config_additions:  # add a list of custom lines of config
        - 'location = /favicon.ico {alias /var/not_www/site_guys_statics/favicon.ico;}'

    git_stuff:
      mode: 'redirect'
      redirect:
        target: 'https://github.com/ansibleguy'

      ssl:
        mode: 'letsencrypt'
      letsencrypt:
        email: 'nginx@template.ansibleguy.net'

      security:
        restrict_methods: false

```

### Execution

Run the playbook:
```bash
ansible-playbook -K -D -i inventory/hosts.yml playbook.yml
```

There are also some useful **tags** available:
* base => only configure basics; sites will not be touched
* sites
* config => only update site config (_excluding certificates_)
* certs
