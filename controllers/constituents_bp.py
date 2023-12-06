from flask import Blueprint, render_template
from repository.constituent_repository import ConstituentRepository

def constituents_bp(cursor):
    constituents = Blueprint(
        'constituents',
        __name__,
        template_folder='templates/',
        static_folder='static/',
        url_prefix="/constituents"
    )

    repository = ConstituentRepository(cursor=cursor)

    @constituents.route('/')
    def constituents_page():
        constituents = repository.get_all_constituents()
        return render_template('constituents.html', constituents=constituents)
    
    @constituents.route('/<int:id>')
    def constituent_by_id(id: int):
        constituent = repository.get_constituent_by_id(id)
        return f"{constituent.forwarddisplayname}"
    
    @constituents.route('/<string:name>')
    def constituent_by_name(name: str):
        constituents = repository.get_constituents_by_name(name=name)
        return render_template('constituents.html', constituents=constituents)

    return constituents
