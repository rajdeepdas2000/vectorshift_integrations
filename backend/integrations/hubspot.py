import json
import secrets
import base64
import httpx
import requests
import os

from dotenv import load_dotenv
from fastapi import Request, HTTPException
from fastapi.responses import HTMLResponse

from integrations.integration_item import IntegrationItem
from redis_client import add_key_value_redis, get_value_redis, delete_key_redis

load_dotenv()
CLIENT_ID = os.getenv("HUBSPOT_CLIENT_ID")
CLIENT_SECRET = os.getenv("HUBSPOT_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8000/integrations/hubspot/oauth2callback"

AUTH_URL = "https://app.hubspot.com/oauth/authorize"
TOKEN_URL = "https://api.hubapi.com/oauth/v1/token"


# Authorize hubspot
async def authorize_hubspot(user_id, org_id):
    state_data = {
        "state": secrets.token_urlsafe(32),
        "user_id": user_id,
        "org_id": org_id
    }

    encoded_state = base64.urlsafe_b64encode(
        json.dumps(state_data).encode()
    ).decode()

    await add_key_value_redis(
        f"hubspot_state:{org_id}:{user_id}",
        json.dumps(state_data),
        expire=600
    )

    auth_url = (
        f"{AUTH_URL}"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope=crm.objects.contacts.read crm.objects.companies.read crm.objects.deals.read"
        f"&state={encoded_state}"
    )

    return auth_url


# Callback from hubspot
async def oauth2callback_hubspot(request: Request):
    if request.query_params.get("error"):
        raise HTTPException(status_code=400, detail="OAuth error")

    code = request.query_params.get("code")
    encoded_state = request.query_params.get("state")

    state_data = json.loads(
        base64.urlsafe_b64decode(encoded_state).decode()
    )

    user_id = state_data["user_id"]
    org_id = state_data["org_id"]
    original_state = state_data["state"]

    saved_state = await get_value_redis(
        f"hubspot_state:{org_id}:{user_id}"
    )

    if not saved_state or original_state != json.loads(saved_state)["state"]:
        raise HTTPException(status_code=400, detail="Invalid state")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uri": REDIRECT_URI,
                "code": code,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

    await delete_key_redis(f"hubspot_state:{org_id}:{user_id}")

    await add_key_value_redis(
        f"hubspot_credentials:{org_id}:{user_id}",
        json.dumps(response.json()),
        expire=600
    )

    return HTMLResponse(
        content="<script>window.close();</script>"
    )


# Get credentials
async def get_hubspot_credentials(user_id, org_id):
    credentials = await get_value_redis(
        f"hubspot_credentials:{org_id}:{user_id}"
    )

    if not credentials:
        raise HTTPException(status_code=400, detail="No credentials")

    await delete_key_redis(
        f"hubspot_credentials:{org_id}:{user_id}"
    )

    return json.loads(credentials)


# Create IntegrationItem
def create_integration_item_metadata_object(obj, obj_type):
    return IntegrationItem(
        id=obj.get("id"),
        name=obj.get("properties", {}).get("firstname", "Unnamed"),
        type=obj_type,
    )


# Fetch items
async def get_items_hubspot(credentials):
    credentials = json.loads(credentials)
    access_token = credentials.get("access_token")

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(
        "https://api.hubapi.com/crm/v3/objects/contacts",
        headers=headers
    )

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to fetch data")

    data = response.json().get("results", [])

    items = [
        create_integration_item_metadata_object(obj, "contact")
        for obj in data
    ]

    print("HubSpot Items:", [item.__dict__ for item in items])
    return items