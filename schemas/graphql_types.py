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

    type Location {
        lat: Float!
        lng: Float!
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

    input LocationInput {
        lat: Float!
        lng: Float!
    }

    input BranchInput {
        label: String!
        city: String!
        province: String!
        address: String!
        location: LocationInput!
        phones: [String!]!
        emails: [String!]!
    }

    input BusinessDetailInput {
        type: String!
        values: [String!]!
    }

    input SocialLinkInput {
        platform: String!
        url: String!
    }

    input MessengerLinkInput {
        platform: String!
        url: String!
    }
""")

user_type_defs = gql("""
    type User {
        id: ID!
        first_name: String
        last_name: String
        phone: String!
        password: String
        roles: [String!]!
        status: String
        otp: String
        otp_expires_at: String
        bio: String
        avatar_urls: [String!]
        phones: [String!]
        birthdate: String
        gender: String
        languages: [String!]
        created_at: String!
        updated_at: String!
    }
""")

product_type_defs = gql("""
    type Product {
        id: ID!
        vendor_id: ID!
        names: [String!]!
        short_descriptions: [String!]
        prices: [Price!]
        colors: [Color!]
        images: [Image!]
        video_urls: [String!]
        audio_files: [AudioFile!]
        technical_specs: [Spec!]
        tags: [String!]
        thumbnail_urls: [String!]
        suggested_products: [ID!]
        status: String!
        qr_code_url: String
        category_ids: [ID!]!
        subcategory_ids: [ID!]
        created_by: ID!
        created_at: String!
        updated_by: ID!
        updated_at: String!
    }

    type Price {
        type: String!
        amount: Float!
        currency: String!
    }

    type Color {
        name: String!
        hex: String!
    }

    type Image {
        url: String!
        related_colors: [String!]!
        textures: [String!]!
    }

    type AudioFile {
        url: String!
        label: String!
    }

    type Spec {
        key: String!
        value: String!
    }

    input PriceInput {
        type: String!
        amount: Float!
        currency: String!
    }

    input ColorInput {
        name: String!
        hex: String!
    }

    input ImageInput {
        url: String!
        related_colors: [String!]!
        textures: [String!]!
    }

    input AudioFileInput {
        url: String!
        label: String!
    }

    input SpecInput {
        key: String!
        value: String!
    }
""")