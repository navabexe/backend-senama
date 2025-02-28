from ariadne import gql
from .owner import owner_type_defs
from .vendor import vendor_type_defs
from .product import product_type_defs
from .log import log_type_defs
from .user_interaction import user_interaction_type_defs
from .category import category_type_defs

type_defs = gql(
    owner_type_defs +
    vendor_type_defs +
    product_type_defs +
    log_type_defs +
    user_interaction_type_defs +
    category_type_defs +
    """
    type Query {
        myVendorProfile: Vendor
        vendorProfile(vendorId: ID!): Vendor
        products(vendorId: ID!): [Product!]
        searchVendors(username: String): [Vendor!]
        searchProducts(name: String): [Product!]
        logs(modelType: String!, modelId: ID!): [Log]
        interactions(userId: ID!): [UserInteraction!]
        owner(ownerId: ID!): Owner
        categories: [Category!]
        subcategories(categoryId: ID!): [Subcategory!]
    }

    type Mutation {
        createOwner(firstName: String!, lastName: String!, phone: String!): Owner!
        updateOwner(
            ownerId: ID!
            firstName: String
            lastName: String
            phone: String
            bio: String
            avatarUrls: [String!]
            phones: [String!]
            birthdate: String
            gender: String
            languages: [String!]
        ): Owner!
        deleteOwner(ownerId: ID!): Owner
        createVendor(
            username: String!
            name: String!
            ownerName: String!
            ownerPhone: String!
            address: String!
            location: LocationInput!
            city: String!
            province: String!
            categoryIds: [ID!]!
        ): Vendor!
        updateVendor(
            vendorId: ID!
            name: String
            logoUrls: [String!]
            bannerUrls: [String!]
            bios: [String!]
            aboutUs: [String!]
            branches: [BranchInput!]
            businessDetails: [BusinessDetailInput!]
            visibility: Boolean
            attachedVendors: [ID!]
            blockedVendors: [ID!]
            accountTypes: [String!]
            socialLinks: [SocialLinkInput!]
            messengerLinks: [MessengerLinkInput!]
        ): Vendor!
        deleteVendor(vendorId: ID!): Vendor
        createProduct(vendorId: ID!, name: String!, categoryIds: [ID!]!): Product!
        updateProduct(
            productId: ID!
            name: String
            shortDescriptions: [String!]
            prices: [PriceInput!]
            colors: [ColorInput!]
            images: [ImageInput!]
            videoUrls: [String!]
            audioFiles: [AudioFileInput!]
            technicalSpecs: [SpecInput!]
            tags: [String!]
            thumbnailUrls: [String!]
            suggestedProducts: [ID!]
            status: String
            qrCodeUrl: String
            categoryIds: [ID!]
            subcategoryIds: [ID!]
        ): Product!
        deleteProduct(productId: ID!): Product
        trackInteraction(targetType: String!, targetId: ID!, action: String!): UserInteraction!
        createCategory(name: String!): Category!
        createSubcategory(categoryId: ID!, name: String!): Subcategory!
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
    """
)