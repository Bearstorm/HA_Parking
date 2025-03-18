# 🚗 Fleet Charging Manager v.1.0.0

## 🇸🇰 Slovenčina

**Fleet Charging Manager** je custom integrácia pre Home Assistant určená na správu virtuálneho vozového parku, identifikáciu vozidiel a používateľov na nabíjacích stojanoch, reporting nabíjacích relácií a okamžité notifikácie o aktivite.

### ✅ Funkcie:
- Databáza vozidiel a používateľov priamo v Home Assistant (SQLite)
- Identifikácia vozidiel a používateľov pomocou jednoduchej služby
- Automatické logovanie nabíjacích relácií
- Generovanie denných reportov o používaní
- Automatizácie a notifikácie podľa identifikácie

### 📂 Inštalácia:
1. V Home Assistant cez HACS:
   - Prejdi do HACS → Integrations → Custom repositories
   - Zadaj URL tohto GitHub repozitára a vyber typ „Integration“
2. Integráciu „Fleet Charging Manager“ nainštaluj a reštartuj Home Assistant.

### 🛠️ Použitie:
- Pridaj vozidlá a používateľov priamo do SQLite databázy integrácie (napr. pomocou SQLite editora).
- Zavolaj službu `fleet_charging.identify_vehicle` s parametrami:
```yaml
service: fleet_charging.identify_vehicle
data:
  vehicle_id: "EV123"
  user_id: "user001"
```

### 📊 Senzory dostupné v HA:
- `sensor.aktualna_relacia_nabijania` – aktuálne identifikované vozidlo a používateľ
- `sensor.denny_report_nabijania` – denný report aktivity

---

## 🇬🇧 English

**Fleet Charging Manager** is a custom integration for Home Assistant designed to manage a virtual vehicle fleet, identify vehicles and users at charging stations, report charging sessions, and provide immediate notifications about activity.

### ✅ Features:
- Built-in database of vehicles and users in Home Assistant (SQLite)
- Identification of vehicles and users using a simple service
- Automatic logging of charging sessions
- Daily usage report generation
- Automation and notifications based on identification events

### 📂 Installation:
1. Using HACS in Home Assistant:
   - Navigate to HACS → Integrations → Custom repositories
   - Enter the URL of this GitHub repository and select type "Integration"
2. Install the "Fleet Charging Manager" integration and restart Home Assistant.

### 🛠️ Usage:
- Add vehicles and users directly to the integration's SQLite database (e.g., using an SQLite editor).
- Call the service `fleet_charging.identify_vehicle` with parameters:
```yaml
service: fleet_charging.identify_vehicle
data:
  vehicle_id: "EV123"
  user_id: "user001"
```

### 📊 Available sensors in HA:
- `sensor.aktualna_relacia_nabijania` – currently identified vehicle and user
- `sensor.denny_report_nabijania` – daily activity report

---

### 🧑‍💻 Autor / Author:

- [Baerstorm](https://github.com/Bearstorm)

📌 **Feedback a návrhy vítané! / Feedback and suggestions welcome!**

