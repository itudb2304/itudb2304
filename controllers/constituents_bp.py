from flask import Blueprint, render_template, request, redirect, url_for
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
            return render_template('constituents.html', constituents=constituents)
    
    @constituents.route('/<int:id>')
    def constituent_by_id(id: int):
        constituent = repository.get_constituent_by_id(id)
        return f"{constituent.forwarddisplayname}"
    
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
        return render_template('constituents.html', constituents=constituents)
    
    @constituents.route('/add', methods=['GET','POST'])
    def add_constituent():
        attributes = request.args.get('list')
        return render_template('constituents_add.html')


    return constituents
