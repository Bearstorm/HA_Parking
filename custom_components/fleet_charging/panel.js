window.customPanels = window.customPanels || [];
window.customPanels.push({
    name: "fleet_charging",
    embed_iframe: false,
    component_name: "fleet-charging-panel",
    js_url: "/hacsfiles/fleet_charging_manager.js",
    config: {}
});

class FleetChargingPanel extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: "open" });
    }

    async connectedCallback() {
        this.render();
    }

    render() {
        this.shadowRoot.innerHTML = `
            <style>
                .container {
                    font-family: Arial, sans-serif;
                    padding: 20px;
                    max-width: 800px;
                }
                h1 {
                    font-size: 24px;
                    margin-bottom: 20px;
                }
                fleet-charging-manager {
                    display: block;
                    width: 100%;
                }
            </style>

            <div class="container">
                <h1>Fleet Charging Panel</h1>
                <fleet-charging-manager></fleet-charging-manager>
            </div>
        `;
    }
}

customElements.define("fleet-charging-panel", FleetChargingPanel);
