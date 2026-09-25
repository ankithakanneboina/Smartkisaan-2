"""
config/exception_handler.py

Wraps DRF's default exception handler so every API error — whether it
comes from a serializer validation, a 404, a 403, or an unhandled
exception — returns the same JSON envelope:

  {"error": true, "detail": "human-readable string", "code": "error_code"}

This makes the frontend error-handling trivial: check `data.detail` and
display it. No more field-by-field inspection of validation error dicts
deep in every Axios catch block.
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        # Unhandled exception — DRF lets it propagate as a 500 in DEBUG
        # mode; in production Django's 500 handler takes over. Nothing
        # to reshape here.
        return response

    # Flatten DRF's various error shapes into one consistent envelope.
    data = response.data
    if isinstance(data, dict):
        # DRF validation errors: {"field": ["msg"]} → pick first message
        if "detail" in data:
            detail = str(data["detail"])
            code = getattr(data.get("detail"), "code", "error")
        else:
            # Flatten field errors into one readable string for the UI.
            # Individual field names are preserved in "fields" for forms
            # that want to highlight the specific input.
            messages = []
            for field, errors in data.items():
                if isinstance(errors, list):
                    messages.append(f"{field}: {errors[0]}")
                else:
                    messages.append(str(errors))
            detail = " | ".join(messages)
            code = "validation_error"
            response.data = {
                "error": True,
                "detail": detail,
                "code": code,
                "fields": data,  # kept for form field highlighting
            }
            return response
    elif isinstance(data, list):
        detail = str(data[0]) if data else "Unknown error"
        code = "error"
    else:
        detail = str(data)
        code = "error"

    response.data = {"error": True, "detail": detail, "code": code}
    return response
