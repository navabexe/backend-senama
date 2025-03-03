from ariadne import QueryType
from .vendor import resolve_my_vendor_profile, resolve_vendor_profile, resolve_search_vendors
from .product import resolve_products, resolve_search_products
from .log import resolve_logs
from .user_interaction import resolve_interactions
from .category import resolve_categories, resolve_subcategories
from .business_category import resolve_business_categories
from .story import resolve_stories
from .follow_block import resolve_follows, resolve_blocks

query = QueryType()

query.set_field("myVendorProfile", resolve_my_vendor_profile)
query.set_field("vendorProfile", resolve_vendor_profile)
query.set_field("searchVendors", resolve_search_vendors)
query.set_field("products", resolve_products)
query.set_field("searchProducts", resolve_search_products)
query.set_field("logs", resolve_logs)
query.set_field("interactions", resolve_interactions)
query.set_field("categories", resolve_categories)
query.set_field("subcategories", resolve_subcategories)
query.set_field("businessCategories", resolve_business_categories)
query.set_field("stories", resolve_stories)
query.set_field("follows", resolve_follows)
query.set_field("blocks", resolve_blocks)