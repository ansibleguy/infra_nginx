from re import sub as regex_replace


class FilterModule(object):

    def filters(self):
        return {
            "safe_key": self.safe_key,
            "ensure_list": self.ensure_list,
            "prepare_letsencrypt": self.prepare_letsencrypt,
        }

    @staticmethod
    def safe_key(key: str) -> str:
        return regex_replace(r'[^0-9a-zA-Z\.]+', '', key.replace(' ', '_'))

    @staticmethod
    def ensure_list(data: (str, list)) -> list:
        # if user supplied a string instead of a list => convert it to match our expectations
        if isinstance(data, list):
            return data

        return [data]

    @classmethod
    def prepare_letsencrypt(cls, sites: dict, state: str, email: str = None, only_site: str = None) -> dict:
        certs = {}
        for unsafe_name, site in sites.items():
            if only_site is None or (
                    unsafe_name == only_site or
                    only_site in unsafe_name or
                    unsafe_name in only_site
            ):

                try:
                    if site['ssl']['mode'] == 'letsencrypt':
                        _name = cls.safe_key(unsafe_name)
                        _domains = [site['domain']]
                        _state, _email, _key_size = state, email, None

                        if 'aliases' in site:
                            _domains.extend(site['aliases'])

                        if 'letsencrypt' in site:
                            if 'email' in site['letsencrypt']:
                                _email = site['letsencrypt']['email']

                            if 'key_size' in site['letsencrypt']:
                                _key_size = site['letsencrypt']['key_size']

                        if 'state' in site:
                            _state = site['state']

                        certs[_name] = {
                            'domains': _domains,
                            'email': _email,
                            'state': _state,
                        }

                        if _key_size is not None:
                            certs[_name]['key_size'] = _key_size

                except KeyError:
                    continue

        return certs
