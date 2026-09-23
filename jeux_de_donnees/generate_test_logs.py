"""Injecte des decisions d'acces synthetiques dans Loki pour les tests."""

import json
import os
import random
import urllib.request
from datetime import datetime, timedelta, timezone


LOKI_URL = os.getenv("LOKI_URL", "http://localhost:3100")
LOG_COUNT = 20
DENIED_COUNT = 15


def main() -> None:
    random_generator = random.Random(20260923)
    now = datetime.now(timezone.utc)
    event_times = sorted(
        now - timedelta(minutes=random_generator.randint(0, 24 * 60))
        for _ in range(LOG_COUNT)
    )

    entries = []
    zones = ["Accueil", "Open Space", "Salle serveur", "Parking"]
    for index, event_time in enumerate(event_times):
        authorized = index >= DENIED_COUNT
        payload = {
            "timestamp": event_time.isoformat(),
            "level": "INFO",
            "logger": "app.access",
            "message": "Access decision recorded",
            "event": "access_decision",
            "details": {
                "badge_id": f"test-badge-{index + 1:02d}",
                "zone": zones[index % len(zones)],
                "time": event_time.strftime("%H:%M:%S"),
                "authorized": authorized,
                "synthetic": True,
            },
        }
        entries.append(
            [str(int(event_time.timestamp() * 1_000_000_000)), json.dumps(payload)]
        )

    request = urllib.request.Request(
        f"{LOKI_URL}/loki/api/v1/push",
        data=json.dumps(
            {
                "streams": [
                    {
                        "stream": {
                            "service": "api_python",
                            "container": "workspace-api",
                            "event": "access_decision",
                            "level": "info",
                            "source": "synthetic",
                        },
                        "values": entries,
                    }
                ]
            }
        ).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(request) as response:
        if response.status != 204:
            raise RuntimeError(f"Loki a repondu avec le statut {response.status}")

    print(f"{LOG_COUNT} logs envoyes a {LOKI_URL}")
    print(f"Acces autorises : {LOG_COUNT - DENIED_COUNT}")
    print(f"Acces refuses : {DENIED_COUNT}")


if __name__ == "__main__":
    main()