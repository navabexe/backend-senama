from ariadne import gql

product_type_defs = gql("""
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
""")