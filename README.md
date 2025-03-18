# 🚗 Fleet Charging Manager

## 🇸🇰 Slovenčina

**Fleet Charging Manager** je custom integrácia pre Home Assistant určená na správu virtuálneho vozového parku, identifikáciu vozidiel a používateľov na nabíjacích stojanoch, reporting nabíjacích relácií a okamžité notifikácie o aktivite.

### ✅ Funkcie:
- Automatické vytvorenie a správa SQLite databázy priamo v Home Assistant (bez externých nástrojov)
- Pridávanie vozidiel a používateľov priamo cez Home Assistant služby
- Identifikácia vozidiel a používateľov prostredníctvom služby
- Automatické logovanie nabíjacích relácií
- Denné generovanie reportov o používaní
- Podpora automatizácií a okamžitých notifikácií na základe identifikácie

### 📂 Inštalácia:
1. V Home Assistant cez HACS:
   - Prejdi do HACS → Integrations → Custom repositories
   - Zadaj URL tohto GitHub repozitára a vyber typ „Integration“
2. Integráciu „Fleet Charging Manager“ nainštaluj a reštartuj Home Assistant.

### 🛠️ Použitie:
- Pridávanie vozidiel:
```yaml
service: fleet_charging.add_vehicle
data:
  vehicle_id: "EV123"
  name: "Škoda Enyaq"
```

- Pridávanie používateľov:
```yaml
service: fleet_charging.add_user
data:
  user_id: "user001"
  name: "Ján Novák"
```

- Identifikácia vozidla a používateľa:
```yaml
service: fleet_charging.identify_vehicle
data:
  vehicle_id: "EV123"
  user_id: "user001"
```

### 📊 Senzory dostupné v HA:
- `sensor.aktualna_relacia_nabijania` – aktuálne identifikované vozidlo a používateľ
- `sensor.denny_report_nabijania` – denný report aktivity

### 🚀 Pridávanie vozidiel a používateľov cez UI (voliteľné):
Môžete pridať vozidlá a používateľov priamo cez používateľské rozhranie Home Assistant:

- Prejdi do **Settings → Devices & Services → Fleet Charging Manager → Configure**
- Zadaj ID a mená vozidiel a používateľov
- Údaje sa automaticky uložia do integrovanej databázy

---

## 🇬🇧 English

**Fleet Charging Manager** is a custom integration for Home Assistant designed to manage a virtual vehicle fleet, identify vehicles and users at charging stations, report charging sessions, and provide immediate notifications about activity.

### ✅ Features:
- Automatic creation and management of SQLite database directly within Home Assistant (no external tools required)
- Adding vehicles and users directly through Home Assistant services
- Vehicle and user identification via a Home Assistant service
- Automatic logging of charging sessions
- Daily usage report generation
- Automation and notifications based on identification events

### 📂 Installation:
1. Using HACS in Home Assistant:
   - Navigate to HACS → Integrations → Custom repositories
   - Enter the URL of this GitHub repository and select type "Integration"
2. Install the "Fleet Charging Manager" integration and restart Home Assistant.

### 🛠️ Usage:
- Adding vehicles:
```yaml
service: fleet_charging.add_vehicle
data:
  vehicle_id: "EV123"
  name: "Tesla Model 3"
```

- Adding users:
```yaml
service: fleet_charging.add_user
data:
  user_id: "user001"
  name: "John Doe"
```

- Identifying vehicles and users:
```yaml
service: fleet_charging.identify_vehicle
data:
  vehicle_id: "EV123"
  user_id: "user001"
```

### 📊 Available sensors in HA:
- `sensor.aktualna_relacia_nabijania` – currently identified vehicle and user
- `sensor.denny_report_nabijania` – daily activity report

### 🚀 Adding vehicles and users through UI (optional):
You can add vehicles and users directly through the Home Assistant UI:

- Navigate to **Settings → Devices & Services → Fleet Charging Manager → Configure**
- Enter IDs and names for vehicles and users
- Data is automatically saved to the integrated database

---

### 🧑‍💻 Autor / Author:

- [Tvoje meno / Your name](https://github.com/tvojGithub)

📌 **Feedback a návrhy vítané! / Feedback and suggestions welcome!**



