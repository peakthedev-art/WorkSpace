from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO

reader = SimpleMFRC522()


def aa():
    return True


try:
    print("Approchez un badge...")
    badge_id, role_id, activation_date, ending_date = reader.read()

    print("Badge détecté !")
    print("badge :", badge_id)
    print("role :", role_id)
    print("Date activation :", activation_date)
    print("Date fin :", ending_date)
    print("Résultat de aa() :", aa())

finally:
    GPIO.cleanup()