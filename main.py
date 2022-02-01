'''
Date: 2021-10-30 20:03:47
LastEditors: GC
LastEditTime: 2021-11-01 20:19:14
FilePath: \Flask-Project\main.py
'''
from website import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
