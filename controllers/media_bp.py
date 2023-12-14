from flask import Blueprint, render_template, request
from repository.media_repository import MediaRepository

def media_bp(connection):
    media = Blueprint(
        'media',
        __name__,
        template_folder='templates/',
        static_folder='static/',
        url_prefix="/media"
    )

    repository = MediaRepository(connection=connection)

    @media.route('/')
    def media_page():
        page = request.args.get('page', 1, type=int)
        media = repository.get_media(page)
        return render_template('media.html', media=media)
    return media
