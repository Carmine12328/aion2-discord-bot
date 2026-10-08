# ⚔️ Aion 2 Discord Event Notifier (EU Server)

Un servizio leggero e autonomo in Python che notifica su Discord l'inizio imminente di tutti gli eventi di Aion 2 (**Spatial Rifts, World Bosses, Abyss e Daily/Hourly events**) **10 minuti prima** dell'avvio.

---

## 🚀 Caratteristiche

- ⏱️ **Preavviso a 10 minuti**: invia notifiche ricche ed eleganti (Discord Embed) prima che l'evento o il boss compaia.
- 🐉 **World Boss con Mappe e Ritratti**:
  - Immagine della mappa incorporata nell'embed per individuare subito il punto di spawn.
  - Miniatura dell'avatar del boss.
  - Link diretto con marker su [interactivemap.app](https://interactivemap.app).
- 🕒 **Timestamp Dinamici di Discord**: mostrano il conto alla rovescia in tempo reale (`<t:TIMESTAMP:R>`) e l'ora adattata al fuso di ogni utente.
- 🌍 **Configurato per la Regione EU**: sincronizzato con gli orari ufficiali del server europeo (UTC+2).
- 🐳 **Pronto per Docker & Cloud**: eseguibile su qualsiasi VPS, piccolo server o piattaforma cloud gratuita 24/7.

---

## 🛠️ Guida Rapida alla Configurazione

### 1. Crea il Webhook su Discord (30 secondi)
1. Apri Discord ed entra nel server in cui vuoi ricevere gli avvisi.
2. Clicca con il tasto destro sul canale prescelto (o clicca l'ingranaggio **Modifica Canale**).
3. Vai nella scheda **Integrazioni** -> **Webhook** -> **Nuovo Webhook**.
4. Dai un nome al webhook (es. *Aion 2 Alerts*) e clicca **Copia URL del webhook**.

### 2. Configura il file `.env`
Apri il file `.env` all'interno della cartella del progetto e incolla l'URL:

```env
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/tuo_id/tuo_token
ADVANCE_MINUTES=10
TIMEZONE=Europe/Rome
```

---

## 🧪 Comandi di Test & Utilizzo

### Invia subito un messaggio di prova su Discord
Per verificare che il webhook funzioni e vedere come appare l'embed del Boss con la mappa:
```bash
python src/main.py --test
```

### Visualizza la lista di tutti gli eventi delle prossime 24 ore
```bash
python src/main.py --list
```

### Avvia il monitoraggio continuo sul tuo PC
```bash
python src/main.py
```

---

## ☁️ Deploy Gratuito 24/7 (Render.com + UptimeRobot)

Questa procedura ti permette di mantenere il bot attivo giorno e notte senza costi e senza tenere acceso il PC:

### Passo 1: Carica il progetto su GitHub
1. Vai su [GitHub.com](https://github.com) e crea un nuovo repository privato (es. `aion2-discord-bot`).
2. Nella cartella del progetto (`C:\Users\User\.gemini\antigravity\scratch\aion2-discord-bot`), esegui:
   ```bash
   git init
   git add .
   git commit -m "Initial commit Aion 2 Notifier"
   git branch -M main
   git remote add origin https://github.com/TUO_USERNAME/aion2-discord-bot.git
   git push -u origin main
   ```

### Passo 2: Crea il Web Service Gratuito su Render
1. Registrati gratis su [Render.com](https://render.com) (puoi accedere con GitHub).
2. Clicca su **New +** ➔ **Web Service**.
3. Seleziona il tuo repository `aion2-discord-bot`.
4. Render leggerà automaticamente il file `render.yaml` già presente. Verifica:
   - **Environment**: Python
   - **Plan**: Free (0$/mese)
5. Nella sezione **Environment Variables**, clicca **Add Environment Variable**:
   - `DISCORD_WEBHOOK_URL`: *(incolla l'URL del tuo webhook di Discord)*
6. Clicca su **Deploy Web Service**.
7. In circa 1 minuto il servizio sarà attivo e Render ti fornirà un link pubblico (es. `https://aion2-discord-bot-xyz.onrender.com`).

### Passo 3: Mantienilo Sempre Attivo con UptimeRobot (100% Free)
I servizi gratuiti di Render vanno in "sleep" se non ricevono visite per 15 minuti. Per mantenerlo sveglio 24/7:
1. Crea un account gratuito su [UptimeRobot.com](https://uptimerobot.com).
2. Clicca **Add New Monitor**:
   - **Monitor Type**: `HTTP(s)`
   - **Friendly Name**: `Aion 2 Bot KeepAlive`
   - **URL (or IP)**: Incolla l'URL fornito da Render (es. `https://aion2-discord-bot-xyz.onrender.com`)
   - **Monitoring Interval**: `5 minutes` (o 10 minutes)
3. Clicca **Create Monitor**.

🎉 **Fatto!** UptimeRobot invierà un ping leggero al micro-server web del bot ogni 5 minuti, impedendo a Render di spegnerlo e consentendo al bot di inviare le notifiche su Discord 24 ore su 24 con 10 minuti di anticipo!
