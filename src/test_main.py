import main
def test_main_alert_system():
    expected = 1
    result = main.manual_alert_system()
    assert result == expected

def test_repeat():
    expected = 1
    result = main.repeat()
    assert expected == result
