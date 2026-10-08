import json
import requests
from datetime import datetime

def build_discord_embed(event_info):
    """
    Costruisce l'embed Discord ricco di dettagli, inclusi orari dinamici,
    miniatura del boss e immagine della mappa.
    """
    event = event_info["event"]
    spawn_time = event_info["spawn_time"]
    minutes_left = event_info.get("minutes_left", 10)
    unix_ts = int(spawn_time.timestamp())

    icon = event.get("icon", "⚔️")
    name = event.get("name", "Evento")
    category = event.get("category", "Evento")
    location = event.get("location", "Mondo di gioco")
    map_url = event.get("map_url", "https://gamers4.life/aion-2/database/en/events/")
    color = event.get("color", 3718648)
    desc = event.get("description", "")

    embed = {
        "title": f"{icon} In arrivo tra ~{minutes_left} minuti: {name}",
        "url": map_url,
        "description": desc,
        "color": color,
        "fields": [
            {
                "name": "⏰ Inizio",
                "value": f"<t:{unix_ts}:t> (<t:{unix_ts}:R>)",
                "inline": True
            },
            {
                "name": "📍 Posizione",
                "value": location,
                "inline": True
            },
            {
                "name": "🏷️ Categoria",
                "value": category,
                "inline": True
            }
        ],
        "footer": {
            "text": "Aion 2 Event Notifier • Server EU (UTC+2)",
            "icon_url": "https://gamers4.life/aion-2/database/aion2-logo.png"
        },
        "timestamp": datetime.utcnow().isoformat()
    }

    # Miniatura del boss (avatar)
    if event.get("thumbnail_url"):
        embed["thumbnail"] = {"url": event["thumbnail_url"]}

    # Immagine della mappa (se presente, es. per i World Boss)
    if event.get("image_url"):
        embed["image"] = {"url": event["image_url"]}

    if map_url and "interactivemap.app" in map_url:
        embed["fields"].append({
            "name": "🗺️ Mappa Interattiva",
            "value": f"[Clicca qui per aprire con marker]({map_url})",
            "inline": False
        })

    return embed

def send_discord_notification(webhook_url, event_info, mention=""):
    """
    Invia la notifica a Discord via Webhook.
    """
    if not webhook_url or "discord.com/api/webhooks" not in webhook_url:
        print(f"[Notifier - Console/DryRun] Notifica per {event_info['event']['name']} (mancano ~{event_info.get('minutes_left')} min)")
        return True

    embed = build_discord_embed(event_info)
    payload = {
        "username": "Aion 2 Alerts",
        "avatar_url": "https://gamers4.life/aion-2/database/aion2-logo.png",
        "embeds": [embed]
    }

    if mention:
        payload["content"] = mention

    try:
        response = requests.post(
            webhook_url,
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        if response.status_code in [200, 204]:
            print(f"[Notifier] Notifica inviata con successo su Discord per {event_info['event']['name']}!")
            return True
        else:
            print(f"[Notifier Errore] Status {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"[Notifier Eccezione] Errore di connessione a Discord: {e}")
        return False
