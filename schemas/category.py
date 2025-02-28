from ariadne import gql

category_type_defs = gql("""
    type Category {
        id: ID!
        name: String!
        created_at: String!
        updated_at: String!
    }

    type Subcategory {
        id: ID!
        category_id: ID!
        name: String!
        created_at: String!
        updated_at: String!
    }
""")