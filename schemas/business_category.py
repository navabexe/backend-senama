from ariadne import gql

business_category_type_defs = gql("""
    type BusinessCategory {
        id: ID!
        name: String!
        created_at: String!
        updated_at: String!
    }
""")