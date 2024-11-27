from pydantic import BaseModel, Field


class Metadata(BaseModel):
    project_name: str = Field(min_length=5)
    run_name: str = Field(min_length=1)
    project_path: str = Field(min_length=1)


