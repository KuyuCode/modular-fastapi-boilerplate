from . import error

endpoint_not_found = error.define_error("endpoint", "not-found", "Path {path} not found", 404)


