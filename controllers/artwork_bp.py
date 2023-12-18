from flask import Blueprint, render_template, request, redirect, url_for, abort
from repository.artwork_repository import ArtworkRepository
from repository.artwork_repository import Artwork

def artwork_bp(connection):
    artwork = Blueprint(
        'artwork',
        __name__,
        template_folder='templates/',
        static_folder='static/',
        url_prefix="/artwork"
    )

    repository = ArtworkRepository(connection=connection)

    @artwork.route('/', methods=['GET', 'POST'])
    def artwork_page():
        if request.method == "GET":
            artwork = repository.get_all_artwork()
            return render_template("artwork.html", artwork=artwork)
        else:
            ids = request.form.getlist("uuid")
            for id in ids:
                repository.delete_artwork(id)
            return redirect(url_for("artwork.artwork_page"))


    @artwork.route('/delete', methods=['GET', 'POST'])
    def delete_artwork():
        if request.method == 'GET':
            values = {"id": "", "url": "", "modified": "", "maxpixels": "", "height": ""}
            return render_template("edit_artwork.html", values = values)
        else:
            artwork_id = request.form["id"]
            artwork_url = request.form["url"]
            artwork_modified = request.form["modified"]
            artwork_maxpixels = request.form["maxpixels"]
            artwork_height = request.form["height"]
            
            new_artwork = Artwork(artwork_id, artwork_url, artwork_modified, artwork_maxpixels, artwork_height)
            repository.delete_artwork(new_artwork)
            return redirect(url_for("artwork.artwork_page"))
        
    @artwork.route('/create', methods=['GET', 'POST'])
    def create_artwork():
        if request.method == 'GET':
            values = {"id": "", "url": "", "modified": "", "maxpixels": "", "height": ""}
            return render_template("edit_artwork.html", values = values)
        else:
            artwork_id = request.form["id"]
            artwork_url = request.form["url"]
            artwork_modified = request.form["modified"]
            artwork_maxpixels = request.form["maxpixels"]
            artwork_height = request.form["height"]
            
            new_artwork = Artwork(artwork_id, artwork_url, artwork_modified, artwork_maxpixels, artwork_height)
            repository.add_artwork(new_artwork)
            return redirect(url_for("artwork.artwork_page"))
        


    @artwork.route('/edit', methods=['GET', 'POST'])
    def artwork_edit_page():
        if request.method == "GET":
            values = {"id": "", "url": "", "modified": "", "maxpixels": "", "height": ""}
            return render_template("edit_artwork.html", values = values)
        else:
            artwork_id = request.form["id"]
            artwork_url = request.form["url"]
            artwork_modified = request.form["modified"]
            artwork_maxpixels = request.form["maxpixels"]
            artwork_height = request.form["height"]
            artwork = Artwork(artwork_id, artwork_url, artwork_modified, artwork_maxpixels, artwork_height)
            repository.update_artwork(artwork)
            return redirect(url_for("artwork.artwork_page"))


    return artwork





    

    


   

