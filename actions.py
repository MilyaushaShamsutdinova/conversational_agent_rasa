from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


bookings = {}


class ActionBookRoom(Action):

    def name(self) -> Text:
        return "action_book_room"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        date = tracker.get_slot('date')
        time = tracker.get_slot('time')

        booking_id = f"{date}_{time}"
        bookings[booking_id] = {
            "date": date,
            "time": time
        }

        dispatcher.utter_message(text=f"Your booking is confirmed for {date} at {time}.")
        return []


class ActionCancelBooking(Action):

    def name(self) -> Text:
        return "action_cancel_booking"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        date = tracker.get_slot('date')
        time = tracker.get_slot('time')

        booking_id = f"{date}_{time}"
        if booking_id in bookings:
            del bookings[booking_id]
            dispatcher.utter_message(text="Your booking has been canceled.")
        else:
            dispatcher.utter_message(text="No booking found to cancel.")
        return []


class ActionCheckAvailability(Action):

    def name(self) -> Text:
        return "action_check_availability"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        date = tracker.get_slot('date')
        time = tracker.get_slot('time')

        booking_id = f"{date}_{time}"
        if booking_id in bookings:
            dispatcher.utter_message(text=f"The room is not available on {date} at {time}.")
        else:
            dispatcher.utter_message(text=f"The room is available on {date} at {time}.")
        return []
