from fastapi import APIRouter, Request
from pathlib import Path
import json

HERE = Path(__file__).parent

router = APIRouter()


@router.get('/ai-plugin.json')
async def aiplugin(request: Request):
    """ Returns ai-plugin.json, a file at the root level """

    response = json.loads((HERE.parent.parent / 'ai-plugin.json').read_text())
    return response
