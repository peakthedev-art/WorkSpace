import os
import time

import requests
import RPi.GPIO as GPIO
from gpiozero import LED
from mfrc522 import MFRC522


API_BASE_URL = os.getenv(
    "ACCESS_API_URL",
    "http://192.168.50.137:8000",
).rstrip("/")

KEY = [0xFF] * 6
BLOCK = 4
SCAN_TIMEOUT = 10
LED_DURATION = 5


def verifier_role_badge(badge_id: int) -> bool:
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

        role_id = badge["role_id"]

        response = requests.get(
            f"{API_BASE_URL}/role/{role_id}",
            timeout=5,
        )

        if response.status_code == 404:
            print("Rôle introuvable dans l'API.")
            return False

        response.raise_for_status()
        role = response.json()

        nom_role = role["name"]
        print(f"Rôle détecté : {nom_role}")

        return nom_role.casefold() == "administrateur"

    except requests.RequestException as exc:
        print(f"Erreur lors de l'appel à l'API : {exc}")
        return False
    except (KeyError, TypeError, ValueError) as exc:
        print(f"Réponse de l'API invalide : {exc}")
        return False


def lire_identifiant(reader: MFRC522) -> int | None:
    deadline = time.time() + SCAN_TIMEOUT

    while time.time() < deadline:
        status, _ = reader.Request(reader.PICC_REQIDL)

        if status == reader.MI_OK:
            status, uid = reader.Anticoll()

            if status != reader.MI_OK:
                time.sleep(0.1)
                continue

            if reader.SelectTag(uid) == 0:
                print("Impossible de sélectionner le badge.")
                return None

            status = reader.Authenticate(
                reader.PICC_AUTHENT1A,
                BLOCK,
                KEY,
                uid,
            )

            if status != reader.MI_OK:
                print("Authentification du badge échouée.")
                return None

            try:
                data = reader.ReadTag(BLOCK)
            finally:
                reader.StopCrypto1()

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

    print(f"Aucun badge détecté en {SCAN_TIMEOUT} secondes.")
    return None


def afficher_resultat(est_administrateur: bool, led1: LED, led2: LED) -> None:
    led1.off()
    led2.off()

    led = led1 if est_administrateur else led2
    led.on()
    time.sleep(LED_DURATION)
    led.off()


def main() -> None:
    led1 = LED(20)
    led2 = LED(21)
    reader = None

    try:
        led1.off()
        led2.off()

        print("Démarrage du lecteur RFID...")
        reader = MFRC522()
        print("Approchez un badge...")

        badge_id = lire_identifiant(reader)

        if badge_id is None:
            print("Aucune décision d'accès.")
            return

        print(f"Badge détecté : {badge_id}")

        est_administrateur = verifier_role_badge(badge_id)
        print(est_administrateur)
        afficher_resultat(est_administrateur, led1, led2)

    except Exception as exc:
        print(f"Erreur : {exc}")

    finally:
        led1.off()
        led2.off()

        if reader is not None:
            try:
                reader.Close()
            except Exception:
                pass

        GPIO.cleanup()
        led1.close()
        led2.close()


if __name__ == "__main__":
    main()