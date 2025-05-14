from typing import Any, Text, Dict, List, Optional
from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import dateparser
import  requests


class ValidateFlightSearchForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_flight_search_form"

    def required_slots(
        self,
        slots_mapped_in_domain: List[Text],
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Optional[List[Text]]:

        passengers_type = tracker.get_slot("passengers_type")
        trip_type = tracker.get_slot("trip_type")

        slots = [
            "departure_city",
            "destination_city",
            "departure_date",
            "trip_type",
            "passengers_type"
        ]

        # إذا الرحلة ذهاب وعودة → أضف return_date
        if trip_type and "ذهاب وعودة" in trip_type:
            slots.append("return_date")

        # إذا يسافر مع العائلة → أضف children_count
        if passengers_type and "عائلة" in passengers_type:
            slots.append("children_count")

        return slots

    def validate_departure_date(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict
    ) -> Dict[Text, Any]:

        parsed = dateparser.parse(slot_value, languages=["ar"])
        if parsed:
            return {"departure_date": parsed.strftime("%Y-%m-%d")}
        else:
            dispatcher.utter_message("لم أفهم تاريخ السفر، هل يمكنك كتابته بصيغة مثل 20 مايو أو الجمعة القادمة؟")
            return {"departure_date": None}

    def validate_return_date(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict
    ) -> Dict[Text, Any]:

        parsed = dateparser.parse(slot_value, languages=["ar"])
        if parsed:
            return {"return_date": parsed.strftime("%Y-%m-%d")}
        else:
            dispatcher.utter_message("لم أفهم تاريخ العودة، هل يمكنك كتابته بصيغة مثل 25 مايو أو الأحد القادم؟")
            return {"return_date": None}


class ActionSubmitFlightSearch(Action):
    def name(self) -> Text:
        return "action_submit_flight_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        departure_city = tracker.get_slot("departure_city")
        destination_city = tracker.get_slot("destination_city")
        departure_date = tracker.get_slot("departure_date")
        return_date = tracker.get_slot("return_date")
        travel_type = tracker.get_slot("travel_type")
        children_count = tracker.get_slot("children_count")

        message = f"🔍 تم تسجيل رحلتك من {departure_city} إلى {destination_city} بتاريخ {departure_date}."

        if return_date:
            message += f"\n📅 تاريخ العودة: {return_date}."

        if travel_type:
            message += f"\n👤 نوع الرحلة: {travel_type}."
        if children_count:
            message += f"\n🧒 عدد الأطفال: {children_count}."

        dispatcher.utter_message(text=message)
        return []
    

class ActionSendWhatsApp(Action):
    def name(self) -> str:
        return "action_send_whatsapp"

    def run(self, dispatcher, tracker, domain):
        token = "EAARN1trbZBlQBO5ICWSZBOQIIIH26owLZAuKrp6zBa65Qr9BZBHGXhNgEUTJrCD0YEWMfsCAQfs2VH29U1I2bZB5GZAQVuZA8z1B9fGjZCKmNA1ZBmkE2dZAxuKsoCrZB6MvG3ylox9ecHRNzT2i633ZByZBZAerPxmZANgtbnZBZBxn0cqSrghAoVpoy4m1KHFFbZCIXmxy8VdVxrodmwu7GCVjxCoOqZC70msyN5LVZAS8POwqFeUyMDY8"
        phone_number_id = "667189289803746"
        recipient_number = "967780489090"

        headers = {
            "Authorization": f"Bearer EAARN1trbZBlQBO5ICWSZBOQIIIH26owLZAuKrp6zBa65Qr9BZBHGXhNgEUTJrCD0YEWMfsCAQfs2VH29U1I2bZB5GZAQVuZA8z1B9fGjZCKmNA1ZBmkE2dZAxuKsoCrZB6MvG3ylox9ecHRNzT2i633ZByZBZAerPxmZANgtbnZBZBxn0cqSrghAoVpoy4m1KHFFbZCIXmxy8VdVxrodmwu7GCVjxCoOqZC70msyN5LVZAS8POwqFeUyMDY8",
            "Content-Type": "application/json"
        }

        message_data = {
            "messaging_product": "whatsapp",
            "to": recipient_number,
            "type": "text",
            "text": {"body": "مرحبا! تم تأكيد حجزك."}
        }

        url = f"https://graph.facebook.com/v17.0/{667189289803746}/messages"

        response = requests.post(url, headers=headers, json=message_data)

        if response.status_code == 200:
            dispatcher.utter_message("📤 تم إرسال رسالة واتساب عبر Meta.")
        else:
            dispatcher.utter_message(f"❌ خطأ في الإرسال: {response.text}")

        return []
