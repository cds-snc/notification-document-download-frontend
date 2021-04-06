import uuid

from bs4 import BeautifulSoup
from flask import url_for
from flask_wtf.csrf import CSRFError

from tests.conftest import skip_if_direct_download


def test_bad_url_returns_page_not_found(client):
    response = client.get('/bad_url')
    assert response.status_code == 404
    page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')
    assert page.h1.string.strip() == 'Page could not be found'


@skip_if_direct_download
def test_csrf_returns_400(client, mocker, sample_service):
    # we turn off CSRF handling for tests, so fake a CSRF response here.
    csrf_err = CSRFError('400 Bad Request: The CSRF tokens do not match.')
    mocker.patch('app.service_api_client.get_service', return_value={'data': sample_service})
    mocker.patch('app.main.views.index.render_template', side_effect=csrf_err)

    response = client.get(
        url_for(
            'main.landing',
            service_id=uuid.uuid4(),
            document_id=uuid.uuid4(),
            key='1234'
        )
    )

    assert response.status_code == 400
    page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')
    assert page.h1.string.strip() == 'Something went wrong, please go back and try again.'
