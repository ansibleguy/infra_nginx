# Ansible Nginx Role

Role to configure a nginx webserver.

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


  * **Default config**:
    * Disabled: <TLS1.2, unsecure ciphers, autoindex, servertokens
    * Security headers: HSTS, X-Frame, Referrer-Policy, Content-Type nosniff, X-Domain-Policy, XXS-Protection
    * Limits to prevent DDoS
    * Logging to syslog
    * Using a Self-Signed certificate


  * **SSL modes** (_for more info see: [CERT ROLE](https://github.com/ansibleguy/infra_certs)_)
    * **selfsigned** => Generate self-signed ones
    * **ca** => Generate a minimal Certificate Authority and certificate signed by it
    * **letsencrypt** => Uses the LetsEncrypt certbot
    * **existing** => Copy certificate files or use existing ones


  * **Default opt-ins**:
    * restricting methods to POST/GET/HEAD


## Info

* **Note:** this role currently only supports debian-based systems


* **Note:** Most of this functionality can be opted in or out using the main defaults file and variables!


* **Note:** This role expects that the site's unencrypted 'server' will only redirect to its encrypted connection.


* **Note:** If you want all domain-names to get 'caught' by a site/server you need to add an underline '_' as alias or domain!<br>
This will also be done automatically if no domain is supplied.


* **Warning:** Not every setting/variable you provide will be checked for validity. Bad config might break the role!

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

      ssl:
        mode: 'existing'  # pre-existing certificates to be copied to the target server

    guys_statics:
      mode: 'serve'
      domain: 'static.guy.net'
      serve:
        path: '/var/www/static'
      ssl:
        mode: 'ca'  # create minimal ca with signed server-certificate

    git_stuff:
      mode: 'redirect'
      redirect:
        target: 'https://github.com/ansibleguy'
      ssl:
        mode: 'letsencrypt'
      letsencrypt:
        email: 'nginx@template.ansibleguy.net'

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
