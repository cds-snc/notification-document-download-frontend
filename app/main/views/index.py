from flask import abort, current_app, render_template, request
from notifications_python_client.errors import HTTPError

from app import service_api_client
from app.main import main
from app.utils import assess_contact_type


@main.route('/_status')
def status():
    return "ok", 200


@main.route('/d/<base64_uuid:service_id>/<base64_uuid:document_id>', methods=['GET'])
def landing(service_id, document_id):
    key = request.args.get('key', None)
    if not key:
        abort(404)

    try:
        service = service_api_client.get_service(service_id)
    except HTTPError as e:
        abort(e.status_code)

    service_contact_info = service['data']['contact_link']
    contact_info_type = assess_contact_type(service_contact_info)
    return render_template(
        'views/index.html',
        service_id=service_id,
        service_name=service['data']['name'],
        service_contact_info=service_contact_info,
        contact_info_type=contact_info_type,
        document_id=document_id,
        key=key
    )


@main.route('/d/<base64_uuid:service_id>/<base64_uuid:document_id>/download', methods=['GET'])
def download_document(service_id, document_id):
    key = request.args.get('key', None)
    if not key:
        abort(404)

    download_link = '{}/services/{}/documents/{}?key={}'.format(
        current_app.config['DOCUMENT_DOWNLOAD_API_HOST_NAME'],
        service_id,
        document_id,
        key
    )

    try:
        service = service_api_client.get_service(service_id)
    except HTTPError as e:
        abort(e.status_code)

    service_contact_info = service['data']['contact_link']
    contact_info_type = assess_contact_type(service_contact_info)
    return render_template(
        'views/download.html',
        download_link=download_link,
        service_name=service['data']['name'],
        service_contact_info=service_contact_info,
        contact_info_type=contact_info_type,
    )
