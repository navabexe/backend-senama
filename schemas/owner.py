from ariadne import gql

owner_type_defs = gql("""
    type Owner {
        id: ID!
        first_name: String!
        last_name: String!
        phone: String!
        bio: String
        avatar_urls: [String!]!
        phones: [String!]!
        birthdate: String
        gender: String
        languages: [String!]!
        created_at: String!
        updated_at: String!
    }
""")