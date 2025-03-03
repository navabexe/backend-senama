from ariadne import QueryType, MutationType, make_executable_schema
from ariadne.asgi import GraphQL
from fastapi import FastAPI
from schemas import type_defs
from resolvers.mutations import mutation
from resolvers.queries import query

app = FastAPI()

schema = make_executable_schema(type_defs, query, mutation)
graphql_app = GraphQL(schema, debug=True)

app.mount("/graphql", graphql_app)