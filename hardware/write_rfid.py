from mfrc522 import MFRC522
import RPi.GPIO as GPIO
import time

reader = MFRC522()

KEY = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
BLOCK = 4

value = input("Valeur à enregistrer : ")

data = [0] * 16
encoded = value.encode("utf-8")[:16]

for i, byte in enumerate(encoded):
    data[i] = byte

try:
    print("Approche le badge...")

    start_time = time.time()

    while time.time() - start_time < 10:
        status, tag_type = reader.MFRC522_Request(reader.PICC_REQIDL)

        if status == reader.MI_OK:
            status, uid = reader.MFRC522_Anticoll()

            if status == reader.MI_OK:
                print("Badge détecté !")
                print("UID :", uid)

                status = reader.MFRC522_SelectTag(uid)

                if status != reader.MI_OK:
                    print("Impossible de sélectionner le badge")
                    break

                status = reader.MFRC522_Auth(
                    reader.PICC_AUTHENT1A,
                    BLOCK,
                    KEY,
                    uid
                )

                if status != reader.MI_OK:
                    print("Échec de l'authentification")
                    break

                status = reader.MFRC522_Write(BLOCK, data)

                if status == reader.MI_OK:
                    print("Valeur enregistrée :", value)
                else:
                    print("Erreur pendant l'écriture")

                reader.MFRC522_StopCrypto1()
                break

        time.sleep(0.1)

    else:
        print("Aucun badge détecté après 10 secondes.")

finally:
    GPIO.cleanup()