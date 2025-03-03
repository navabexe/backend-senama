from ariadne import MutationType
from .user import resolve_create_user, resolve_request_otp, resolve_verify_otp, resolve_refresh_token, resolve_logout_user
from .vendor import resolve_create_vendor, resolve_update_vendor, resolve_delete_vendor, resolve_activate_vendor
from .product import resolve_create_product

mutation = MutationType()

mutation.set_field("createUser", resolve_create_user)
mutation.set_field("requestOtp", resolve_request_otp)
mutation.set_field("verifyOtp", resolve_verify_otp)
mutation.set_field("refreshToken", resolve_refresh_token)
mutation.set_field("logoutUser", resolve_logout_user)
mutation.set_field("createVendor", resolve_create_vendor)
mutation.set_field("updateVendor", resolve_update_vendor)
mutation.set_field("deleteVendor", resolve_delete_vendor)
mutation.set_field("activateVendor", resolve_activate_vendor)
mutation.set_field("createProduct", resolve_create_product)