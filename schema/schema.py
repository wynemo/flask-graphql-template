from datetime import datetime

import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

from db import db
import util
from model import SimpleRecord as SimpleRecordModel


class SimpleRecordType(SQLAlchemyObjectType):
    class Meta:
        model = SimpleRecordModel


class Query(graphene.ObjectType):
    simple_records = graphene.List(SimpleRecordType,
                                   offset=graphene.Int(),
                                   limit=graphene.Int(),)

    def resolve_simple_records(self, info, offset=0, limit=10, **kwargs):
        query = SimpleRecordType.get_query(info).filter_by(**kwargs).offset(offset).limit(limit)  # SQLAlchemy query
        return query.all()


class CreateRecord(graphene.Mutation):
    """Create a record."""
    record = graphene.Field(lambda: SimpleRecordType, description="SimpleRecord created by this mutation.")

    class Arguments:
        ip = graphene.String()
        port = graphene.Int()
        username = graphene.String()
        password = graphene.String()

    def mutate(self, info, **input):
        data = util.input_to_dictionary(input)

        record = SimpleRecordModel(**data)
        db.session.add(record)
        db.session.commit()

        return CreateRecord(record=record)


class Mutation(graphene.ObjectType):
    createRecord = CreateRecord.Field()


schema = graphene.Schema(query=Query, mutation=Mutation, types=[SimpleRecordType])

