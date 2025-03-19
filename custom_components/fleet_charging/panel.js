class FleetChargingPanel extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: "open" });
    }

    set hass(hass) {
        if (!this.content) {
            this.content = document.createElement("div");
            this.content.innerHTML = `
                <style>
                    .container {
                        display: grid;
                        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                        gap: 20px;
                        padding: 20px;
                    }
                    .card {
                        background: var(--card-background-color);
                        padding: 20px;
                        border-radius: 10px;
                        box-shadow: var(--ha-card-box-shadow);
                    }
                    h2 {
                        margin: 0;
                        font-size: 1.5em;
                    }
                </style>
                <div class="container">
                    <div class="card">
                        <h2>Priradenie používateľov a vozidiel</h2>
                        <p><strong>Aktuálne priradené:</strong></p>
                        <ul id="user-vehicle-list"></ul>
                    </div>
                    <div class="card">
                        <h2>Wallboxy a spotreba</h2>
                        <p><strong>Spotreba Wallboxov:</strong></p>
                        <p id="wallbox-energy"></p>
                    </div>
                </div>
            `;
            this.shadowRoot.appendChild(this.content);
        }

        // Aktualizácia dát
        const userVehicleList = this.shadowRoot.getElementById("user-vehicle-list");
        userVehicleList.innerHTML = hass.states["sensor.fleet_charging_users"].state.split(",").map(u => `<li>${u}</li>`).join("");

        const wallboxEnergy = this.shadowRoot.getElementById("wallbox-energy");
        wallboxEnergy.textContent = hass.states["sensor.wallbox_energy"].state + " kWh";
    }
}

customElements.define("fleet-charging-panel", FleetChargingPanel);
