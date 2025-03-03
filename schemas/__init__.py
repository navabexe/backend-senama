from ariadne import gql
from .vendor import vendor_type_defs
from .product import product_type_defs
from .log import log_type_defs
from .user_interaction import user_interaction_type_defs
from .category import category_type_defs
from .story import story_type_defs
from .business_category import business_category_type_defs
from .follow_block import follow_block_type_defs

type_defs = gql(
    vendor_type_defs +
    product_type_defs +
    log_type_defs +
    user_interaction_type_defs +
    category_type_defs +
    story_type_defs +
    business_category_type_defs +
    follow_block_type_defs +
    """
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

    type Session {
        id: ID!
        user_id: ID!
        token: String!
        expires_at: String!
        created_at: String!
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

    type Query {
        myVendorProfile: Vendor
        vendorProfile(vendorId: ID!): Vendor
        products(vendorId: ID!): [Product!]
        searchVendors(username: String, name: String, city: String, province: String, businessCategoryId: ID): [Vendor!]
        searchProducts(name: String, tag: String, categoryId: ID, status: String): [Product!]
        logs(modelType: String!, modelId: ID!): [Log]
        interactions(userId: ID!): [UserInteraction!]
        categories: [Category!]
        subcategories(categoryId: ID!): [Subcategory!]
        businessCategories: [BusinessCategory!]
        stories(vendorId: ID!): [Story!]
        follows(followerId: ID!): [FollowBlock!]
        blocks(followerId: ID!): [FollowBlock!]
    }

    type Mutation {
        createUser(phone: String!, firstName: String, lastName: String, password: String, roles: [String!], bio: String, avatarUrls: [String!], phones: [String!], birthdate: String, gender: String, languages: [String!]): UserCreationPayload!
        verifyOtp(phone: String!, otp: String!): AuthPayload!
        logoutUser: LogoutPayload!
        activateUser(userId: ID!): ActivationPayload!
        regenerateOtp(phone: String!): UserCreationPayload!
        createVendor(
            username: String!
            name: String!
            ownerName: String!
            ownerPhone: String!
            address: String!
            location: LocationInput!
            city: String!
            province: String!
            businessCategoryIds: [ID!]!
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
        activateVendor(vendorId: ID!, vendorType: String): ActivationPayload!
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
        createBusinessCategory(name: String!): BusinessCategory!
        createStory(vendorId: ID!, mediaUrl: String!): Story!
        updateStory(
            storyId: ID!
            description: String
            link: String
            tags: [String!]
        ): Story!
        deleteStory(storyId: ID!): Story
        createFollowBlock(followerId: ID!, followingId: ID!, action: String!): FollowBlock!
        deleteFollowBlock(followBlockId: ID!): FollowBlock
    }

    type UserCreationPayload {
        id: ID!
        otp: String!
    }

    type AuthPayload {
        access_token: String!
        token_type: String!
        user_id: ID!
    }

    type LogoutPayload {
        message: String!
    }

    type ActivationPayload {
        message: String!
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