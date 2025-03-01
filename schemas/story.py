from ariadne import gql

story_type_defs = gql("""
    type Story {
        id: ID!
        vendor_id: ID!
        media_url: String!
        description: String
        link: String
        tags: [String!]!
        created_at: String!
        updated_at: String!
    }
""")