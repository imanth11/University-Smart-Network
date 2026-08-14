from gpio import *
from time import *

state = ""

def get_temperature(raw):
    return ((raw / 1024.0) * 201.0) - 100.0

def normal_mode():
    digitalWrite(0, LOW)
    digitalWrite(1, HIGH)
    digitalWrite(2, LOW)
    customWrite(3, "0")
    customWrite(4, "0")
    customWrite(5, "SYSTEM NORMAL")

def emergency_mode():
    digitalWrite(0, HIGH)
    digitalWrite(1, LOW)
    digitalWrite(2, HIGH)
    customWrite(3, "2")
    customWrite(4, "1")
    customWrite(5, "EMERGENCY - FIRE")

def main():
    global state

    pinMode(A0, IN)
    pinMode(A1, IN)

    pinMode(0, OUT)
    pinMode(1, OUT)
    pinMode(2, OUT)

    normal_mode()
    state = "normal"

    print("University Disaster Recovery System")
    print("System Started")
    print("Status: NORMAL")

    while True:
        temp_raw = analogRead(A0)
        smoke_raw = analogRead(A1)

        temperature = get_temperature(temp_raw)
        smoke = smoke_raw > 0

        if temperature > 45 and smoke:
            if state != "emergency":
                emergency_mode()
                state = "emergency"

                print("--------------------------------")
                print("EMERGENCY DETECTED")
                print("Temperature: " + str(int(temperature)) + " C")
                print("Smoke Raw: " + str(smoke_raw))
                print("Alarm: ON")
                print("Red LED: ON")
                print("Green LED: OFF")
                print("Fan: ON")
                print("Door: OPEN")
                print("Display: EMERGENCY")
                print("--------------------------------")
        else:
            if state != "normal":
                normal_mode()
                state = "normal"

                print("--------------------------------")
                print("SYSTEM RECOVERED")
                print("Temperature: " + str(int(temperature)) + " C")
                print("Smoke Raw: " + str(smoke_raw))
                print("Alarm: OFF")
                print("Red LED: OFF")
                print("Green LED: ON")
                print("Fan: OFF")
                print("Door: CLOSED")
                print("Display: NORMAL")
                print("--------------------------------")

        delay(500)

if __name__ == "__main__":
    main()