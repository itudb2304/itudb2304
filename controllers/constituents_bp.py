from flask import Blueprint, render_template, request, redirect, url_for, flash
from repository.constituent_repository import ConstituentRepository
from repository.media_repository import MediaRepository
from repository.objects_repository import ObjectsRepository

def constituents_bp(connection):
    constituents = Blueprint(
        'constituents',
        __name__,
        template_folder='../templates/constituents',
        static_folder='static/',
        url_prefix="/constituents"
    )

    repository = ConstituentRepository(connection=connection)
    objects_repository = ObjectsRepository(connection=connection)
    media_repository = MediaRepository(connection=connection)
    constituent_attributes = [
        "ulanid",
        "preferred-display-name",
        "forward-display-name",
        "lastname",
        "display-date",
        "artist-of-nga-object",
        "birthyear",
        "deathyear",
        "visualbrowsertimespan",
        "nationality",
        "constituent-type",
        "wikidataid"
    ]

    constituent_objects_attributes = [
        "objectid",
        "constituentid",
        "roletype",
        "role",
        "displaydate",
        "displayorder",
        "country"
    ]

    @constituents.route('/', methods=['GET', 'POST'])
    def constituents_page():
        if request.method == 'POST':
            if 'constituent-search' in request.form:
                req = request.form['constituent-search']
                return redirect( url_for('.constituent_by_name', name=req) )
            elif 'add-constituent' in request.form:
                req = request.form['add-constituent']
                return redirect(url_for('.add_constituent'))
        else:
            constituents = repository.get_all_constituents()
            constituent_id = request.args.get('constituent_id')
            media = media_repository.get_constituent_media_by_id(constituent_id)
            return render_template('constituents.html', constituents_list=constituents,  media=media, get_constituent_media_by_id=media_repository.get_constituent_media_by_id)

    @constituents.route('/<string:name>', methods=['GET', 'POST'])
    def constituent_by_name(name: str):
        constituents = repository.get_constituents_by_name(name=name)
        
        if request.method == 'POST':
            print("POST")
            if 'constituent-search' in request.form:
                req = request.form['constituent-search']
                return redirect( url_for('.constituent_by_name', name=req) )
            elif 'add-constituent' in request.form:
                req = request.form['add-constituent']
                return redirect(url_for('.add_constituent'))
        return render_template('constituents.html', constituents_list=constituents, get_constituent_media_by_id=media_repository.get_constituent_media_by_id)

    @constituents.route('/add', methods=['GET','POST'])
    def add_constituent():
        if request.method == 'GET':
            return render_template('constituents_add.html')
        else:
            attributes = []
            for key in constituent_attributes:
                if key in request.form and len(request.form[key]):
                    attributes.append(request.form[key])
                else:
                    attributes.append(None)
            repository.add_constituent(attributes=attributes)
            flash('Constituent has been added successfully.')
            return render_template('constituents_add.html')
        
    @constituents.route('/<int:id>', methods=['GET', 'POST'])
    def constituent_objects(id: int):
        if request.method == 'GET':
            constituent_objects = repository.constituent_objects(id)
            return render_template('constituent_objects.html',constituent_objects=constituent_objects, constituentID=id)
        else:
            return redirect(url_for('.add_constituent_object', id=id))
    
    @constituents.route('/<int:id>/add-object', methods=['GET', 'POST'])
    def add_constituent_object(id: int):
        if request.method == 'GET':
            return render_template("add_constituent_object.html", object_ids=repository.get_object_ids(), constituent_ids=repository.get_constituent_ids(), current_constituentID=id)
        else:
            attributes = []
            for att in constituent_objects_attributes:
                if att in request.form:
                    attributes.append(request.form[att])
                else:
                    attributes.append(None)
            attributes.append(objects_repository.get_object_by_objectid(attributes[0]).title)
            print(attributes)
            attributes.append(repository.get_constituent_by_id(attributes[1]).forwarddisplayname)
            repository.add_constituent_object(attributes=attributes)
            flash('Constituent object has been added successfully.')
            return render_template("add_constituent_object.html", object_ids=repository.get_object_ids(), constituent_ids=repository.get_constituent_ids(), current_constituentID=id)
    
    @constituents.route('/<int:constituent_id>/<int:relation_id>/', methods=['GET', 'POST'])
    def update_constituent_object(constituent_id: int, relation_id: int):
        if request.method == 'GET':
            constituent_object = repository.get_constituent_object_by_id(relation_id)
            return render_template("edit_constituent_object.html", constituent_object = constituent_object)
        else:
            attributes = []
            for att in constituent_objects_attributes:
                if att in request.form:
                    attributes.append(request.form[att])
                else:
                    attributes.append(None)
            repository.update_constituent_object(attributes=attributes, relationid=relation_id)
            flash('Constituent has been updated successfully.')
            constituent_objects = repository.constituent_objects(constituentid=constituent_id)
            return redirect(url_for('.constituent_objects', id=constituent_id))

    @constituents.route('/<int:constituentid>/<int:relationid>/delete', methods=['GET','POST'])
    def delete_constituent_object(constituentid: int, relationid: int):
        repository.delete_constituent_object(relationid=relationid)
        return redirect(url_for('.constituent_objects', id=constituentid))

    return constituents
