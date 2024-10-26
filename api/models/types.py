from typing import Annotated

from pydantic import Field

# Define a custom type that is a string that is not empty
NonEmptyString = Annotated[str, Field(..., min_length=1)]
