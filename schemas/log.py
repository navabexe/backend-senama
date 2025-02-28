from ariadne import gql

log_type_defs = gql("""
    type Log {
        id: ID!
        model_type: String!
        model_id: ID!
        action: String!
        changed_by: ID!
        changed_at: String!
        previous_data: String
        new_data: String!
    }
""")