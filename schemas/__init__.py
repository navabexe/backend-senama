from ariadne import gql

type_defs = gql("""
    type Vendor {
        id: ID!
        username: String!
        name: String!
        owner_id: ID!
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

    type Product {
        id: ID!
        vendor_id: ID!
        names: [String!]!
        short_descriptions: [String!]!
        prices: [Price!]!
        colors: [Color!]!
        images: [Image!]!
        video_urls: [String!]!
        audio_files: [AudioFile!]!
        technical_specs: [Spec!]!
        tags: [String!]!
        thumbnail_urls: [String!]!
        suggested_products: [ID!]!
        status: String!
        qr_code_url: String!
        category_ids: [ID!]!
        subcategory_ids: [ID!]!
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

    type UserInteraction {
        id: ID!
        user_id: ID!
        target_type: String!
        target_id: ID!
        action: String!
        timestamp: String!
        details: String
    }

    type Query {
        myVendorProfile: Vendor
        vendorProfile(vendorId: ID!): Vendor
        products(vendorId: ID!): [Product!]
        logs(modelType: String!, modelId: ID!): [Log] 
        interactions(userId: ID!): [UserInteraction!]
    }

    type Mutation {
        createVendor(username: String!, name: String!, ownerId: ID!): Vendor!
        createProduct(vendorId: ID!, name: String!): Product!
        trackInteraction(targetType: String!, targetId: ID!, action: String!): UserInteraction!
    }
""")