from ariadne import QueryType
from .product import resolve_products
from .user import resolve_user_profile
from .vendor import resolve_my_vendor_profile, resolve_vendor_profile, resolve_search_vendors

query = QueryType()

query.set_field("myVendorProfile", resolve_my_vendor_profile)
query.set_field("vendorProfile", resolve_vendor_profile)
query.set_field("products", resolve_products)
query.set_field("searchVendors", resolve_search_vendors)
query.set_field("userProfile", resolve_user_profile)