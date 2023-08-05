/*! For license information please see cf372946095cae18176f.chunk.js.LICENSE */
(window.webpackJsonp=window.webpackJsonp||[]).push([[54],{197:function(e,t,a){"use strict";a(2),a(26),a(30),a(43);var r=a(3),s=a(0);Object(r.a)({_template:s["a"]`
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
`,is:"paper-item-body"})},207:function(e,t,a){"use strict";a(155),a(154),a(122),a(62);var r=a(0),s=a(4);customElements.define("hass-subpage",class extends s.a{static get template(){return r["a"]`
    <style include="ha-style"></style>
    <app-header-layout has-scrolling-region="">
      <app-header slot="header" fixed="">
        <app-toolbar>
          <paper-icon-button icon="hass:arrow-left" on-click="_backTapped"></paper-icon-button>
          <div main-title="">[[header]]</div>
          <slot name="toolbar-icon"></slot>
        </app-toolbar>
      </app-header>

      <slot></slot>
    </app-header-layout>
`}static get properties(){return{header:String}}_backTapped(){history.back()}})},236:function(e,t,a){"use strict";a(2),a(26),a(75),a(64),a(48),a(30);var r=a(59),s=a(3),i=a(0);const o=i["a"]`
  <style include="paper-material-styles">
    :host {
      @apply --layout-vertical;
      @apply --layout-center-center;

      background: var(--paper-fab-background, var(--accent-color));
      border-radius: 50%;
      box-sizing: border-box;
      color: var(--text-primary-color);
      cursor: pointer;
      height: 56px;
      min-width: 0;
      outline: none;
      padding: 16px;
      position: relative;
      -moz-user-select: none;
      -ms-user-select: none;
      -webkit-user-select: none;
      user-select: none;
      width: 56px;
      z-index: 0;

      /* NOTE: Both values are needed, since some phones require the value \`transparent\`. */
      -webkit-tap-highlight-color: rgba(0,0,0,0);
      -webkit-tap-highlight-color: transparent;

      @apply --paper-fab;
    }

    [hidden] {
      display: none !important;
    }

    :host([mini]) {
      width: 40px;
      height: 40px;
      padding: 8px;

      @apply --paper-fab-mini;
    }

    :host([disabled]) {
      color: var(--paper-fab-disabled-text, var(--paper-grey-500));
      background: var(--paper-fab-disabled-background, var(--paper-grey-300));

      @apply --paper-fab-disabled;
    }

    iron-icon {
      @apply --paper-fab-iron-icon;
    }

    span {
      width: 100%;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      text-align: center;

      @apply --paper-fab-label;
    }

    :host(.keyboard-focus) {
      background: var(--paper-fab-keyboard-focus-background, var(--paper-pink-900));
    }

    :host([elevation="1"]) {
      @apply --paper-material-elevation-1;
    }

    :host([elevation="2"]) {
      @apply --paper-material-elevation-2;
    }

    :host([elevation="3"]) {
      @apply --paper-material-elevation-3;
    }

    :host([elevation="4"]) {
      @apply --paper-material-elevation-4;
    }

    :host([elevation="5"]) {
      @apply --paper-material-elevation-5;
    }
  </style>

  <iron-icon id="icon" hidden\$="{{!_computeIsIconFab(icon, src)}}" src="[[src]]" icon="[[icon]]"></iron-icon>
  <span hidden\$="{{_computeIsIconFab(icon, src)}}">{{label}}</span>
`;o.setAttribute("strip-whitespace",""),Object(s.a)({_template:o,is:"paper-fab",behaviors:[r.a],properties:{src:{type:String,value:""},icon:{type:String,value:""},mini:{type:Boolean,value:!1,reflectToAttribute:!0},label:{type:String,observer:"_labelChanged"}},_labelChanged:function(){this.setAttribute("aria-label",this.label)},_computeIsIconFab:function(e,t){return e.length>0||t.length>0}})},625:function(e,t,a){"use strict";a.r(t),a(89);var r=a(8),s=a(15),i=a(0),o=a(4),p=a(81),n=(a(236),a(120),a(153),a(197),a(207),a(13)),l=a(14);let d=!1;customElements.define("ha-user-picker",class extends(Object(l.a)(Object(p.a)(Object(n.a)(o.a)))){static get template(){return i["a"]`
  <style>
    paper-fab {
      position: fixed;
      bottom: 16px;
      right: 16px;
      z-index: 1;
    }
    paper-fab[is-wide] {
      bottom: 24px;
      right: 24px;
    }
    paper-card {
      display: block;
      max-width: 600px;
      margin: 16px auto;
    }
    a {
      text-decoration: none;
      color: var(--primary-text-color);
    }
  </style>

  <hass-subpage header="[[localize('ui.panel.config.users.picker.title')]]">
    <paper-card>
      <template is="dom-repeat" items="[[users]]" as="user">
        <a href='[[_computeUrl(user)]]'>
          <paper-item>
            <paper-item-body two-line>
              <div>[[_withDefault(user.name, 'Unnamed User')]]</div>
              <div secondary="">
                [[user.id]]
                <template is='dom-if' if='[[user.system_generated]]'>
                - System Generated
                </template>
              </div>
            </paper-item-body>
            <iron-icon icon="hass:chevron-right"></iron-icon>
          </paper-item>
        </a>
      </template>
    </paper-card>

    <paper-fab
      is-wide$="[[isWide]]"
      icon="hass:plus"
      title="[[localize('ui.panel.config.users.picker.add_user')]]"
      on-click="_addUser"
    ></paper-fab>
  </hass-subpage>
`}static get properties(){return{hass:Object,users:Array}}connectedCallback(){super.connectedCallback(),d||(d=!0,this.fire("register-dialog",{dialogShowEvent:"show-add-user",dialogTag:"ha-dialog-add-user",dialogImport:()=>a.e(60).then(a.bind(null,651))}))}_withDefault(e,t){return e||t}_computeUrl(e){return`/config/users/${e.id}`}_addUser(){this.fire("show-add-user",{hass:this.hass,dialogClosedCallback:async({userId:e})=>{this.fire("reload-users"),e&&this.navigate(`/config/users/${e}`)}})}}),a(55),customElements.define("ha-user-editor",class extends(Object(l.a)(Object(p.a)(Object(n.a)(o.a)))){static get template(){return i["a"]`
  <style>
    paper-card {
      display: block;
      max-width: 600px;
      margin: 0 auto 16px;
    }
    paper-card:first-child {
      margin-top: 16px;
    }
    paper-card:last-child {
      margin-bottom: 16px;
    }
  </style>

  <hass-subpage header="View user">
    <paper-card heading="[[_computeName(user)]]">
      <table class='card-content'>
        <tr>
          <td>ID</td>
          <td>[[user.id]]</td>
        </tr>
        <tr>
          <td>Owner</td>
          <td>[[user.is_owner]]</td>
        </tr>
        <tr>
          <td>Active</td>
          <td>[[user.is_active]]</td>
        </tr>
        <tr>
          <td>System generated</td>
          <td>[[user.system_generated]]</td>
        </tr>
      </table>
    </paper-card>
    <paper-card>
      <div class='card-actions'>
        <paper-button on-click='_deleteUser' disabled='[[user.system_generated]]'>
          [[localize('ui.panel.config.users.editor.delete_user')]]
        </paper-button>
        <template is='dom-if' if='[[user.system_generated]]'>
          Unable to remove system generated users.
        </template>
      </div>
    </paper-card>
  </hass-subpage>
`}static get properties(){return{hass:Object,user:Object}}_computeName(e){return e&&(e.name||"Unnamed user")}async _deleteUser(e){if(confirm(`Are you sure you want to delete ${this._computeName(this.user)}`)){try{await this.hass.callWS({type:"config/auth/delete",user_id:this.user.id})}catch(e){return void alert(e.code)}this.fire("reload-users"),this.navigate("/config/users")}else e.target.blur()}}),customElements.define("ha-config-users",class extends(Object(p.a)(o.a)){static get template(){return i["a"]`
    <app-route
      route='[[route]]'
      pattern='/users/:user'
      data="{{_routeData}}"
    ></app-route>

    <template is='dom-if' if='[[_equals(_routeData.user, "picker")]]'>
      <ha-user-picker
        hass='[[hass]]'
        users='[[_users]]'
      ></ha-user-picker>
    </template>
    <template is='dom-if' if='[[!_equals(_routeData.user, "picker")]]' restamp>
      <ha-user-editor
        hass='[[hass]]'
        user='[[_computeUser(_users, _routeData.user)]]'
      ></ha-user-editor>
    </template>
`}static get properties(){return{hass:Object,route:{type:Object,observer:"_checkRoute"},_routeData:Object,_user:{type:Object,value:null},_users:{type:Array,value:null}}}ready(){super.ready(),this._loadData(),this.addEventListener("reload-users",()=>this._loadData())}_handlePickUser(e){this._user=e.detail.user}_checkRoute(e){e&&"/users"===e.path.substr(0,6)&&(this.fire("iron-resize"),this._debouncer=s.a.debounce(this._debouncer,r.d.after(0),()=>{"/users"===e.path&&this.navigate("/config/users/picker",!0)}))}_computeUser(e,t){return e&&e.filter(e=>e.id===t)[0]}_equals(e,t){return e===t}async _loadData(){this._users=await this.hass.callWS({type:"config/auth/list"})}})}}]);
//# sourceMappingURL=cf372946095cae18176f.chunk.js.map