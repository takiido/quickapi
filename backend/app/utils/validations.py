from fastapi import HTTPException


def validate_id(id: int, table_name: str):
    if id <= 0:
        raise HTTPException(status_code=400, detail=f"Invalid {table_name} ID")