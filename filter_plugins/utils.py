from re import sub as regex_replace


class FilterModule(object):

    def filters(self):
        return {
            "safe_key": self.safe_key,
            "fallback": self.fallback,
            "prepare_letsencrypt": self.prepare_letsencrypt,
        }

    @staticmethod
    def safe_key(key: str) -> str:
        return regex_replace(r'[^0-9a-zA-Z\.]+', '', key.replace(' ', '_'))

    @staticmethod
    def fallback(opt1: str, opt2: str) -> str:
        if opt1 not in [None, '', 'None', 'none', ' ']:
            return opt1

        return opt2

    @staticmethod
    def prepare_letsencrypt(site: dict, name: str) -> dict:
        domains = [site['domain']]
        domains.extend(site['aliases'])
        return {
            name: {
                'domains': domains,
                'email': site['letsencrypt']['email'],
                'key_size': site['letsencrypt']['key_size'],
                'state': site['state'],
            }
        }
