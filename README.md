# ⚔️ Aion 2 Discord Event Notifier

A lightweight, fully automated Python service that sends **Discord notifications 10 minutes before every Aion 2 event** — Spatial Rifts, World Bosses, Abyss sieges, and daily/hourly events — for the **EU server**.

Runs 24/7 for free via **GitHub Actions** (no server required).

---

## 🌟 Features

- ⏱️ **10-minute early warning** — rich Discord embeds with countdown timers before each event starts.
- 🐉 **World Boss maps & portraits** — each boss notification includes a spawn-point map with marker overlay and a boss avatar thumbnail.
- 🕒 **Dynamic Discord timestamps** — `<t:TIMESTAMP:R>` format auto-adapts to each user's local timezone.
- 🌍 **EU server schedule** — synchronized with official European server times (UTC+2).
- 🤖 **Zero-maintenance** — runs every 5 minutes on GitHub Actions with anti-duplicate cache.
- 🗺️ **Interactive map links** — direct links to [interactivemap.app](https://interactivemap.app) with boss markers.

---

## 🚀 Quick Start

### 1. Create a Discord Webhook (30 seconds)
1. Open Discord and go to the channel where you want alerts.
2. Right-click the channel → **Edit Channel** → **Integrations** → **Webhooks** → **New Webhook**.
3. Name it (e.g., *Aion 2 Alerts*) and click **Copy Webhook URL**.

### 2. Deploy on GitHub Actions (free, 24/7)
1. **Fork** this repository (or clone and push to your own GitHub account).
2. Go to **Settings** → **Secrets and variables** → **Actions** → **New repository secret**.
3. Add a secret named `DISCORD_WEBHOOK_URL` with your webhook URL as the value.
4. That's it! The workflow runs automatically every 5 minutes and sends notifications when events are approaching.

### 3. Test it
You can trigger a test notification manually:
- Go to the **Actions** tab → **Aion 2 Event Notifier** → **Run workflow** → check **"Invia notifica di test"** → **Run**.

### Local usage (optional)
```bash
# Install dependencies
pip install -r requirements.txt

# Copy and configure environment
cp .env.example .env
# Edit .env and paste your DISCORD_WEBHOOK_URL

# Send a test notification
python src/main.py --test

# List upcoming events (next 24h)
python src/main.py --list

# Run continuous monitoring locally
python src/main.py
```

---

## 🗂️ Project Structure

```
├── .github/workflows/notify.yml   # GitHub Actions cron (every 5 min)
├── assets/maps/                   # World Boss spawn maps with markers
├── config/events_eu.json          # Full EU event schedule database
├── src/
│   ├── main.py                    # Entry point (--test, --list, --cron)
│   ├── notifier.py                # Discord webhook sender with embeds
│   ├── schedule_helper.py         # Time engine for next occurrences
│   └── generate_maps.py           # One-time map image generator
├── .env.example                   # Environment template
├── requirements.txt               # Python dependencies
└── README.md
```

---

## 📸 Preview

Each notification includes:
- 🎨 Color-coded embeds by category (Rifts, Bosses, Abyss, Events)
- ⏳ Live countdown via Discord timestamps
- 🗺️ Boss spawn maps uploaded directly as attachments
- 🖼️ Boss portrait thumbnails

---

## 📋 Supported Events

| Category | Events |
|---|---|
| 🔴 **Rifts** | Spacetime Rift (every 3 hours) |
| 🐉 **World Bosses** | Watcher Kaira, Executor Tamasa, Executor Argo, Executor Kaira, Guardian Lord Nahma |
| ⚔️ **Abyss** | Artifact Siege |
| 🎪 **Events** | Shugo Festival, Arena of Tactics, Dimensional Invasion, Daily Reset |

---

## ⚙️ Configuration

| Environment Variable | Default | Description |
|---|---|---|
| `DISCORD_WEBHOOK_URL` | *(required)* | Your Discord webhook URL |
| `ADVANCE_MINUTES` | `10` | Minutes before event to send notification |
| `TIMEZONE` | `Europe/Rome` | Server timezone |
| `DISCORD_MENTION` | *(empty)* | Optional role/user mention (e.g., `@everyone`) |

---

## 📜 License

MIT — feel free to fork and customize for your guild!

---
---

# 🇮🇹 Versione Italiana

## ⚔️ Aion 2 Discord Event Notifier (Server EU)

Un servizio leggero e autonomo in Python che notifica su Discord l'inizio imminente di tutti gli eventi di Aion 2 (**Spatial Rifts, World Bosses, Abyss e Daily/Hourly events**) **10 minuti prima** dell'avvio.

Gira 24/7 gratuitamente tramite **GitHub Actions** (nessun server richiesto).

---

### 🚀 Caratteristiche

- ⏱️ **Preavviso a 10 minuti**: invia notifiche ricche ed eleganti (Discord Embed) prima che l'evento o il boss compaia.
- 🐉 **World Boss con Mappe e Ritratti**:
  - Immagine della mappa incorporata nell'embed per individuare subito il punto di spawn.
  - Miniatura dell'avatar del boss.
  - Link diretto con marker su [interactivemap.app](https://interactivemap.app).
- 🕒 **Timestamp Dinamici di Discord**: mostrano il conto alla rovescia in tempo reale (`<t:TIMESTAMP:R>`) e l'ora adattata al fuso di ogni utente.
- 🌍 **Configurato per la Regione EU**: sincronizzato con gli orari ufficiali del server europeo (UTC+2).
- 🤖 **Zero manutenzione**: gira ogni 5 minuti su GitHub Actions con cache anti-duplicato.

---

### 🛠️ Guida Rapida

#### 1. Crea il Webhook su Discord (30 secondi)
1. Apri Discord ed entra nel server in cui vuoi ricevere gli avvisi.
2. Clicca con il tasto destro sul canale prescelto → **Modifica Canale**.
3. Vai nella scheda **Integrazioni** → **Webhook** → **Nuovo Webhook**.
4. Dai un nome al webhook (es. *Aion 2 Alerts*) e clicca **Copia URL del webhook**.

#### 2. Deploy su GitHub Actions (gratuito, 24/7)
1. **Fai un fork** di questo repository (o clona e pusha sul tuo account GitHub).
2. Vai su **Settings** → **Secrets and variables** → **Actions** → **New repository secret**.
3. Aggiungi un secret chiamato `DISCORD_WEBHOOK_URL` con l'URL del tuo webhook.
4. Fatto! Il workflow gira automaticamente ogni 5 minuti e invia notifiche quando un evento sta per iniziare.

#### 3. Testa il bot
Puoi inviare una notifica di test manualmente:
- Vai nella tab **Actions** → **Aion 2 Event Notifier** → **Run workflow** → spunta **"Invia notifica di test"** → **Run**.

#### Uso locale (opzionale)
```bash
# Installa le dipendenze
pip install -r requirements.txt

# Copia e configura l'environment
cp .env.example .env
# Modifica .env e incolla il tuo DISCORD_WEBHOOK_URL

# Invia una notifica di test
python src/main.py --test

# Elenca i prossimi eventi (24 ore)
python src/main.py --list

# Avvia il monitoraggio continuo
python src/main.py
```

---

### 📋 Eventi Supportati

| Categoria | Eventi |
|---|---|
| 🔴 **Rifts** | Spacetime Rift (ogni 3 ore) |
| 🐉 **World Bosses** | Watcher Kaira, Executor Tamasa, Executor Argo, Executor Kaira, Guardian Lord Nahma |
| ⚔️ **Abyss** | Artifact Siege |
| 🎪 **Events** | Shugo Festival, Arena of Tactics, Dimensional Invasion, Daily Reset |
