"""
Parse response text, returning JSONRPCResponse objects.
"""
import json
from typing import List, Union

import jsonschema  # type: ignore
from pkg_resources import resource_string

from . import exceptions
from .response import JSONRPCResponse

response_schema = json.loads(resource_string(__name__, "response-schema.json").decode())


def parse(
    response_text: str, validate_against_schema: bool = True
) -> Union[JSONRPCResponse, List[JSONRPCResponse], None]:
    """
    Parses response text, returning JSONRPCResponse objects.

    Args:
        response_text: JSON-RPC response string.
        ParseResponseError: The response was not valid JSON.
        ValidationError: The response was not a valid JSON-RPC response object.
    """
    if response_text:
        # If a string, ensure it's json-decodable
        try:
            decoded = json.loads(response_text)
        except ValueError:
            raise exceptions.ParseResponseError()
        # Validate the response against the Response schema (raises
        # jsonschema.ValidationError if invalid)
        if validate_against_schema:
            jsonschema.validate(decoded, response_schema)

        # Return a Response object, or a list of Responses in the case of a batch
        # request.
        if isinstance(decoded, list):
            return [JSONRPCResponse(r) for r in decoded if "id" in r]
        # else:
        return JSONRPCResponse(decoded) if "id" in decoded else None
    # else:
    return None
