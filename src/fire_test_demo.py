import fire_alarm_system


def test_trigger_alarm():
    print("Test Case 1: Triggering alarm")
    fire_alarm_system.trigger_alarm()
    assert fire_alarm_system.is_alarm_active() == True
    print("Test Case 1 Passed\n")


def test_reset_alarm():
    print("Test Case 2: Resetting alarm")
    fire_alarm_system.trigger_alarm()  # Ensure alarm is active initially
    fire_alarm_system.reset_alarm()
    assert fire_alarm_system.is_alarm_active() == False
    print("Test Case 2 Passed\n")


def test_trigger_and_reset_alarm():
    print("Test Case 3: Triggering and Resetting alarm")
    fire_alarm_system.trigger_alarm()
    assert fire_alarm_system.is_alarm_active() == True
    fire_alarm_system.reset_alarm()
    assert fire_alarm_system.is_alarm_active() == False
    print("Test Case 3 Passed\n")


def test_initial_alarm_status():
    print("Test Case 4: Checking initial alarm status")
    assert fire_alarm_system.is_alarm_active() == False
    print("Test Case 4 Passed\n")


def fire_demo():
    print("Welcome to the Fire Alarm System Simulator!")
    print("Press 't' to run tests or any other key to start the simulation.")

    choice = input("Your choice: ")

    if choice.lower() == "t":
        print("Starting Fire Alarm System Tests...\n")
        test_trigger_alarm()
        test_reset_alarm()
        test_trigger_and_reset_alarm()
        test_initial_alarm_status()
        print("All tests passed successfully!")
    else:
        while True:
            print("\nOptions:")
            print("1. Trigger alarm")
            print("2. Reset alarm")
            print("3. Check alarm status")
            print("4. Exit")

            choice = input("Enter your choice (1/2/3/4): ")

            if choice == "1":
                fire_alarm_system.trigger_alarm()
                print("Alarm triggered!")
            elif choice == "2":
                fire_alarm_system.reset_alarm()
                print("Alarm reset.")
            elif choice == "3":
                if fire_alarm_system.is_alarm_active():
                    print("The alarm is active.")
                else:
                    print("The alarm is not active.")
            elif choice == "4":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    fire_demo()