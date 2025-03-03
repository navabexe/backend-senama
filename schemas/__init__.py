from ariadne import gql
from .graphql_types import vendor_type_defs, user_type_defs, product_type_defs

type_defs = gql(
    vendor_type_defs +
    user_type_defs +
    product_type_defs +
    """
    type Category {
        id: ID!
        name: String!
        description: String
        created_by: ID!
        created_at: String!
        updated_by: ID
        updated_at: String
    }

    type Session {
        id: ID!
        user_id: ID!
        token: String!
        expires_at: String!
        created_at: String!
    }

    type Query {
        myVendorProfile: Vendor
        vendorProfile(vendorId: ID!): Vendor
        products(vendorId: ID!): [Product!]
        searchVendors(username: String, name: String, city: String, province: String, businessCategoryId: ID, limit: Int = 10, offset: Int = 0): [Vendor!]
        userProfile: User!
    }

    type Mutation {
        createUser(phone: String!, firstName: String, lastName: String, password: String, roles: [String!], bio: String, avatarUrls: [String!], phones: [String!], birthdate: String, gender: String, languages: [String!]): UserCreationPayload!
        requestOtp(phone: String!): UserCreationPayload!
        verifyOtp(phone: String!, otp: String!): AuthPayload!
        refreshToken(refreshToken: String!): RefreshPayload!
        logoutUser: LogoutPayload!
        createVendor(username: String!, name: String!, ownerName: String!, ownerPhone: String!, address: String!, location: LocationInput!, city: String!, province: String!, businessCategoryIds: [ID!]!): Vendor!
        updateVendor(vendorId: ID!, name: String, logoUrls: [String!], bannerUrls: [String!], bios: [String!], aboutUs: [String!], branches: [BranchInput!], businessDetails: [BusinessDetailInput!], visibility: Boolean, attachedVendors: [ID!], blockedVendors: [ID!], accountTypes: [String!], socialLinks: [SocialLinkInput!], messengerLinks: [MessengerLinkInput!]): Vendor!
        deleteVendor(vendorId: ID!): Vendor
        activateVendor(vendorId: ID!, vendorType: String): ActivationPayload!
        createProduct(vendorId: ID!, name: String!, categoryIds: [ID!]!): Product!
        updateProduct(productId: ID!, name: String, categoryIds: [ID!]): Product!
        deleteProduct(productId: ID!): Product
        createCategory(name: String!, description: String): Category!
        updateCategory(categoryId: ID!, name: String, description: String): Category!
        deleteCategory(categoryId: ID!): Category
    }

    type UserCreationPayload {
        id: ID!
        otp: String!
    }

    type AuthPayload {
        access_token: String!
        refresh_token: String!
        token_type: String!
        user_id: ID!
    }

    type RefreshPayload {
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
    """
)