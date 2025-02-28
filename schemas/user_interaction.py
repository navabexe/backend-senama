from ariadne import gql

user_interaction_type_defs = gql("""
    type UserInteraction {
        id: ID!
        user_id: ID!
        target_type: String!
        target_id: ID!
        action: String!
        timestamp: String!
        details: String
    }
""")