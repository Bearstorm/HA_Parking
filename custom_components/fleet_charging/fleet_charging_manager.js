class FleetChargingPanel extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: "open" });
    }

    connectedCallback() {
        this.render();
        this.updateData();
        setInterval(() => this.updateData(), 5000);
    }

    async updateData() {
        const response = await fetch("/api/states");
        this.data = await response.json();
        this.render();
    }

    render() {
        if (!this.data) return;

        this.shadowRoot.innerHTML = `
            <style>
                .container {
                    font-family: Arial, sans-serif;
                    padding: 16px;
                }
                .card {
                    background: #1e1e1e;
                    color: white;
                    padding: 16px;
                    margin-bottom: 10px;
                    border-radius: 8px;
                }
                select, button {
                    padding: 8px;
                    margin-top: 8px;
                    width: 100%;
                    font-size: 16px;
                }
            </style>
            <div class="container">
                <h1>Fleet Charging Manager</h1>

                <div class="card">
                    <h3>Vyberte Wallbox</h3>
                    <select id="wallboxSelect">
                        ${this.getWallboxOptions()}
                    </select>
                </div>

                <div class="card">
                    <h3>Vyberte Vozidlo</h3>
                    <select id="vehicleSelect">
                        ${this.getVehicleOptions()}
                    </select>
                </div>

                <div class="card">
                    <h3>Aktuálna relácia</h3>
                    <p>${this.getCurrentSession()}</p>
                </div>

                <div class="card">
                    <h3>Spotreba Wallboxu</h3>
                    <p>${this.getWallboxEnergy()}</p>
                </div>

                <button onclick="startCharging()">Spustiť nabíjanie</button>
            </div>
        `;
    }

    getWallboxOptions() {
        return this.data
            .filter(state => state.entity_id.startsWith("sensor.") && state.entity_id.includes("wallbox"))
            .map(state => `<option value="${state.entity_id}">${state.attributes.friendly_name}</option>`)
            .join("");
    }

    getVehicleOptions() {
        return this.data
            .filter(state => state.entity_id.startsWith("sensor.") && state.entity_id.includes("vehicle"))
            .map(state => `<option value="${state.entity_id}">${state.attributes.friendly_name}</option>`)
            .join("");
    }

    getCurrentSession() {
        const session = this.data.find(state => state.entity_id === "sensor.fleet_charging_session");
        return session ? session.state : "Žiadna aktívna relácia";
    }

    getWallboxEnergy() {
        const energy = this.data.find(state => state.entity_id === "sensor.wallbox_energy");
        return energy ? energy.state + " kWh" : "Dáta nie sú dostupné";
    }
}

customElements.define("fleet-charging-panel", FleetChargingPanel);
