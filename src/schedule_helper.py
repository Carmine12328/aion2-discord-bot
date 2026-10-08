import json
from datetime import datetime, timedelta
import pytz

DAY_NAMES = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

def load_events(config_path="config/events_eu.json"):
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_next_occurrence(event, now_tz):
    """
    Calcola la prossima data/ora di spawn per un determinato evento
    rispetto al fuso orario di riferimento.
    """
    days_allowed = [d.lower() for d in event.get("days", DAY_NAMES)]
    hours = sorted(event.get("hours", []))
    minute = event.get("minute", 0)

    # Cerca nei prossimi 8 giorni
    for day_offset in range(8):
        check_date = (now_tz + timedelta(days=day_offset)).date()
        weekday_name = DAY_NAMES[check_date.weekday()]
        if weekday_name not in days_allowed:
            continue

        for hour in hours:
            candidate_dt = now_tz.tzinfo.localize(
                datetime(check_date.year, check_date.month, check_date.day, hour, minute, 0)
            )
            if candidate_dt > now_tz:
                return candidate_dt

    return None

def find_events_due_for_notification(events, now_tz, advance_minutes=10, tolerance_seconds=59):
    """
    Restituisce tutti gli eventi il cui spawn avverrà tra (advance_minutes) minuti (es. tra 9 e 10 min o esattamente a T-10 min).
    """
    due_events = []
    target_lead = timedelta(minutes=advance_minutes)
    
    for event in events:
        next_dt = get_next_occurrence(event, now_tz)
        if not next_dt:
            continue
        
        time_until = next_dt - now_tz
        # Verifica se rientra nella finestra di notifica [advance_minutes - 1 min, advance_minutes]
        # o entro una tolleranza di 60s per un tick ogni 30s-60s
        diff_from_target = abs((time_until - target_lead).total_seconds())
        if diff_from_target <= tolerance_seconds:
            due_events.append({
                "event": event,
                "spawn_time": next_dt,
                "minutes_left": round(time_until.total_seconds() / 60)
            })
            
    return due_events
