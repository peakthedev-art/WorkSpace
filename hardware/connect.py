import os
import time
from datetime import date

import requests
import RPi.GPIO as GPIO
from mfrc522 import MFRC522


API_BASE_URL = os.getenv("ACCESS_API_URL", "http://127.0.0.1:8000").rstrip("/")
KEY = [0xFF] * 6
BLOCK = 4
SCAN_TIMEOUT = 10


def verifier_role_badge(badge_id: int) -> bool:
    """Vérifie le badge et son rôle via les routes de l'API."""
    try:
        response = requests.get(
            f"{API_BASE_URL}/badge/{badge_id}",
            timeout=5,
        )
        if response.status_code == 404:
            print("Badge introuvable dans l'API.")
            return False
        response.raise_for_status()
        badge = response.json()

        aujourd_hui = date.today()
        activation = date.fromisoformat(badge["activation_date"])
        fin = date.fromisoformat(badge["ending_date"])

        if not activation <= aujourd_hui <= fin:
            print("Badge hors période de validité.")
            return False

        response = requests.get(
            f"{API_BASE_URL}/role/{badge['role_id']}",
            timeout=5,
        )
        if response.status_code == 404:
            print("Rôle introuvable dans l'API.")
            return False
        response.raise_for_status()
        role = response.json()

        return role["name"].casefold() == "administrateur"

    except requests.RequestException as exc:
        print(f"Erreur lors de l'appel à l'API ({API_BASE_URL}) : {exc}")
        return False
    except (KeyError, TypeError, ValueError) as exc:
        print(f"Réponse de l'API invalide : {exc}")
        return False


def lire_identifiant(reader: MFRC522) -> int | None:
    """Lit l'identifiant numérique de 12 chiffres stocké dans le bloc 4."""
    deadline = time.time() + SCAN_TIMEOUT

    while time.time() < deadline:
        status, _ = reader.MFRC522_Request(reader.PICC_REQIDL)

        if status == reader.MI_OK:
            status, uid = reader.MFRC522_Anticoll()

            if status == reader.MI_OK:
                if reader.MFRC522_SelectTag(uid) == 0:
                    print("Impossible de sélectionner le badge.")
                    return None

                status = reader.MFRC522_Auth(
                    reader.PICC_AUTHENT1A,
                    BLOCK,
                    KEY,
                    uid,
                )

                if status != reader.MI_OK:
                    print("Authentification du badge échouée.")
                    return None

                try:
                    data = reader.MFRC522_Read(BLOCK)
                finally:
                    reader.MFRC522_StopCrypto1()

                if data is None:
                    print("Lecture du bloc du badge échouée.")
                    return None

                identifiant = bytes(data[:12]).decode(
                    "ascii",
                    errors="ignore",
                ).strip("\x00 ").strip()

                if len(identifiant) != 12 or not identifiant.isdigit():
                    print(f"Identifiant invalide dans le badge : {identifiant!r}")
                    return None

                return int(identifiant)

        time.sleep(0.1)

    print("Aucun badge détecté en 10 secondes.")
    return None


def main() -> None:
    print("Démarrage du lecteur RFID...")
    reader = None

    try:
        reader = MFRC522()
        print("Approchez un badge...")

        badge_id = lire_identifiant(reader)
        if badge_id is None:
            print(False)
            return

        print(f"Badge détecté : {badge_id}")
        print(verifier_role_badge(badge_id))

    except Exception as exc:
        print(f"Erreur du lecteur RFID/SPI : {exc}")
        print(False)

    finally:
        if reader is not None:
            try:
                reader.Close_MFRC522()
            except Exception:
                GPIO.cleanup()
        else:
            GPIO.cleanup()


if __name__ == "__main__":
    main()