import re
from urllib.parse import urlencode, urlparse

from flask import current_app
from notifications_utils.recipients import EMAIL_REGEX_PATTERN


def get_cdn_domain():
    parsed_uri = urlparse(current_app.config['ADMIN_BASE_URL'])

    if parsed_uri.netloc.startswith('localhost'):
        return 'static-logos.notify.tools'

    subdomain = parsed_uri.hostname.split('.')[0]
    domain = parsed_uri.netloc[len(subdomain + '.'):]

    return "static-logos.{}".format(domain)


def assess_contact_type(service_contact_info):
    if re.search(EMAIL_REGEX_PATTERN, service_contact_info):
        return "email"
    if service_contact_info.startswith("http"):
        return "link"
    else:
        return "other"


def download_link(service_id, document_id, key, filename):
    query_params = urlencode({
        k: v for k, v
        in {'key': key, 'filename': filename}.items()
        if v
    })

    return '{}/services/{}/documents/{}?{}'.format(
        current_app.config['DOCUMENT_DOWNLOAD_API_HOST_NAME'],
        service_id,
        document_id,
        query_params,
    )
