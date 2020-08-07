"""
Hanwei Wang
Time: 24-2-2020 8:27
Contact: hanwei_wang_94@outlook.com
Naming standard:
    name of a class: AbcdAbcd
    name of a method/function: abcdabcd
    name of a variable: abcd_abcd
    name of a instantiation: abcd_abcd
    # in English is the comments
"""

from Webapp import create_app

if __name__== '__main__':
    app = create_app()
    print(app.root_path)
    app.run(debug = False, port=800)