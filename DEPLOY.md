# Deploying SuitUp on SleepyCore (Ubuntu + Docker + Dockge)

SuitUp is a single self-contained container that serves the app on **port 8092**.
It has no database, no secrets, and makes no network calls at runtime.

## Option A — Dockge (recommended)

Dockge manages compose stacks from a directory (default `/opt/stacks`).

```bash
# 1. Go to your Dockge stacks directory (adjust if yours differs)
cd /opt/stacks

# 2. Clone SuitUp as a stack folder
git clone https://github.com/Sleepyreaper/SuitUp.git suitup
cd suitup

# 3. Build + start it
docker compose up -d --build
```

Then open **Dockge** in your browser — the `suitup` stack appears and you can
Start/Stop/view logs from the UI. The app is live at:

```
http://<your-server-ip>:8092
```

To update later:

```bash
cd /opt/stacks/suitup
git pull
docker compose up -d --build
```

## Option B — plain docker compose (no Dockge)

```bash
git clone https://github.com/Sleepyreaper/SuitUp.git
cd SuitUp
docker compose up -d --build
# open http://<your-server-ip>:8092
```

## Useful commands

```bash
docker compose ps                 # status
docker compose logs -f suitup     # follow logs
docker compose down               # stop + remove
docker compose up -d --build      # rebuild after changes
curl http://localhost:8092/healthz   # -> {"status":"ok"}
```

## Notes

- **Port:** the app listens on 8092 inside the container and is published to
  8092 on the host (`compose.yaml` → `ports: 8092:8092`). To use a different host
  port, change the left number, e.g. `"9000:8092"`, then browse `:9000`.
- **Firewall:** if you reach the box from another machine, allow the port:
  `sudo ufw allow 8092/tcp`.
- **Health:** the container has a healthcheck hitting `/healthz`; `docker compose ps`
  shows `healthy` once it's up.
