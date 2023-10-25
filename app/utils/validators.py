import re


class Validators:
    @staticmethod
    def url_regex(link):
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,63}|'
            r'[A-Z0-9-]{2,}(?<!-)))'  # domain...
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return bool(re.match(regex, link))
