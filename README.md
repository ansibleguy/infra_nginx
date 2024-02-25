[![Nginx](https://nginx.org/nginx.png)](https://nginx.org)

# Ansible Role - Nginx Webserver

Ansible Role to deploy one or multiple NGINX sites on a linux server.

[![Molecule Test Status](https://badges.ansibleguy.net/infra_nginx.molecule.svg)](https://github.com/ansibleguy/_meta_cicd/blob/latest/templates/usr/local/bin/cicd/molecule.sh.j2)
[![YamlLint Test Status](https://badges.ansibleguy.net/infra_nginx.yamllint.svg)](https://github.com/ansibleguy/_meta_cicd/blob/latest/templates/usr/local/bin/cicd/yamllint.sh.j2)
[![PyLint Test Status](https://badges.ansibleguy.net/infra_nginx.pylint.svg)](https://github.com/ansibleguy/_meta_cicd/blob/latest/templates/usr/local/bin/cicd/pylint.sh.j2)
[![Ansible-Lint Test Status](https://badges.ansibleguy.net/infra_nginx.ansiblelint.svg)](https://github.com/ansibleguy/_meta_cicd/blob/latest/templates/usr/local/bin/cicd/ansiblelint.sh.j2)
[![Ansible Galaxy](https://badges.ansibleguy.net/galaxy.badge.svg)](https://galaxy.ansible.com/ui/standalone/roles/ansibleguy/infra_nginx)

Molecule Logs: [Short](https://badges.ansibleguy.net/log/molecule_infra_nginx_test_short.log), [Full](https://badges.ansibleguy.net/log/molecule_infra_nginx_test.log)

**Tested:**
* Debian 11
* Debian 12

## Install

```bash
# latest
ansible-galaxy role install git+https://github.com/ansibleguy/infra_nginx

# from galaxy
ansible-galaxy install ansibleguy.infra_nginx

# or to custom role-path
ansible-galaxy install ansibleguy.infra_nginx --roles-path ./roles

# install dependencies
ansible-galaxy install -r requirements.yml

# if you want to use basic-auth: install python dependencies
python3 -m pip install -r requirements.txt
```

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
  * Option to filter 'locations' by GeoIP => COMING SOON (:

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
    * Blocking of Known Script-Bots
    * Blocking of known Bad-Crawler-Bots

## Info

* **Note:** this role currently only supports debian-based systems


* **Note:** Most of the role's functionality can be opted in or out.

  For all available options - see the default-config located in the main/site defaults-file!


* **Info:** Many variables can be set either on 'global' or 'per-site' scope.

  Site config is always overruling the global one.


* **Note:** This role expects that the site's unencrypted 'server' will only redirect to its encrypted connection.


* **Note:** If you want all domain-names to get 'caught' by a site/server you need to add an underline '_' as alias or domain!<br>
This will also be done automatically if no domain is supplied.


* **Warning:** Not every setting/variable you provide will be checked for validity. Bad config might break the role!


* **Info:** To disable default settings and headers => just set their value to: '' (_empty string_)


* **Info:** If you are filtering web-requests via GeoIP filter using your firewall => LetsEncrypt will work with only opening port 80 to the world.

  Requests other than '.well-known/acme-challenge/' are just redirected to 443.


* **Info:** For LetsEncrypt renewal to work, you must allow outgoing connections to:

  80/tcp, 443/tcp+udp to acme-v02.api.letsencrypt.org, staging-v02.api.letsencrypt.org (_debug mode_) and r3.o.lencr.org


* **Info:** This role also supports configuring basic-auth.

  For advanced use-cases you might want to set [auth_request](http://nginx.org/en/docs/http/ngx_http_auth_request_module.html) in `site.config_additions_root` that can be used to implement OAuth-Proxies and so on.


## Usage

You want a simple Ansible GUI? Check-out my [Ansible WebUI](https://github.com/ansibleguy/webui)

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

      security:
        # very basic filtering of bad bots based on user-agent matching
        block_script_bots: true
        block_bad_crawler_bots: true

    guys_statics:
      mode: 'server'
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

    fileshare:
      mode: 'server'
      domain: 'files.guy.net'
      serve:
        path: '/var/www/files'

      basic_auth:
        enable: true
        provider: 'file'
        file:
          users:
            some_user: 'some_password'
```

### Execution

Run the playbook:
```bash
ansible-playbook -K -D -i inventory/hosts.yml playbook.yml
```

To only process a specific site: (_and safe time_)
```bash
ansible-playbook -K -D -i inventory/hosts.yml playbook.yml -e only_site=SITE_NAME
# note: multiple comma-separated sites should also work
```


There are also some useful **tags** available:
* base => only configure basics; sites will not be touched
* sites
* config => only update site config (_excluding certificates_)
* certs
* letsencrypt
* auth

To debug errors - you can set the 'debug' variable at runtime:
```bash
ansible-playbook -K -D -i inventory/hosts.yml playbook.yml -e debug=yes
```
