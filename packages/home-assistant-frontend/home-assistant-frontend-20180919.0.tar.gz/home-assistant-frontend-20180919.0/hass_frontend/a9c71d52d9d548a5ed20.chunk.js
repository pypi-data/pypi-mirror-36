/*! For license information please see a9c71d52d9d548a5ed20.chunk.js.LICENSE */
(window.webpackJsonp=window.webpackJsonp||[]).push([[42],{197:function(e,t,o){"use strict";o(2),o(26),o(30),o(43);var i=o(3),r=o(0);Object(i.a)({_template:r["a"]`
    <style>
      :host {
        overflow: hidden; /* needed for text-overflow: ellipsis to work on ff */
        @apply --layout-vertical;
        @apply --layout-center-justified;
        @apply --layout-flex;
      }

      :host([two-line]) {
        min-height: var(--paper-item-body-two-line-min-height, 72px);
      }

      :host([three-line]) {
        min-height: var(--paper-item-body-three-line-min-height, 88px);
      }

      :host > ::slotted(*) {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      :host > ::slotted([secondary]) {
        @apply --paper-font-body1;

        color: var(--paper-item-body-secondary-color, var(--secondary-text-color));

        @apply --paper-item-body-secondary;
      }
    </style>

    <slot></slot>
`,is:"paper-item-body"})},648:function(e,t,o){"use strict";o.r(t),o(120),o(197);var i=o(0),r=o(4),a=o(14),p=o(79);customElements.define("ha-pick-auth-provider",class extends(Object(a.a)(Object(p.a)(r.a))){static get template(){return i["a"]`
    <style>
      paper-item {
        cursor: pointer;
      }
      p {
        margin-top: 0;
      }
    </style>
    <p>[[localize('ui.panel.page-authorize.pick_auth_provider')]]:</p>
    <template is="dom-repeat" items="[[authProviders]]">
      <paper-item on-click="_handlePick">
        <paper-item-body>[[item.name]]</paper-item-body>
        <iron-icon icon="hass:chevron-right"></iron-icon>
      </paper-item>
    </template>
`}static get properties(){return{_state:{type:String,value:"loading"},authProviders:Array}}_handlePick(e){this.fire("pick",e.model.item)}_equal(e,t){return e===t}})}}]);
//# sourceMappingURL=a9c71d52d9d548a5ed20.chunk.js.map