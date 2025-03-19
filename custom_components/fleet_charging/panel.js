class FleetChargingPanel extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: "open" });
    }

    set hass(hass) {
        this.hass = hass;
        this.fetchData();
    }

    async fetchData() {
        try {
            const response = await fetch("/api/fleet_charging");
            this.data = await response.json();
            this.render();
        } catch (error) {
            console.error("Chyba pri načítaní údajov:", error);
        }
    }

    render() {
        if (!this.shadowRoot) return;

        this.shadowRoot.innerHTML = `
            <style>
                .container { padding: 20px; font-family: Arial, sans-serif; }
                h2 { color: #3498db; }
                .section { margin-bottom: 20px; padding: 10px; border: 1px solid #ddd; border-radius: 5px; background: #f9f9f9; }
                .section h3 { margin-top: 0; }
                .item { padding: 5px 0; }
            </style>
            <div class="container">
                <h2>Fleet Charging Manager</h2>
                <div class="section">
                    <h3>🔹 Priradenie používateľov</h3>
                    ${this.data?.users?.map(user => `<div class="item">👤 ${user.name}</div>`).join('') || "Žiadni používatelia"}
                </div>
                <div class="section">
                    <h3>🚗 Vozidlá</h3>
                    ${this.data?.vehicles?.map(vehicle => `<div class="item">🚘 ${vehicle.name}</div>`).join('') || "Žiadne vozidlá"}
                </div>
                <div class="section">
                    <h3>⚡ Nabíjacie relácie</h3>
                    ${this.data?.sessions?.map(session => `<div class="item">🔋 ${session.vehicle_id} nabíjané užívateľom ${session.user_id}</div>`).join('') || "Žiadne relácie"}
                </div>
            </div>
        `;
    }
}

customElements.define("fleet-charging-panel", FleetChargingPanel);
