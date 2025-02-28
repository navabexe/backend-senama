from ariadne import MutationType
from .owner import resolve_create_owner, resolve_update_owner, resolve_delete_owner
from .vendor import resolve_create_vendor, resolve_update_vendor, resolve_delete_vendor
from .product import resolve_create_product, resolve_update_product, resolve_delete_product
from .user_interaction import resolve_track_interaction
from .category import resolve_create_category, resolve_create_subcategory

mutation = MutationType()

mutation.set_field("createOwner", resolve_create_owner)
mutation.set_field("updateOwner", resolve_update_owner)
mutation.set_field("deleteOwner", resolve_delete_owner)
mutation.set_field("createVendor", resolve_create_vendor)
mutation.set_field("updateVendor", resolve_update_vendor)
mutation.set_field("deleteVendor", resolve_delete_vendor)
mutation.set_field("createProduct", resolve_create_product)
mutation.set_field("updateProduct", resolve_update_product)
mutation.set_field("deleteProduct", resolve_delete_product)
mutation.set_field("trackInteraction", resolve_track_interaction)
mutation.set_field("createCategory", resolve_create_category)
mutation.set_field("createSubcategory", resolve_create_subcategory)