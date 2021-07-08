from urllib.parse import urlencode

from flask import abort, current_app, redirect, render_template, request
from notifications_python_client.errors import HTTPError

from app import service_api_client
from app.main import main
from app.utils import assess_contact_type, download_link


@main.route('/_status')
def status():
    return "ok", 200


@main.route('/d/<base64_uuid:service_id>/<base64_uuid:document_id>', methods=['GET'])
def landing(service_id, document_id):
    key = request.args.get('key', None)
    if not key:
        abort(404)

    filename = request.args.get('filename')

    return redirect(
        download_link(
            service_id,
            document_id,
            key,
            filename
        ),
        code=302
    )

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
        key=key,
        filename=request.args.get('filename'),
    )


@main.route('/d/<base64_uuid:service_id>/<base64_uuid:document_id>/download', methods=['GET'])
def download_document(service_id, document_id):
    key = request.args.get('key', None)
    if not key:
        abort(404)
    filename = request.args.get('filename')

    query_params = urlencode({
        k: v for k, v
        in {'key': key, 'filename': filename}.items()
        if v
    })

    download_link = '{}/services/{}/documents/{}?{}'.format(
        current_app.config['DOCUMENT_DOWNLOAD_API_HOST_NAME'],
        service_id,
        document_id,
        query_params,
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
