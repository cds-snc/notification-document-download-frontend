from uuid import uuid4

from bs4 import BeautifulSoup
from flask import url_for


def test_landing_page_en(client, mocker, sample_service):
    mocker.patch('app.service_api_client.get_service', return_value={'data': sample_service})
    service_id = uuid4()
    document_id = uuid4()
    response = client.get(
        url_for(
            'main.landing',
            service_id=service_id,
            document_id=document_id,
            key='1234'
        ),
        headers=[("Accept-Language", "en_CA")]
    )

    assert response.status_code == 200
    page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')
    button = page.find('div', class_='lang-button')

    assert page.find('title').text.strip() == 'GC Notify - Document download'
    assert button.text.strip() == 'Français'


def test_landing_page_fr(client, mocker, sample_service):
    mocker.patch('app.service_api_client.get_service', return_value={'data': sample_service})
    service_id = uuid4()
    document_id = uuid4()
    response = client.get(
        url_for(
            'main.landing',
            service_id=service_id,
            document_id=document_id,
            key='1234'
        ),
        headers=[("Accept-Language", "en_CA")]
    )
    page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')
    fr_url = page.find('div', class_='lang-button').find('a')['href']

    # Change lang
    response = client.get(fr_url, follow_redirects=True)
    page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')
    button = page.find('div', class_='lang-button')

    assert response.status_code == 200
    assert page.find('title').text.strip() == 'GC Notification - Téléchargement de fichiers'
    assert button.text.strip() == 'English'
