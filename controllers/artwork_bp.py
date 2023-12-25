from flask import Blueprint, render_template, request, redirect, url_for, abort
from repository.artwork_repository import ArtworkRepository
from repository.artwork_repository import Artwork

def artwork_bp(connection):
    artwork = Blueprint(
        'artwork',
        __name__,
        template_folder='../templates/artwork',
        static_folder='static/',
        url_prefix="/artwork"
    )

    repository = ArtworkRepository(connection=connection)

    @artwork.route('/', methods=['GET', 'POST'])
    def artwork_page():
        if request.method == "GET":
            media = repository.get_all_artwork()
            return render_template('artwork.html', artwork=media)


        
    @artwork.route('/delete', methods=['GET', 'POST'])
    def delete_artwork():
        values = {"uuid": ""}
        if request.method == 'GET':
            return render_template("edit_artwork.html", values = values)
        else:
            if repository.validation_artworkid(request.form["uuid"])[0][0]>0:
                uuid = request.form["uuid"]
                new_artwork = Artwork(uuid, "","","","")
                repository.delete_artwork(new_artwork)
                return redirect(url_for("artwork.artwork_page"))   
            else:
                error_message = "No such artwork. Please enter another id."
                return render_template("edit_artwork.html", values=values, error_message=error_message, object_ids=repository.get_object_ids())
                
        
    @artwork.route('/create', methods=['GET', 'POST'])
    def create_artwork():
        artwork = {"uuid": "", "iiifthumburl": "", "assistivetext": "", "created": "", "related":""}
        if request.method == 'GET':
            return render_template("edit_artwork.html", values = artwork, object_ids=repository.get_object_ids())
        else:
            uuid = request.form["uuid"]
            url = request.form["iiifthumburl"]
            assistivetext = request.form["assistivetext"]
            created = request.form["created"]
            related = request.form["related"]
            values = Artwork(uuid, url, created, related,assistivetext)
            if repository.validation_objectid(request.form["related"])[0][0] > 0:
                if repository.validation_artworkid(request.form["uuid"])[0][0]>0:
                    error_message = "Artwork is in use. Please enter another id."
                    return render_template("edit_artwork.html", values=values, error_message=error_message, object_ids=repository.get_object_ids())
                else:
                    repository.add_artwork(values)
                    return redirect(url_for("artwork.artwork_page"))
            else:
                error_message = "No object found. Please create object first."
                return render_template("edit_artwork.html", values=values, error_message=error_message, object_ids=repository.get_object_ids())


    @artwork.route('/edit', methods=['GET', 'POST'])
    def artwork_edit_page():
        values = {"uuid": "", "iiifthumburl": "", "assistivetext": "", "created": "", "related":""}
        if request.method == "GET":
            return render_template("edit_artwork.html", values = values)
        else:
            uuid = request.form["uuid"]
            url = request.form["iiifthumburl"]
            assistivetext = request.form["assistivetext"]
            created = request.form["created"]
            related = request.form["related"]
            artwork = Artwork(uuid, url, created,assistivetext,related)
            if repository.validation_objectid(request.form["related"])[0][0] > 0:
                if repository.validation_artworkid(request.form["uuid"])[0][0]>0:
                    repository.update_artwork(artwork)
                    return redirect(url_for("artwork.artwork_page"))
                else:
                    error_message = "No such artwork!"
                    return render_template("edit_artwork.html", values=artwork, error_message=error_message, object_ids=repository.get_object_ids())
            else:
                error_message = "No such object!"
                return render_template("edit_artwork.html", values=artwork, error_message=error_message, object_ids=repository.get_object_ids())

    return artwork
