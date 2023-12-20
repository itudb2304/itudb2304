from flask import Blueprint, render_template, request, redirect, url_for, flash
from repository.constituent_repository import ConstituentRepository

def constituents_bp(connection):
    constituents = Blueprint(
        'constituents',
        __name__,
        template_folder='../templates/constituents',
        static_folder='static/',
        url_prefix="/constituents"
    )

    repository = ConstituentRepository(connection=connection)

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
            return render_template('constituents.html', constituents_list=constituents)
    
    @constituents.route('/<string:name>', methods=['GET', 'POST'])
    def constituent_by_name(name: str):
        constituents = repository.get_constituents_by_name(name=name)
        if request.method == 'POST':
            if 'constituent-search' in request.form:
                req = request.form['constituent-search']
                return redirect( url_for('.constituent_by_name', name=req) )
            elif 'add-constituent' in request.form:
                req = request.form['add-constituent']
                return redirect(url_for('.add_constituent'))
        return render_template('constituents.html', constituents_list=constituents)
    
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
        
    @constituents.route('/<int:id>')
    def constituent_objects(id: int):
        constituent_objects = repository.constituent_objects(id)
        print(constituent_objects)
        return render_template('constituent_objects.html',constituent_objects=constituent_objects)


    return constituents
