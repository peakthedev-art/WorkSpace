from mfrc522 import MFRC522
import RPi.GPIO as GPIO
import time

from app import access_service
from app.database import SessionLocal

KEY = [0xFF] * 6
BLOCK = 4


def verifier_role_badge(badge_id: int) -> tuple[bool, str | None]:
    """Renvoie (True/False selon le rôle, nom du rôle ou None)."""
    db = SessionLocal()

    try:
        badge = access_service.finad_badge(db, badge_id)

        if badge is None:
            return False, None

        role = access_service.find_role(db, badge.role_id)

        if role is None:
            return False, None

        role_name = role.name
        return role_name == "administrateur", role_name
    finally:
        db.close()


reader = MFRC522()

try:
    print("Approche un badge...")
    deadline = time.time() + 10

    while time.time() < deadline:
        status, _ = reader.MFRC522_Request(reader.PICC_REQIDL)

        if status == reader.MI_OK:
            status, uid = reader.MFRC522_Anticoll()

            if status == reader.MI_OK:
                if reader.MFRC522_SelectTag(uid) == 0:
                    print((False, None))
                    break

                status = reader.MFRC522_Auth(
                    reader.PICC_AUTHENT1A,
                    BLOCK,
                    KEY,
                    uid
                )

                if status != reader.MI_OK:
                    print((False, None))
                    break

                data = reader.MFRC522_Read(BLOCK)
                reader.MFRC522_StopCrypto1()

                if data is None:
                    print((False, None))
                    break

                identifiant = bytes(data[:12]).decode(
                    "ascii", errors="ignore"
                ).strip("\x00")

                if not identifiant.isdigit():
                    print((False, None))
                    break

                resultat = verifier_role_badge(int(identifiant))
                print(resultat)
                break

        time.sleep(0.1)
    else:
        print((False, None))

finally:
    GPIO.cleanup()