from fastapi import HTTPException, status

UsernameNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Username does not exist"
)

UsernameAlreadyTakenException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Username already taken"
)
