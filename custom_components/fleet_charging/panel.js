class FleetChargingPanel extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: "open" });
    }

    set hass(hass) {
        if (!this.content) {
            this.hass = hass;
            this.content = document.createElement("div");
            this.content.innerHTML = `
                <style>
                    .container {
                        padding: 20px;
                        font-family: Arial, sans-serif;
                    }
                    .card {
                        background: var(--card-background-color);
                        border-radius: 8px;
                        padding: 15px;
                        margin-bottom: 20px;
                        box-shadow: var(--ha-card-box-shadow);
                    }
                    .title {
                        font-size: 1.2em;
                        font-weight: bold;
                        margin-bottom: 10px;
                    }
                    .button {
                        background: var(--primary-color);
                        color: white;
                        border: none;
                        padding: 10px;
                        cursor: pointer;
                        border-radius: 5px;
                        margin-top: 10px;
                    }
                    .button:hover {
                        opacity: 0.8;
                    }
                    select, input {
                        width: 100%;
                        padding: 8px;
                        margin: 5px 0;
                        border: 1px solid #ccc;
                        border-radius: 4px;
                    }
                </style>
                <div class="container">
                    <div class="card">
                        <div class="title">Priradenie používateľa k vozidlu</div>
                        <select id="user_select"></select>
                        <select id="vehicle_select"></select>
                        <button class="button" id="assign_user_vehicle">Priradiť</button>
                    </div>
                    <div class="card">
                        <div class="title">Zoznam nabíjacích relácií</div>
                        <ul id="sessions_list"></ul>
                    </div>
                    <div class="card">
                        <div class="title">Správa Wallboxov</div>
                        <select id="wallbox_select"></select>
                        <select id="vehicle_wallbox_select"></select>
                        <button class="button" id="assign_wallbox">Priradiť Wallbox</button>
                    </div>
                </div>
            `;
            this.shadowRoot.appendChild(this.content);

            this.loadData();
            this.shadowRoot.getElementById("assign_user_vehicle").addEventListener("click", () => this.assignUserToVehicle());
            this.shadowRoot.getElementById("assign_wallbox").addEventListener("click", () => this.assignWallbox());
        }
    }

    async loadData() {
        try {
            const response = await fetch("/api/fleet_charging");
            const data = await response.json();

            const userSelect = this.shadowRoot.getElementById("user_select");
            const vehicleSelect = this.shadowRoot.getElementById("vehicle_select");
            const wallboxSelect = this.shadowRoot.getElementById("wallbox_select");
            const vehicleWallboxSelect = this.shadowRoot.getElementById("vehicle_wallbox_select");
            const sessionsList = this.shadowRoot.getElementById("sessions_list");

            userSelect.innerHTML = data.users.map(user => `<option value="${user.id}">${user.name}</option>`).join("");
            vehicleSelect.innerHTML = data.vehicles.map(vehicle => `<option value="${vehicle.id}">${vehicle.name}</option>`).join("");
            wallboxSelect.innerHTML = data.wallboxes.map(wallbox => `<option value="${wallbox.id}">${wallbox.name}</option>`).join("");
            vehicleWallboxSelect.innerHTML = data.vehicles.map(vehicle => `<option value="${vehicle.id}">${vehicle.name}</option>`).join("");
            sessionsList.innerHTML = data.sessions.map(session => `<li>${session.vehicle_id} - ${session.user_id} (${session.timestamp})</li>`).join("");
        } catch (error) {
            console.error("Chyba pri načítaní údajov:", error);
        }
    }

    async assignUserToVehicle() {
        const user_id = this.shadowRoot.getElementById("user_select").value;
        const vehicle_id = this.shadowRoot.getElementById("vehicle_select").value;

        const response = await fetch("/api/fleet_charging", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ action: "assign_vehicle", user_id, vehicle_id }),
        });

        const result = await response.json();
        alert(result.message);
        this.loadData();
    }

    async assignWallbox() {
        const wallbox_id = this.shadowRoot.getElementById("wallbox_select").value;
        const vehicle_id = this.shadowRoot.getElementById("vehicle_wallbox_select").value;

        const response = await fetch("/api/fleet_charging", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ action: "set_wallbox", wallbox_id, vehicle_id }),
        });

        const result = await response.json();
        alert(result.message);
        this.loadData();
    }
}

customElements.define("fleet-charging-panel", FleetChargingPanel);
