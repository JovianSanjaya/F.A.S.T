import scdf_tele_notification
import false_alarm
def test_scdf_tele_notification():
    fire_status = 1
    manual_status = 1
    test_input = scdf_tele_notification.scd_notification(fire_status,manual_status)
    expected_input = 'Fire Detected'
    assert test_input == expected_input

def test_false_alarm():
    test_input = false_alarm.false_alarm()
    expected_input = 'False Alarm'
    assert test_input == expected_input
