class FleetChargingManager extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: "open" });
    }

    set hass(hass) {
        if (!this.content) {
            this.createUI();
        }
        this.updateUI(hass);
    }

    createUI() {
        this.content = document.createElement("div");
        this.content.innerHTML = `
            <style>
                .container {
                    padding: 16px;
                    font-family: Arial, sans-serif;
                }
                .section {
                    margin-bottom: 20px;
                    padding: 10px;
                    border-radius: 8px;
                    background: #1e1e1e;
                    color: white;
                }
                .section h2 {
                    margin: 0;
                    padding-bottom: 10px;
                    border-bottom: 1px solid #444;
                }
                .entry {
                    display: flex;
                    justify-content: space-between;
                    padding: 5px 0;
                }
                .button {
                    background: #007bff;
                    color: white;
                    padding: 5px 10px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                }
                .button:hover {
                    background: #0056b3;
                }
                select, input {
                    padding: 5px;
                    border-radius: 5px;
                    border: 1px solid #ccc;
                    width: 100%;
                }
                .grid {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 10px;
                }
            </style>

            <div class="container">
                <div class="section">
                    <h2>Správa používateľov a vozidiel</h2>
                    <div class="grid">
                        <div>
                            <label>Vyberte spoločnosť</label>
                            <select id="companySelection"></select>
                        </div>
                        <div>
                            <label>Vyberte používateľa</label>
                            <select id="userSelection"></select>
                        </div>
                    </div>
                    <button id="assignUserBtn" class="button">Priradiť používateľa</button>
                </div>

                <div class="section">
                    <h2>Správa wallboxov</h2>
                    <div class="grid">
                        <div>
                            <label>Vyberte vozidlo</label>
                            <select id="vehicleSelection"></select>
                        </div>
                        <div>
                            <label>Vyberte wallbox</label>
                            <select id="wallboxSelection"></select>
                        </div>
                    </div>
                    <button id="authorizeWallboxBtn" class="button">Autorizovať wallbox</button>
                </div>

                <div class="section">
                    <h2>Aktuálne nabíjanie</h2>
                    <p id="chargingStatus">Žiadna aktívna nabíjacia relácia</p>
                </div>
            </div>
        `;
        this.shadowRoot.appendChild(this.content);
        this.attachEventListeners();
    }

    attachEventListeners() {
        this.shadowRoot.getElementById("assignUserBtn").addEventListener("click", () => this.assignUser());
        this.shadowRoot.getElementById("authorizeWallboxBtn").addEventListener("click", () => this.authorizeWallbox());
    }

    async updateUI(hass) {
        try {
            const response = await fetch("/api/fleet_charging?action=get_vehicles");
            const data = await response.json();
            const vehicleSelect = this.shadowRoot.getElementById("vehicleSelection");
            vehicleSelect.innerHTML = data.vehicles.map(v => `<option value="${v.id}">${v.name}</option>`).join("");

            const userResponse = await fetch("/api/fleet_charging?action=get_users");
            const userData = await userResponse.json();
            const userSelect = this.shadowRoot.getElementById("userSelection");
            userSelect.innerHTML = userData.users.map(u => `<option value="${u.id}">${u.name}</option>`).join("");

            const sessionResponse = await fetch("/api/fleet_charging?action=get_active_session");
            const sessionData = await sessionResponse.json();
            this.shadowRoot.getElementById("chargingStatus").innerText = sessionData.active_session 
                ? `Nabíja sa: ${sessionData.active_session.vehicle_name} - ${sessionData.active_session.user_name}` 
                : "Žiadna aktívna nabíjacia relácia";
        } catch (error) {
            console.error("Chyba pri načítaní údajov:", error);
        }
    }

    async assignUser() {
        const user_id = this.shadowRoot.getElementById("userSelection").value;
        const vehicle_id = this.shadowRoot.getElementById("vehicleSelection").value;

        const response = await fetch("/api/fleet_charging", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ action: "assign_vehicle", user_id, vehicle_id })
        });

        if (response.ok) {
            alert("Používateľ bol úspešne priradený k vozidlu.");
        } else {
            alert("Chyba pri priraďovaní používateľa.");
        }
    }

    async authorizeWallbox() {
        const user_id = this.shadowRoot.getElementById("userSelection").value;
        const wallbox_id = this.shadowRoot.getElementById("wallboxSelection").value;

        const response = await fetch("/api/fleet_charging", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ action: "authorize_wallbox", user_id, wallbox_id })
        });

        if (response.ok) {
            alert("Wallbox bol úspešne autorizovaný.");
        } else {
            alert("Chyba pri autorizácii wallboxu.");
        }
    }
}

customElements.define("fleet-charging-manager", FleetChargingManager);
