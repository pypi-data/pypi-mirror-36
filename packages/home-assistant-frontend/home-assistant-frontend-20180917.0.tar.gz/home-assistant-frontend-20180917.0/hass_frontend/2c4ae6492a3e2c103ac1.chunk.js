(window.webpackJsonp=window.webpackJsonp||[]).push([[47],{207:function(e,t,i){"use strict";i(157),i(156),i(124),i(63);var a=i(0),n=i(4);customElements.define("hass-subpage",class extends n.a{static get template(){return a["a"]`
    <style include="ha-style"></style>
    <app-header-layout has-scrolling-region="">
      <app-header slot="header" fixed="">
        <app-toolbar>
          <paper-icon-button icon="hass:arrow-left" on-click="_backTapped"></paper-icon-button>
          <div main-title="">[[header]]</div>
        </app-toolbar>
      </app-header>

      <slot></slot>
    </app-header-layout>
`}static get properties(){return{header:String}}_backTapped(){history.back()}})},391:function(e,t,i){"use strict";i.r(t),i(155);var a=i(0),n=i(4),r=(i(207),i(29)),o=(i(127),i(14)),s=(e,t)=>e<t?-1:e>t?1:0;function c(e,t){if(t.name)return t.name;const i=e.states[t.entity_id];return i?Object(r.a)(i):null}customElements.define("ha-overview-device-row",class extends(Object(o.a)(n.a)){static get template(){return a["a"]`
    <style>
      :host {
        display: block;
      }
      .device-row {
        display: flex;
        flex-direction: row;
        margin-bottom: 8px;
      }
      .device {
        width: 30%;
      }
      .device .name {
        font-weight: bold;
      }
      .device .model,
      .device .manuf {
        color: var(--secondary-text-color);
      }
      .entity-rows {
        padding-top: 12px;
        margin-left: 8px;
      }
      .entity-row {
        margin: 8px 0;
        display: flex;
        flex-direction: row;
      }
      state-badge {
        margin-right: 8px;
        cursor: pointer;
      }
      .entity-row .entity-id {
        color: var(--secondary-text-color);
      }
      ha-overview-device-row {
        margin-left: 16px;
      }
    </style>
    <div>
      <div class='device-row'>
      <div class='device'>
        <div class='name'>[[device.name]]</div>
        <div class='model'>[[device.model]]</div>
        <div class='manuf'>by [[device.manufacturer]]</div>
      </div>

      <div class='entity-rows'>
        <template is='dom-repeat' items='[[_computeDeviceEntities(hass, device, entities)]]' as='entity'>
          <div class='entity-row'>
            <state-badge
              state-obj="[[_computeStateObj(entity, hass)]]"
              on-click='_openMoreInfo'
            ></state-badge>
            <div>
              <div class='name'>[[_computeEntityName(entity, hass)]]</div>
              <div class='entity-id'>[[entity.entity_id]]</div>
            </div>
          </div class='entity-row'>
        </template>
      </div>
      </div>
      <template is='dom-repeat' items='[[_childDevices]]' as='device'>
        <ha-overview-device-row
          hass='[[hass]]'
          devices='[[devices]]'
          device='[[device]]'
          entities='[[entities]]'
        ></ha-overview-device-row>
      </template>
    </div>
    `}static get properties(){return{device:Object,devices:Array,entities:Array,hass:Object,_childDevices:{type:Array,computed:"_computeChildDevices(device, devices)"}}}_computeChildDevices(e,t){return t.filter(t=>t.hub_device_id===e.id).sort((e,t)=>s(e.name,t.name))}_computeDeviceEntities(e,t,i){return i.filter(e=>e.device_id===t.id).sort((t,i)=>s(c(e,t)||`zzz${t.entity_id}`,c(e,i)||`zzz${i.entity_id}`))}_computeStateObj(e,t){return t.states[e.entity_id]}_computeEntityName(e,t){return c(t,e)||"(entity unavailable)"}_computeDeviceName(e,t){const i=e.find(e=>e.id===t);return i?i.name:"(device unavailable)"}_openMoreInfo(e){this.fire("hass-more-info",{entityId:e.model.entity.entity_id})}}),customElements.define("ha-config-overview",class extends n.a{static get template(){return a["a"]`
    <style>
      a {
        color: var(--primary-color);
      }
      paper-card {
        display: block;
        margin: 16px auto;
        max-width: 500px;
      }
      li {
        color: var(--primary-text-color);
      }
      .secondary {
        color: var(--secondary-text-color);
      }
      .device-row {
        display: flex;
        flex-direction: row;
        margin-bottom: 8px;
      }
      .device {
        width: 30%;
      }
      .device .name {
        font-weight: bold;
      }
      .device .model,
      .device .manuf,
      .device .hub {
        color: var(--secondary-text-color);
      }
      .entity-rows {
        padding-top: 12px;
        margin-left: 8px;
      }
      .entity-row {
        margin: 8px 0;
        display: flex;
        flex-direction: row;
      }
      state-badge {
        margin-right: 8px;
      }
      .entity-row .entity-id {
        color: var(--secondary-text-color);
      }
    </style>
    <hass-subpage header="Overview">
      <div class='content'>
        <template is='dom-if' if='[[!_configs.length]]'>
          <paper-card heading='No integrations'>
            <div class='card-content'>
              No integrations found. <a href='/config/integrations'>Configure an integration</a>
            </div>
          </paper-card>
        </template>
        <template is='dom-repeat' items='[[_configs]]' as='configEntry'>
          <paper-card heading='[[configEntry.title]]'>
            <div class='card-content'>
              <!-- <h1>[[configEntry.title]] ([[_computeIntegrationTitle(localize, configEntry.domain)]])</h1> -->

              <template is='dom-repeat' items='[[_computeConfigEntryDevices(configEntry, _devices)]]' as='device'>
                <ha-overview-device-row
                  hass='[[hass]]'
                  devices='[[_devices]]'
                  device='[[device]]'
                  entities='[[_entities]]'
                ></ha-overview-device-row>
              </template>
            </div>
          </paper-card>
        </dom-repeat>
      </div>
    </hass-subpage>
`}static get properties(){return{hass:Object,isWide:Boolean,_loading:{type:Boolean,computed:"_computeLoading(_configs, _devices, _entities)"},_configs:{type:Array,value:null},_devices:{type:Array,value:null},_entities:{type:Array,value:null}}}ready(){super.ready(),this._loadData()}connectedCallback(){super.connectedCallback()}disconnectedCallback(){super.disconnectedCallback()}_loadData(){this.hass.callWS({type:"config/entity_registry/list"}).then(e=>{this._entities=e}),this.hass.callWS({type:"config/device_registry/list"}).then(e=>{this._devices=e}),this.hass.callApi("get","config/config_entries/entry").then(e=>{this._configs=e.sort((e,t)=>s(e.title,t.title))})}_computeLoading(e,t,i){return e&&t&&i}_computeIntegrationTitle(e,t){return e(`component.${t}.config.title`)}_computeConfigEntryDevices(e,t){return t.filter(t=>t.config_entries.includes(e.entry_id)&&!t.hub_device_id).sort((e,t)=>s(e.name,t.name))}_computeDeviceEntities(e,t){return t.filter(t=>t.device_id===e.id)}_computeStateObj(e,t){return t.states[e.entity_id]}_computeEntityName(e,t){const i=t.states[e.entity_id];return i?Object(r.a)(i):`${e.name||""} (entity unavailable)`}_computeDeviceName(e,t){const i=e.find(e=>e.id===t);return i?i.name:"(device unavailable)"}})}}]);
//# sourceMappingURL=2c4ae6492a3e2c103ac1.chunk.js.map