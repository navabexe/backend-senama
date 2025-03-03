from ariadne import MutationType
from .user import resolve_create_user, resolve_verify_otp, resolve_logout_user, resolve_regenerate_otp
from .vendor import resolve_create_vendor, resolve_update_vendor, resolve_delete_vendor, resolve_activate_vendor
from .product import resolve_create_product, resolve_update_product, resolve_delete_product
from .user_interaction import resolve_track_interaction
from .category import resolve_create_category, resolve_create_subcategory
from .business_category import resolve_create_business_category
from .story import resolve_create_story, resolve_update_story, resolve_delete_story
from .follow_block import resolve_create_follow_block, resolve_delete_follow_block

mutation = MutationType()

mutation.set_field("createUser", resolve_create_user)
mutation.set_field("verifyOtp", resolve_verify_otp)
mutation.set_field("logoutUser", resolve_logout_user)
mutation.set_field("createVendor", resolve_create_vendor)
mutation.set_field("updateVendor", resolve_update_vendor)
mutation.set_field("deleteVendor", resolve_delete_vendor)
mutation.set_field("activateVendor", resolve_activate_vendor)
mutation.set_field("createProduct", resolve_create_product)
mutation.set_field("updateProduct", resolve_update_product)
mutation.set_field("deleteProduct", resolve_delete_product)
mutation.set_field("trackInteraction", resolve_track_interaction)
mutation.set_field("createCategory", resolve_create_category)
mutation.set_field("createSubcategory", resolve_create_subcategory)
mutation.set_field("createBusinessCategory", resolve_create_business_category)
mutation.set_field("createStory", resolve_create_story)
mutation.set_field("updateStory", resolve_update_story)
mutation.set_field("deleteStory", resolve_delete_story)
mutation.set_field("createFollowBlock", resolve_create_follow_block)
mutation.set_field("deleteFollowBlock", resolve_delete_follow_block)
mutation.set_field("regenerateOtp", resolve_regenerate_otp)