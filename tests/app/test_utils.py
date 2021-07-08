from uuid import uuid4

import pytest

from app.utils import assess_contact_type, download_link, get_cdn_domain


def test_get_cdn_domain_on_localhost(client, mocker):
    mocker.patch.dict('app.current_app.config', values={'ADMIN_BASE_URL': 'http://localhost:6012'})
    domain = get_cdn_domain()
    assert domain == 'static-logos.notify.tools'


def test_get_cdn_domain_on_non_localhost(client, mocker):
    mocker.patch.dict('app.current_app.config', values={'ADMIN_BASE_URL': 'https://some.admintest.com'})
    domain = get_cdn_domain()
    assert domain == 'static-logos.admintest.com'


@pytest.mark.parametrize(
    "contact_info,expected_result",
    [
        ("07123456789", "other"),
        ("pinkdiamond@homeworld.gem", "email"),
        ("pink.diamond@digital.diamond-office.gov.uk", "email"),
        ("https://homeworld.gem/contact-us", "link"),
        ("http://homeworld.gem/contact-us", "link"),
        ("www.homeworld.gem", "other"),
        ("homeworld.gem", "other"),
        ("pinkdiamond", "other")
    ]
)
def test_assess_contact_type_recognises_email_phone_and_link(contact_info, expected_result):
    assert assess_contact_type(contact_info) == expected_result


def test_download_link(client):
    service_id = uuid4()
    document_id = uuid4()
    key = '1234'
    filename = 'filename.pdf'
    expected_url = (
        f"http://test-doc-download-api/services/{service_id}/documents/{document_id}?key={key}&filename={filename}"
    )
    assert download_link(service_id, document_id, key, filename) == expected_url


def test_download_link_no_filename(client):
    service_id = uuid4()
    document_id = uuid4()
    key = '1234'
    filename = None
    expected_url = (
        f"http://test-doc-download-api/services/{service_id}/documents/{document_id}?key={key}"
    )
    assert download_link(service_id, document_id, key, filename) == expected_url
