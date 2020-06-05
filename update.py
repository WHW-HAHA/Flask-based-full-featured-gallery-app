"""
Hanwei Wang
Time: 18-5-2020 14:31
Contact: hanwei_wang_94@outlook.com
Naming standard:
    name of a class: AbcdAbcd
    name of a method/function: abcdabcd
    name of a variable: abcd_abcd
    name of a instantiation: abcd_abcd
    # in English is the comments
    # 中文的话是需要特别注意的地方以及需要检查的地方
""""""
Hanwei Wang
Time: 20-2-2020 10:32
Contact: hanwei_wang_94@outlook.com
Naming standard:
    name of a class: AbcdAbcd
    name of a method/function: abcdabcd
    name of a variable: abcd_abcd
    name of a instantiation: abcd_abcd
    # in English is the comments
    # 中文的话是需要特别注意的地方以及需要检查的地方
"""

import os


# claim and use .env or .flaskenv as setting files
# dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
# if os.path.exists(dotenv_path):
#     load_dotenv(dotenv_path)


def Update(app):
    ''' Create fake data '''
    from Webapp.fakes import update_post
    import click

    with app.app_context(): # give sqlalchemy an app context

        click.echo('Generating posts...')
        update_post()

        click.echo('Done.')

from Webapp import create_app
#
app = create_app()
Update(app)
app.run(debug = False)

