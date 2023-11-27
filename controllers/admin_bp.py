from flask import Blueprint, render_template
from repository.admin_repository import AdminRepository

def admin_bp(connection):
    admin = Blueprint(
        'admin',
        __name__,
        template_folder='templates/',
        static_folder='static/',
        url_prefix="/admin"
    )

    repository = AdminRepository(connection=connection)

    @admin.route('/')
    def admin_page():
        table_names = repository.get_table_names()
        return render_template('admin.html', table_names=table_names)

    @admin.route('/<string:table_name>')
    def table_page(table_name):
        table_headers, table_content = repository.get_table_content(table_name)
        return render_template('table.html', table_headers=table_headers, table_content=table_content)

    return admin
