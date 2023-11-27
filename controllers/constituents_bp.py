from flask import Blueprint, render_template
from repository.constituent_repository import ConstituentRepository

def constituents_bp(connection):
    constituents = Blueprint(
        'constituents',
        __name__,
        template_folder='templates/',
        static_folder='static/',
        url_prefix="/constituents"
    )

    repository = ConstituentRepository(connection=connection)

    @constituents.route('/')
    def constituents_page():
        constituents = repository.get_all_constituents()
        return render_template('constituents.html', constituents=constituents)

    return constituents
