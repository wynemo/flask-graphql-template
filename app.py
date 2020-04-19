import os
import json

from flask import Flask, request
from flask_graphql import GraphQLView

from db import db
from model import SimpleRecord
from schema.schema import schema

app = Flask(__name__)

# mysqlurl = 'mysql+pymysql://sonar:sonar&404@192.168.56.103:3306/sonar_dev?charset=utf8mb4'
mysqlurl = 'sqlite:///1.db'
config = dict(
    SQLALCHEMY_DATABASE_URI=mysqlurl,
    SQLALCHEMY_TRACK_MODIFICATIONS=True,
    SQLALCHEMY_COMMIT_ON_TEARDOWN=True,
    # SQLALCHEMY_POOL_SIZE=100,
    # SQLALCHEMY_MAX_OVERFLOW=200,
    SQLALCHEMY_POOL_RECYCLE=280, # 280 seconds, if mysql idle is longer you can set it to 7200s
    SQLALCHEMY_ECHO=True if os.environ.get('ECHO') else False,
)

app.config.update(**config)

db.init_app(app)
db.create_all(app=app)

app.add_url_rule('/simple_query', view_func=GraphQLView.as_view('if_you_say_so_ql', schema=schema, graphiql=True,
                                                                get_context=lambda: {'session':db.session}))


@app.route('/',  methods=['GET'])
def detail():
    data = request.args
    offset = data.get('offset', 0, int)
    limit = data.get('limit', 10, int)

    q = db.session.query(SimpleRecord)
    results = [each.to_dict() for each in q.offset(offset).limit(limit).all()]
    count = q.count()
    rv = json.dumps({
        'results': results,
        'total': count
    })
    return rv
