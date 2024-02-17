import resident_alerts
from resident_alerts import temp_list
def test_fire_detection():
    array = []
    result = resident_alerts.fire_detection()
    array.append(result)
    expected = temp_list
    assert array == expected

def test_fire_alarm():
    expected = 1
    result = resident_alerts.fire_alarm()
    assert result == expected

def test_rotate_servo():
    expected = 1
    result = resident_alerts.rotate_servo()
    assert result == expected


