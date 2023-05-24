from fastapi import APIRouter, Request

router = APIRouter()


@router.get('/')
async def hello(request: Request):
    """ Says hello and returns the user_id if the user is logged in """

    response = {"message": "Hello World"}
    return response
