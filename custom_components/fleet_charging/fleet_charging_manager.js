class FleetChargingManager extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: "open" });
    }

    async connectedCallback() {
        this.render();
        await this.fetchData();
    }

    async fetchData() {
        try {
            const response = await fetch("/api/fleet_charging");
            if (!response.ok) throw new Error("Chyba pri načítaní údajov");
            const data = await response.json();
            this.updateData(data);
        } catch (error) {
            console.error("Chyba API:", error);
        }
    }

    updateData(data) {
        const userList = this.shadowRoot.getElementById("user-list");
        const vehicleList = this.shadowRoot.getElementById("vehicle-list");
        const sessionList = this.shadowRoot.getElementById("session-list");

        userList.innerHTML = data.users
            .map(user => `<li>${user.id}: ${user.name}</li>`)
            .join("");

        vehicleList.innerHTML = data.vehicles
            .map(vehicle => `<li>${vehicle.id}: ${vehicle.name}</li>`)
            .join("");

        sessionList.innerHTML = data.sessions
            .map(session => `<li>${session.timestamp} - ${session.vehicle_id} nabíjal ${session.user_id}</li>`)
            .join("");
    }

    async addUser() {
        const userId = this.shadowRoot.getElementById("new-user-id").value;
        const userName = this.shadowRoot.getElementById("new-user-name").value;

        if (!userId || !userName) {
            alert("Zadajte ID a meno používateľa.");
            return;
        }

        await fetch("/api/fleet_charging/add_user", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_id: userId, name: userName })
        });

        await this.fetchData();
    }

    async addVehicle() {
        const vehicleId = this.shadowRoot.getElementById("new-vehicle-id").value;
        const vehicleName = this.shadowRoot.getElementById("new-vehicle-name").value;

        if (!vehicleId || !vehicleName) {
            alert("Zadajte ID a názov vozidla.");
            return;
        }

        await fetch("/api/fleet_charging/add_vehicle", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ vehicle_id: vehicleId, name: vehicleName })
        });

        await this.fetchData();
    }

    render() {
        this.shadowRoot.innerHTML = `
            <style>
                .container {
                    font-family: Arial, sans-serif;
                    padding: 10px;
                    max-width: 600px;
                }
                h2 { margin-bottom: 10px; }
                .section { margin-bottom: 20px; }
                ul { list-style-type: none; padding: 0; }
                li { padding: 5px; border-bottom: 1px solid #ddd; }
                input, button { padding: 5px; margin-top: 5px; }
                .add-section { display: flex; gap: 10px; }
            </style>

            <div class="container">
                <h2>Fleet Charging Manager</h2>

                <div class="section">
                    <h3>Používatelia</h3>
                    <ul id="user-list"></ul>
                    <div class="add-section">
                        <input id="new-user-id" type="text" placeholder="ID používateľa">
                        <input id="new-user-name" type="text" placeholder="Meno používateľa">
                        <button onclick="this.getRootNode().host.addUser()">Pridať</button>
                    </div>
                </div>

                <div class="section">
                    <h3>Vozidlá</h3>
                    <ul id="vehicle-list"></ul>
                    <div class="add-section">
                        <input id="new-vehicle-id" type="text" placeholder="ID vozidla">
                        <input id="new-vehicle-name" type="text" placeholder="Názov vozidla">
                        <button onclick="this.getRootNode().host.addVehicle()">Pridať</button>
                    </div>
                </div>

                <div class="section">
                    <h3>Nabíjacie relácie</h3>
                    <ul id="session-list"></ul>
                </div>
            </div>
        `;
    }
}

customElements.define("fleet-charging-manager", FleetChargingManager);
