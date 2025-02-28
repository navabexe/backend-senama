from ariadne import QueryType
from .owner import resolve_owner
from .vendor import resolve_my_vendor_profile, resolve_vendor_profile, resolve_search_vendors
from .product import resolve_products, resolve_search_products
from .log import resolve_logs
from .user_interaction import resolve_interactions
from .category import resolve_categories, resolve_subcategories

query = QueryType()

query.set_field("owner", resolve_owner)
query.set_field("myVendorProfile", resolve_my_vendor_profile)
query.set_field("vendorProfile", resolve_vendor_profile)
query.set_field("searchVendors", resolve_search_vendors)
query.set_field("products", resolve_products)
query.set_field("searchProducts", resolve_search_products)
query.set_field("logs", resolve_logs)
query.set_field("interactions", resolve_interactions)
query.set_field("categories", resolve_categories)
query.set_field("subcategories", resolve_subcategories)