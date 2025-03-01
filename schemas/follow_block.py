from ariadne import gql

follow_block_type_defs = gql("""
    type FollowBlock {
        id: ID!
        follower_id: ID!
        following_id: ID!
        action: String!
        created_at: String!
    }
""")