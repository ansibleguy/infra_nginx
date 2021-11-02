# Ansible Nginx Role

Role to configure a nginx webserver.

**Tested:**
* Debian 11

## Functionality

* Package installation
  * Ansible dependencies (_minimal_)
  * Nginx
* Configuration
  * Support for multiple sites/servers
  * Three config-modes:
    * proxy (_default_)
    * serve
    * redirect
  * Default config:
    * Disabled: <TLS1.2, unsecure ciphers, autoindex, servertokens
    * Security headers: HSTS, X-Frame, Referrer-Policy, Content-Type nosniff, X-Domain-Policy, XXS-Protection
    * Limits to prevent DDoS
    * Logging to syslog
  * SSL modes
    * local => Copy certificate files or use existing ones
    * self-signed => Generate self-signed ones
    * letsencrypt => _Use letsencrypt certbot (NOT YET IMPLEMENTED)_
  * Default opt-ins:
    * restricting methods to POST/GET/HEAD


## Info

* **Note:** this role currently only supports debian-based systems


* **Note:** Most of this functionality can be opted in or out using the main defaults file and variables!


* **Note:** This role expects that the site's unencrypted 'server' will only redirect to its encrypted connection.


* **Note:** If you want all domain-names to get 'catched' by a site/server you need to add an underline '_' as alias or domain!<br>
This will also be done automatically if no domain is supplied.

## Requirements

* Community collection: ```ansible-galaxy install -r requirements.yml```


## Usage

Just define the 'nginx' dictionary the sites you want to configure!

All options can be found in the [main defaults file](https://github.com/ansibleguy/infra_nginx/blob/stable/defaults/main.yml)!

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

      ssl:
        mode: 'local'  # pre-existing certificate
        path_key: '/etc/nginx/ssl/some.guy.net.key'
        path_pub: '/etc/nginx/ssl/some.guy.net.bundle.crt'  # public cert should be bundled with its ca-certificate

    guys_statics:
      mode: 'serve'
      domain: 'static.guy.net'
      serve:
        path: '/var/www/static'

      ssl:
        mode: 'letsencrypt'  # not yet implemented..

    git_stuff:
      mode: 'redirect'
      redirect:
        target: 'https://github.com/ansibleguy'

```

Run the playbook:
```bash
ansible-playbook -K -D -i inventory/hosts.yml playbook.yml
```

There are also some useful **tags** available:
* base => only configure basics; sites will not be touched
* sites
* config
* certs
