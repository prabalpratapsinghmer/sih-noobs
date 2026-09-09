# Vercel frontend deployment

Vercel hosts the React application only. Deploy the FastAPI gateway and the ATM
model service to a public HTTPS runtime separately; neither can use `localhost`
after deployment.

## Required Vercel environment variable

Set the following in **Project Settings → Environment Variables** for
Production, Preview, and Development, then redeploy:

```text
VITE_API_BASE_URL=https://api.example.com
```

Use the FastAPI service origin only. The frontend appends `/api/v1` itself.
Do not set this to a trailing-slash URL or to `localhost`.

## Required backend environment variables

```text
CORS_ORIGINS=["https://your-project.vercel.app"]
MODEL_API_URL=https://your-atm-model.example.com
```

`MODEL_API_URL` must implement `POST /internal/model/atm_predict` and return a
non-empty JSON list containing `probability` and `time_window` for each ATM.
When it cannot be reached, the backend marks the result as `local_fallback`;
it must not be presented as a live model result.

## Verification

1. Open the deployed Vercel site and file a new report.
2. In browser Network tools, confirm a `201` response from
   `https://api.example.com/api/v1/victim/complaint`.
3. Confirm the response includes `intelligence.atms` and
   `intelligence.model_run.mode` is `live`.
4. Open the Command page; the ATM targets on the map must match
   `intelligence.atms` from that response.

If `VITE_API_BASE_URL` is missing or the backend response lacks ATM
intelligence, the form now reports an error and remains on the submission step.
