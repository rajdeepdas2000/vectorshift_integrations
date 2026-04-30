### Environment Setup:

Create a .env file in the backend directory with the following:

```
HUBSPOT_CLIENT_ID=your_client_id

HUBSPOT_CLIENT_SECRET=your_client_secret
```

Please refer to ```backend/.env.example``` for the format.

### Note 

**uvloop** and **pycurl** were removed from requirements.txt as they are not supported on Windows.