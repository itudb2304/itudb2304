from flask import Blueprint, render_template, request, redirect, url_for, abort
from repository.media_repository import MediaRepository
from repository.media_repository import Media

def media_bp(connection):
    media = Blueprint(
        'media',
        __name__,
        template_folder='templates/',
        static_folder='static/',
        url_prefix="/media"
    )

    repository = MediaRepository(connection=connection)

    @media.route('/', methods=['GET', 'POST'])
    def media_page():
        if request.method == "POST":
            if 'media-search' in request.form:
                req = request.form['media-search']
                media = repository.get_constituent_media_search(req)
                return render_template('media.html', media=media)
        else:
            media = repository.get_constituent_media()
            return render_template('media.html', media=media)


        
    @media.route('/delete', methods=['GET', 'POST'])
    def delete_media():
        if request.method == 'GET':
            values = {"mediaid": "", "table": ""}
            return render_template("edit_media.html", values = values)
        else:
            media_id = request.form["mediaid"]
            new_artwork = Media(media_id, "","","","")
            repository.delete_media(new_artwork)
            return redirect(url_for("media.media_page"))
        
    @media.route('/create', methods=['GET', 'POST'])
    def create_media():
        if request.method == 'GET':
            values = {"mediaid": "", "title": "", "description": "", "thumbnailurl": "", "playurl": "", "related":""}
            return render_template("edit_media.html", values = values)
        else:
            id = request.form["mediaid"]
            title = request.form["title"]
            description = request.form["description"]
            url = request.form["thumbnailurl"]
            play = request.form["playurl"]
            related = request.form["related"]
            media = Media(id, title, description, url, play)
            repository.add_media(media, related)
            return redirect(url_for("media.media_page"))
        


    @media.route('/edit', methods=['GET', 'POST'])
    def media_edit_page():
        if request.method == "GET":
            values = {"mediaid": "", "title": "", "description": "", "thumbnailurl": "", "playurl": ""}
            return render_template("edit_media.html", values = values)
        else:
            mediaid = request.form["mediaid"]
            title = request.form["title"]
            description = request.form["description"]
            url = request.form["thumbnailurl"]
            play = request.form["playurl"]
            media = Media(mediaid, title, description, url, play)
            repository.update_media(media)
            return redirect(url_for("media.media_page"))


    return media
