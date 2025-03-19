class FleetChargingPanel extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: "open" });
    }

    set hass(hass) {
        if (!this.content) {
            this.renderUI(hass);
        }
    }

    renderUI(hass) {
        this.shadowRoot.innerHTML = `
            <style>
                :host {
                    display: block;
                    font-family: Arial, sans-serif;
                    padding: 16px;
                }
                h1 {
                    font-size: 24px;
                    font-weight: bold;
                    margin-bottom: 16px;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                }
                th, td {
                    padding: 12px;
                    border: 1px solid #ddd;
                    text-align: left;
                }
                th {
                    background-color: #f4f4f4;
                }
                .actions {
                    display: flex;
                    gap: 8px;
                }
                button {
                    padding: 6px 12px;
                    border: none;
                    cursor: pointer;
                    border-radius: 4px;
                }
                .add-button {
                    background-color: #2196F3;
                    color: white;
                }
                .delete-button {
                    background-color: #f44336;
                    color: white;
                }
            </style>

            <h1>Správa nabíjania</h1>

            <h2>Vozidlá</h2>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Názov</th>
                    <th>Akcie</th>
                </tr>
                ${this.getVehicles(hass).map(vehicle => `
                    <tr>
                        <td>${vehicle.id}</td>
                        <td>${vehicle.name}</td>
                        <td class="actions">
                            <button class="delete-button" data-id="${vehicle.id}">Odstrániť</button>
                        </td>
                    </tr>
                `).join('')}
            </table>
            <button class="add-button" id="add-vehicle">Pridať vozidlo</button>

            <h2>Používatelia</h2>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Meno</th>
                    <th>Akcie</th>
                </tr>
                ${this.getUsers(hass).map(user => `
                    <tr>
                        <td>${user.id}</td>
                        <td>${user.name}</td>
                        <td class="actions">
                            <button class="delete-button" data-id="${user.id}">Odstrániť</button>
                        </td>
                    </tr>
                `).join('')}
            </table>
            <button class="add-button" id="add-user">Pridať používateľa</button>

            <h2>Wallboxy</h2>
            <table>
                <tr>
                    <th>Wallbox</th>
                    <th>Pripojené vozidlo</th>
                    <th>Stav</th>
                </tr>
                ${this.getWallboxStatus(hass).map(wallbox => `
                    <tr>
                        <td>${wallbox.name}</td>
                        <td>${wallbox.vehicle || "Nepripojené"}</td>
                        <td>${wallbox.status}</td>
                    </tr>
                `).join('')}
            </table>

            <h2>Akcie</h2>
            <button class="add-button" id="authorize-charging">Autorizovať nabíjanie</button>
        `;

        this.shadowRoot.getElementById("add-vehicle").addEventListener("click", () => this.addVehicle(hass));
        this.shadowRoot.getElementById("add-user").addEventListener("click", () => this.addUser(hass));
        this.shadowRoot.getElementById("authorize-charging").addEventListener("click", () => this.authorizeCharging(hass));

        this.shadowRoot.querySelectorAll(".delete-button").forEach(button => {
            button.addEventListener("click", (event) => {
                this.deleteItem(hass, event.target.dataset.id);
            });
        });
    }

    getVehicles(hass) {
        return hass.states["sensor.fleet_charging_vehicles"]?.attributes?.vehicles || [];
    }

    getUsers(hass) {
        return hass.states["sensor.fleet_charging_users"]?.attributes?.users || [];
    }

    getWallboxStatus(hass) {
        return hass.states["sensor.fleet_charging_wallbox_status"]?.attributes?.wallboxes || [];
    }

    addVehicle(hass) {
        const vehicleId = prompt("Zadajte ID vozidla:");
        const vehicleName = prompt("Zadajte názov vozidla:");
        if (vehicleId && vehicleName) {
            hass.callService("fleet_charging", "add_vehicle", {
                vehicle_id: vehicleId,
                name: vehicleName
            });
        }
    }

    addUser(hass) {
        const userId = prompt("Zadajte ID používateľa:");
        const userName = prompt("Zadajte meno používateľa:");
        if (userId && userName) {
            hass.callService("fleet_charging", "add_user", {
                user_id: userId,
                name: userName
            });
        }
    }

    deleteItem(hass, id) {
        if (confirm("Naozaj chcete odstrániť tento záznam?")) {
            hass.callService("fleet_charging", "delete_item", { id: id });
        }
    }

    authorizeCharging(hass) {
        alert("Autorizácia nabíjania bola odoslaná!");
        hass.callService("fleet_charging", "authorize_charging", {});
    }
}

customElements.define("fleet-charging-panel", FleetChargingPanel);

window.customPanels = window.customPanels || [];
window.customPanels.push({
    component_name: "fleet-charging-panel",
    sidebar_title: "Fleet Charging",
    sidebar_icon: "mdi:ev-station",
    module_url: "/local/fleet_charging/panel.js"
});
