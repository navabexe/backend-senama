vendor_type_defs = """
    type Vendor {
        id: ID!
        username: String!
        name: String!
        owner_name: String!
        owner_phone: String!
        address: String!
        location: Location!
        city: String!
        province: String!
        logo_urls: [String!]
        banner_urls: [String!]
        bios: [String!]
        about_us: [String!]
        branches: [Branch!]
        business_details: [BusinessDetail!]
        visibility: Boolean!
        attached_vendors: [ID!]
        blocked_vendors: [ID!]
        account_types: [String!]
        status: String!
        vendor_type: String!
        social_links: [SocialLink!]
        messenger_links: [MessengerLink!]
        followers_count: Int!
        following_count: Int!
        business_category_ids: [ID!]!
        created_by: ID!
        created_at: String!
        updated_by: ID
        updated_at: String
    }
"""