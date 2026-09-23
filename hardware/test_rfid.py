from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO


reader = SimpleMFRC522()


def aa():
    return True


try:
    print("Approche un badge...")

    id, text = reader.read()

    print("Badge détecté !")
    print("UID :", id)

    resultat = aa()

    print("Résultat de aa() :", resultat)

finally:
    GPIO.cleanup()