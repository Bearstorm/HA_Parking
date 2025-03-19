class FleetChargingManagerPanel extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: "open" });
    }

    set hass(hass) {
        this.hass = hass;
        this.render();
    }

    async fetchData() {
        const response = await fetch("/api/fleet_charging");
        if (!response.ok) {
            console.error("Nepodarilo sa načítať dáta.");
            return;
        }
        this.data = await response.json();
        this.render();
    }

    async sendAction(action, payload) {
        const response = await fetch("/api/fleet_charging", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ action, ...payload }),
        });
        if (response.ok) {
            await this.fetchData();
        } else {
            console.error("Chyba pri odosielaní akcie:", action);
        }
    }

    render() {
        if (!this.shadowRoot) return;

        this.shadowRoot.innerHTML = `
            <style>
                .container {
                    padding: 20px;
                    font-family: Arial, sans-serif;
                }
                .section {
                    margin-bottom: 20px;
                    padding: 15px;
                    border: 1px solid #ccc;
                    border-radius: 10px;
                    background: #fff;
                }
                button {
                    padding: 10px;
                    margin-top: 10px;
                    background-color: #007bff;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                }
                select, input {
                    width: 100%;
                    padding: 8px;
                    margin-top: 5px;
                }
            </style>
            <div class="container">
                <h2>🚗 Fleet Charging Manager</h2>

                <div class="section">
                    <h3>📌 Pridanie užívateľa</h3>
                    <input id="user_name" placeholder="Meno užívateľa">
                    <button id="add_user">Pridať užívateľa</button>
                </div>

                <div class="section">
                    <h3>🚘 Pridanie vozidla</h3>
                    <input id="vehicle_name" placeholder="Názov vozidla">
                    <button id="add_vehicle">Pridať vozidlo</button>
                </div>

                <div class="section">
                    <h3>🔗 Priradenie vozidla k užívateľovi</h3>
                    <select id="user_select">
                        ${this.data?.users.map(user => `<option value="${user.id}">${user.name}</option>`).join("")}
                    </select>
                    <select id="vehicle_select">
                        ${this.data?.vehicles.map(vehicle => `<option value="${vehicle.id}">${vehicle.name}</option>`).join("")}
                    </select>
                    <button id="assign_vehicle">Priradiť vozidlo</button>
                </div>

                <div class="section">
                    <h3>🔌 Priradenie vozidla k Wallboxu</h3>
                    <select id="wallbox_select">
                        ${this.data?.wallboxes.map(wallbox => `<option value="${wallbox.id}">${wallbox.location}</option>`).join("")}
                    </select>
                    <select id="vehicle_wallbox_select">
                        ${this.data?.vehicles.map(vehicle => `<option value="${vehicle.id}">${vehicle.name}</option>`).join("")}
                    </select>
                    <button id="set_wallbox">Priradiť Wallbox</button>
                </div>

                <div class="section">
                    <h3>📊 Nabíjacie relácie</h3>
                    <ul>
                        ${this.data?.sessions.map(session => `
                            <li>${session.timestamp}: ${session.vehicle_id} - ${session.user_id} (Wallbox: ${session.wallbox_id})</li>
                        `).join("")}
                    </ul>
                </div>
            </div>
        `;

        this.shadowRoot.querySelector("#add_user").addEventListener("click", () => {
            const userName = this.shadowRoot.querySelector("#user_name").value;
            this.sendAction("add_user", { user_id: Date.now().toString(), user_name: userName });
        });

        this.shadowRoot.querySelector("#add_vehicle").addEventListener("click", () => {
            const vehicleName = this.shadowRoot.querySelector("#vehicle_name").value;
            this.sendAction("add_vehicle", { vehicle_id: Date.now().toString(), vehicle_name: vehicleName });
        });

        this.shadowRoot.querySelector("#assign_vehicle").addEventListener("click", () => {
            const userId = this.shadowRoot.querySelector("#user_select").value;
            const vehicleId = this.shadowRoot.querySelector("#vehicle_select").value;
            this.sendAction("assign_vehicle", { user_id: userId, vehicle_id: vehicleId });
        });

        this.shadowRoot.querySelector("#set_wallbox").addEventListener("click", () => {
            const wallboxId = this.shadowRoot.querySelector("#wallbox_select").value;
            const vehicleId = this.shadowRoot.querySelector("#vehicle_wallbox_select").value;
            this.sendAction("set_wallbox", { wallbox_id: wallboxId, vehicle_id: vehicleId });
        });
    }
}

customElements.define("fleet-charging-manager-panel", FleetChargingManagerPanel);
