from mfrc522 import MFRC522
import RPi.GPIO as GPIO
import time

KEY = [0xFF] * 6
BLOCK = 4
ID_ATTENDU = "111111111111"

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
                    print(False)
                    break

                status = reader.MFRC522_Auth(
                    reader.PICC_AUTHENT1A, BLOCK, KEY, uid
                )

                if status != reader.MI_OK:
                    print(False)
                    break

                data = reader.MFRC522_Read(BLOCK)
                reader.MFRC522_StopCrypto1()

                if data is None:
                    print(False)
                else:
                    identifiant = bytes(data[:12]).decode(
                        "ascii", errors="ignore"
                    )
                    print(identifiant == ID_ATTENDU)

                break

        time.sleep(0.1)
    else:
        print(False)

finally:
    GPIO.cleanup()