from fastapi import FastAPI
from ariadne import make_executable_schema
from ariadne.asgi import GraphQL
from schemas import type_defs
from resolvers.queries import query
from resolvers.mutations import mutation

app = FastAPI()

schema = make_executable_schema(type_defs, query, mutation)
graphql_app = GraphQL(schema, debug=True)
app.mount("/graphql", graphql_app)

@app.get("/")
def read_root():
    return {"message": "Welcome to Senama API"}