from ariadne import gql

vendor_type_defs = gql("""
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
        business_category_ids: [ID!]!
        logo_urls: [String!]!
        banner_urls: [String!]!
        bios: [String!]!
        about_us: [String!]!
        followers_count: Int!
        following_count: Int!
        branches: [Branch!]!
        business_details: [BusinessDetail!]!
        visibility: Boolean!
        attached_vendors: [ID!]!
        blocked_vendors: [ID!]!
        account_types: [String!]!
        social_links: [SocialLink!]!
        messenger_links: [MessengerLink!]!
        created_by: ID!
        created_at: String!
        updated_by: ID!
        updated_at: String!
    }

    type Branch {
        label: String!
        city: String!
        province: String!
        address: String!
        location: Location!
        phones: [String!]!
        emails: [String!]!
    }

    type Location {
        lat: Float!
        lng: Float!
    }

    type BusinessDetail {
        type: String!
        values: [String!]!
    }

    type SocialLink {
        platform: String!
        url: String!
    }

    type MessengerLink {
        platform: String!
        url: String!
    }
""")