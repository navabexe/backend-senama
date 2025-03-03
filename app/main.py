from fastapi import FastAPI, Request, HTTPException
from ariadne import make_executable_schema
from ariadne.asgi import GraphQL
import os

from starlette.responses import Response

from app.middleware.rate_limit import limiter, setup_rate_limit
from resolvers.mutations import mutation
from resolvers.queries import query
from schemas import type_defs

app = FastAPI(title="GraphQL API", description="A FastAPI app with GraphQL integration")
setup_rate_limit(app)

DEBUG_MODE = os.getenv("DEBUG", "False").lower() == "true"
schema = make_executable_schema(type_defs, query, mutation)
graphql_app = GraphQL(schema, debug=DEBUG_MODE)


@app.post("/graphql", response_model=None)
@limiter.limit("10/minute")
async def graphql_endpoint(request: Request) -> Response:
    """Handle GraphQL requests with rate limiting."""
    try:
        body = await request.json()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    query_q = body.get("query", "")
    if "verifyOtp" in query_q:
        limiter.limit("5/minute")(graphql_endpoint)

    response = await graphql_app.handle_request(request)
    return response