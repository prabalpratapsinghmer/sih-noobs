#!/usr/bin/env bash
# SIH26184 — IPFS node bootstrap (local node for dev / Pinata for prod).
# The app (api/services/ipfs.py) works mock-first: with PINATA_API_KEY=mock_key
# it produces deterministic CIDs and needs no IPFS at all. Use this script
# when running a self-hosted node instead of Pinata.
set -euo pipefail

IPFS_VERSION="${IPFS_VERSION:-v0.27.0}"

echo "==> Installing IPFS kubo ${IPFS_VERSION}"
if command -v ipfs >/dev/null 2>&1; then
  echo "ipfs already installed: $(ipfs version)"
else
  case "$(uname -s)-$(uname -m)" in
    Linux-x86_64)  URL="https://dist.ipfs.tech/kubo/${IPFS_VERSION}/kubo_${IPFS_VERSION}_linux-amd64.tar.gz" ;;
    Linux-aarch64) URL="https://dist.ipfs.tech/kubo/${IPFS_VERSION}/kubo_${IPFS_VERSION}_linux-arm64.tar.gz" ;;
    Darwin-x86_64) URL="https://dist.ipfs.tech/kubo/${IPFS_VERSION}/kubo_${IPFS_VERSION}_darwin-amd64.tar.gz" ;;
    Darwin-arm64)  URL="https://dist.ipfs.tech/kubo/${IPFS_VERSION}/kubo_${IPFS_VERSION}_darwin-arm64.tar.gz" ;;
    *) echo "Unsupported platform — download manually from https://dist.ipfs.tech"; exit 1 ;;
  esac
  curl -L "$URL" -o /tmp/kubo.tar.gz
  tar -xzf /tmp/kubo.tar.gz -C /tmp
  sudo mv /tmp/kubo/ipfs /usr/local/bin/ipfs
  rm -rf /tmp/kubo /tmp/kubo.tar.gz
fi

echo "==> Initializing node"
ipfs init --profile server 2>/dev/null || echo "already initialized"

echo "==> Allowing API/gateway from the backend container (LAN)"
ipfs config Addresses.API        --json '["/ip4/127.0.0.1/tcp/5001", "/ip4/0.0.0.0/tcp/5001"]'
ipfs config Addresses.Gateway    --json '["/ip4/127.0.0.1/tcp/8080", "/ip4/0.0.0.0/tcp/8080"]'

echo "==> Starting daemon"
ipfs daemon &

cat <<EOF

Ready. Then point the app at the node:
  # docker-compose: add an `ipfs` service and set:
  IPFS_API_URL=http://ipfs:5001   IPFS_GATEWAY_URL=http://ipfs:8080

Production alternative: keep PINATA_API_KEY / PINATA_API_SECRET real and the
app uploads straight to Pinata (api/services/ipfs.py), with local files
encrypted (AES-256-GCM) BEFORE upload.
EOF