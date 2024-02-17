alarm_active = False

def trigger_alarm():

    global alarm_active
    alarm_active = True
    print("Alarm triggered!")


def reset_alarm():

    global alarm_active
    alarm_active = False
    print("Alarm reset.")


def is_alarm_active():
    return alarm_active