from flask import Blueprint, render_template, request, redirect, url_for, abort, flash
from repository.media_repository import MediaRepository
from repository.media_repository import Media

def media_bp(connection):
    media = Blueprint(
        'media',
        __name__,
        template_folder='../templates/media',
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
        values = {"mediaid": "", "table": ""}
        if request.method == 'GET':
            return render_template("edit_media.html", values = values)
        else:
            if repository.validation_mediaid(request.form["mediaid"])[0][0]>0:
                media_id = request.form["mediaid"]
                new_artwork = Media(media_id, "","","","")
                repository.delete_media(new_artwork)
                return redirect(url_for("media.media_page"))   
            else:
                error_message = "No such media. Please enter another id."
                return render_template("edit_media.html", values=values, error_message=error_message, object_ids=repository.get_object_ids())
                
        
    @media.route('/create', methods=['GET', 'POST'])
    def create_media():
        media = {"mediaid": "", "title": "", "description": "", "thumbnailurl": "", "playurl": "", "related":""}
        if request.method == 'GET':
            return render_template("edit_media.html", values = media, object_ids=repository.get_object_ids())
        else:
            if repository.validation_objectid(request.form["related"])[0][0] > 0:
                if repository.validation_mediaid(request.form["mediaid"])[0][0]>0:
                    error_message = "Mediaid is in use. Please enter another id."
                    return render_template("edit_media.html", values=values, error_message=error_message, object_ids=repository.get_object_ids())
                else:
                    id = request.form["mediaid"]
                    title = request.form["title"]
                    description = request.form["description"]
                    url = request.form["thumbnailurl"]
                    play = request.form["playurl"]
                    related = request.form["related"]
                    values = Media(id, title, description, url, play)
                    repository.add_media(values, related)
                    flash("Media added succesfully", 'success')
                    return redirect(url_for("media.media_page"))
            else:
                error_message = "No objects found. Please create objects first."
                return render_template("edit_media.html", values=values, error_message=error_message, object_ids=repository.get_object_ids())


    @media.route('/edit', methods=['GET', 'POST'])
    def media_edit_page():
        mediaid = request.form["mediaid"]
        title = request.form["title"]
        description = request.form["description"]
        url = request.form["thumbnailurl"]
        play = request.form["playurl"]
        media = Media(mediaid, title, description, url, play)
        if request.method == "GET":
            values = {"mediaid": "", "title": "", "description": "", "thumbnailurl": "", "playurl": ""}
            return render_template("edit_media.html", values = values)
        else:
            if repository.validation_objectid(request.form["related"])[0][0] > 0:
                if repository.validation_mediaid(request.form["mediaid"])[0][0]>0:
                    repository.update_media(media)
                    return redirect(url_for("media.media_page"))
                else:
                    error_message = "No such media!"
                    return render_template("edit_media.html", values=media, error_message=error_message, object_ids=repository.get_object_ids())
            else:
                error_message = "No such object!"
                return render_template("edit_media.html", values=media, error_message=error_message, object_ids=repository.get_object_ids())

    return media
