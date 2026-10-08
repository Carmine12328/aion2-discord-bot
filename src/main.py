import os
import sys
import json
import time
import argparse
from datetime import datetime, timedelta
import pytz
from dotenv import load_dotenv

import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

from schedule_helper import load_events, get_next_occurrence, find_events_due_for_notification
from notifier import send_discord_notification

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "").strip()
TIMEZONE_NAME = os.getenv("TIMEZONE", "Europe/Rome").strip()
ADVANCE_MINUTES = int(os.getenv("ADVANCE_MINUTES", "10"))
DISCORD_MENTION = os.getenv("DISCORD_MENTION", "").strip()
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL_SECONDS", "30"))
PORT = int(os.getenv("PORT", "10000"))

try:
    TZ = pytz.timezone(TIMEZONE_NAME)
except Exception:
    TZ = pytz.timezone("Europe/Rome")

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"OK - Aion 2 Discord Notifier is running 24/7!\n")

    def log_message(self, format, *args):
        # Silenzia i log continui dei ping di UptimeRobot
        return

def start_http_server(port):
    try:
        server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
        print(f"🌐 Server HTTP Healthcheck attivo sulla porta {port} (per Render / UptimeRobot)")
        server.serve_forever()
    except Exception as e:
        print(f"⚠️ Impossibile avviare il server HTTP sulla porta {port}: {e}")

def run_test(events):
    """
    Invia subito un messaggio di test per verificare la grafica e la connettività su Discord.
    """
    print("🚀 Invio notifica di test a Discord...")
    now_tz = datetime.now(TZ)
    sample_boss = next((e for e in events if e.get("category") == "World Bosses"), events[0])
    
    test_info = {
        "event": sample_boss,
        "spawn_time": now_tz + timedelta(minutes=ADVANCE_MINUTES),
        "minutes_left": ADVANCE_MINUTES
    }
    
    success = send_discord_notification(DISCORD_WEBHOOK_URL, test_info, mention=DISCORD_MENTION)
    if success:
        print("✅ Test completato con successo! Controlla il canale Discord.")
    else:
        print("❌ Invio test fallito. Assicurati di aver impostato un DISCORD_WEBHOOK_URL valido nel file .env.")

def list_upcoming(events):
    """
    Mostra nel terminale tutti i prossimi eventi programmati nelle prossime 24 ore.
    """
    now_tz = datetime.now(TZ)
    print(f"\n📅 Prossimi eventi Aion 2 [Server EU / Timezone: {TIMEZONE_NAME}]")
    print(f"🕒 Orario attuale: {now_tz.strftime('%Y-%m-%d %H:%M:%S %Z')}\n")
    print(f"{'Orario di Inizio':<22} | {'Categoria':<15} | {'Evento':<25} | {'Luogo'}")
    print("-" * 85)

    upcoming = []
    for ev in events:
        next_dt = get_next_occurrence(ev, now_tz)
        if next_dt:
            upcoming.append((next_dt, ev))

    upcoming.sort(key=lambda x: x[0])
    cutoff = now_tz + timedelta(hours=24)

    for next_dt, ev in upcoming:
        if next_dt <= cutoff:
            time_str = next_dt.strftime('%d/%m %H:%M')
            time_until = str(next_dt - now_tz).split('.')[0]
            print(f"{time_str} (in {time_until}) | {ev.get('category', ''):<15} | {ev.get('name', ''):<25} | {ev.get('location', '')}")

def run_loop(events, dry_run=False):
    """
    Loop continuo principale: monitora ogni 30 secondi gli orari e invia notifiche a T-10m.
    """
    print(f"🛡️ Aion 2 Notifier in esecuzione! [Timezone: {TIMEZONE_NAME}, Preavviso: {ADVANCE_MINUTES} min]")
    if dry_run:
        print("⚠️ Modalità Dry-Run attiva: le notifiche non verranno inviate a Discord.")
    elif not DISCORD_WEBHOOK_URL:
        print("⚠️ ATTENZIONE: Nessun DISCORD_WEBHOOK_URL specificato nel file .env!")
        print("   Il bot registrerà gli eventi nella console. Configura il webhook nel file .env per inviarli a Discord.")

    # Avvia il server HTTP di healthcheck in un thread daemon
    http_thread = threading.Thread(target=start_http_server, args=(PORT,), daemon=True)
    http_thread.start()

    notified_cache = set()

    while True:
        try:
            now_tz = datetime.now(TZ)
            due = find_events_due_for_notification(events, now_tz, advance_minutes=ADVANCE_MINUTES, tolerance_seconds=25)

            for item in due:
                event_key = f"{item['event']['id']}_{item['spawn_time'].strftime('%Y%m%d%H%M')}"
                if event_key not in notified_cache:
                    print(f"[{now_tz.strftime('%H:%M:%S')}] 🔔 Trovato evento in arrivo: {item['event']['name']} alle {item['spawn_time'].strftime('%H:%M')} (mancano ~{item['minutes_left']}m)")
                    
                    if not dry_run:
                        send_discord_notification(DISCORD_WEBHOOK_URL, item, mention=DISCORD_MENTION)
                    else:
                        print(f"   [Dry Run] Notifica simulata per {item['event']['name']}")

                    notified_cache.add(event_key)

            # Pulizia cache ogni ora
            if len(notified_cache) > 200:
                notified_cache.clear()

            time.sleep(POLL_INTERVAL)
        except KeyboardInterrupt:
            print("\n🛑 Arresto del servizio su richiesta dell'utente.")
            break
        except Exception as e:
            print(f"⚠️ Errore nel loop: {e}")
            time.sleep(5)

def run_cron_mode(events, cache_path="cache/notified.json"):
    """
    Modalità per GitHub Actions / Cron Job: controlla la finestra [2, 13] minuti,
    invia le notifiche se dovute e registra lo stato nella cache per prevenire duplicati.
    """
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
    notified = {}
    if os.path.exists(cache_path):
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                notified = json.load(f)
        except Exception:
            notified = {}

    now_tz = datetime.now(TZ)
    current_ts = int(now_tz.timestamp())
    # Rimuovi eventi passati da oltre 24 ore
    notified = {k: v for k, v in notified.items() if v > current_ts - 86400}

    print(f"[{now_tz.strftime('%Y-%m-%d %H:%M:%S %Z')}] Controllo eventi per il server EU (modalità cron)...")
    found_any = False

    for event in events:
        next_dt = get_next_occurrence(event, now_tz)
        if not next_dt:
            continue
        
        time_until_sec = (next_dt - now_tz).total_seconds()
        minutes_left = round(time_until_sec / 60)
        
        # Finestra di preavviso: evento tra 2 e 18 minuti (intervallo cron ~8 min)
        if 2 * 60 <= time_until_sec <= 18 * 60:
            event_key = f"{event['id']}_{next_dt.strftime('%Y%m%d%H%M')}"
            if event_key not in notified:
                print(f"🔔 Trovato evento in arrivo: {event['name']} alle {next_dt.strftime('%H:%M')} (mancano ~{minutes_left} min)!")
                item = {
                    "event": event,
                    "spawn_time": next_dt,
                    "minutes_left": minutes_left
                }
                send_discord_notification(DISCORD_WEBHOOK_URL, item, mention=DISCORD_MENTION)
                notified[event_key] = int(next_dt.timestamp())
                found_any = True
            else:
                print(f"ℹ️ Evento {event['name']} alle {next_dt.strftime('%H:%M')} già notificato.")

    if not found_any:
        print("✅ Nessun nuovo evento nella finestra dei prossimi 10 minuti.")

    try:
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(notified, f, indent=2)
    except Exception as e:
        print(f"⚠️ Impossibile salvare la cache: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Aion 2 Discord Event Notifier")
    parser.add_argument("--test", action="store_true", help="Invia una notifica di test immediata")
    parser.add_argument("--list", action="store_true", help="Elenca i prossimi eventi nelle prossime 24 ore")
    parser.add_argument("--cron", action="store_true", help="Esegui un singolo controllo (per GitHub Actions)")
    parser.add_argument("--dry-run", action="store_true", help="Esegui in console senza inviare su Discord")
    args = parser.parse_args()

    events = load_events("config/events_eu.json")

    if args.test:
        run_test(events)
    elif args.list:
        list_upcoming(events)
    elif args.cron:
        run_cron_mode(events)
    else:
        run_loop(events, dry_run=args.dry_run)
