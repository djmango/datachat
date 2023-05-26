from fastapi.testclient import TestClient
from fastapi import FastAPI
import pytest

from app.routes.data_router import router as data_router
from app.models.pydantic_models import PydanticModelName
from app.db import get_db
from app.models.pydantic_models import pydantic_models

# Initialize the FastAPI app with the router
app = FastAPI()
app.include_router(data_router)

# Initialize the async test client
client = TestClient(app)

@pytest.mark.parametrize("model_name", [e for e in PydanticModelName])
def test_get_data(model_name: PydanticModelName):
    """
    Test the /{model_name} GET endpoint.
    """
    # Get db
    db = await get_db(model_name)

    # Replace the original get_db function with our mock version
    app.dependency_overrides[get_db] = lambda: session_mock

    # Call the endpoint
    response = client.get(f"/data/{model_name.value}")

    # Check the status code
    if db.query(pydantic_models[model_name]._db).count() > 0:
        assert response.status_code == 200
    else:
        assert response.status_code == 404

    # TODO: Add more specific checks depending on the data you expect to be returned

    # Reset the dependency override after the test completes
    app.dependency_overrides = {}
