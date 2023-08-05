/*! For license information please see b7d11bc701419ef0dfc5.chunk.js.LICENSE */
(window.webpackJsonp=window.webpackJsonp||[]).push([[49],{200:function(e,t,a){"use strict";a(2),a(27),a(30),a(43);var r=a(3),s=a(0);Object(r.a)({_template:s["a"]`
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
`,is:"paper-item-body"})},207:function(e,t,a){"use strict";a(157),a(156),a(124),a(63);var r=a(0),s=a(4);customElements.define("hass-subpage",class extends s.a{static get template(){return r["a"]`
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
`}static get properties(){return{header:String}}_backTapped(){history.back()}})},243:function(e,t,a){"use strict";a(2),a(27),a(76);var r=a(60),s=(a(65),a(48),a(30),a(3));const n=document.createElement("template");n.setAttribute("style","display: none;"),n.innerHTML='<dom-module id="paper-fab">\n  <template strip-whitespace="">\n    <style include="paper-material-styles">\n      :host {\n        @apply --layout-vertical;\n        @apply --layout-center-center;\n\n        background: var(--paper-fab-background, var(--accent-color));\n        border-radius: 50%;\n        box-sizing: border-box;\n        color: var(--text-primary-color);\n        cursor: pointer;\n        height: 56px;\n        min-width: 0;\n        outline: none;\n        padding: 16px;\n        position: relative;\n        -moz-user-select: none;\n        -ms-user-select: none;\n        -webkit-user-select: none;\n        user-select: none;\n        width: 56px;\n        z-index: 0;\n\n        /* NOTE: Both values are needed, since some phones require the value `transparent`. */\n        -webkit-tap-highlight-color: rgba(0,0,0,0);\n        -webkit-tap-highlight-color: transparent;\n\n        @apply --paper-fab;\n      }\n\n      [hidden] {\n        display: none !important;\n      }\n\n      :host([mini]) {\n        width: 40px;\n        height: 40px;\n        padding: 8px;\n\n        @apply --paper-fab-mini;\n      }\n\n      :host([disabled]) {\n        color: var(--paper-fab-disabled-text, var(--paper-grey-500));\n        background: var(--paper-fab-disabled-background, var(--paper-grey-300));\n\n        @apply --paper-fab-disabled;\n      }\n\n      iron-icon {\n        @apply --paper-fab-iron-icon;\n      }\n\n      span {\n        width: 100%;\n        white-space: nowrap;\n        overflow: hidden;\n        text-overflow: ellipsis;\n        text-align: center;\n\n        @apply --paper-fab-label;\n      }\n\n      :host(.keyboard-focus) {\n        background: var(--paper-fab-keyboard-focus-background, var(--paper-pink-900));\n      }\n\n      :host([elevation="1"]) {\n        @apply --paper-material-elevation-1;\n      }\n\n      :host([elevation="2"]) {\n        @apply --paper-material-elevation-2;\n      }\n\n      :host([elevation="3"]) {\n        @apply --paper-material-elevation-3;\n      }\n\n      :host([elevation="4"]) {\n        @apply --paper-material-elevation-4;\n      }\n\n      :host([elevation="5"]) {\n        @apply --paper-material-elevation-5;\n      }\n    </style>\n\n    <iron-icon id="icon" hidden$="{{!_computeIsIconFab(icon, src)}}" src="[[src]]" icon="[[icon]]"></iron-icon>\n    <span hidden$="{{_computeIsIconFab(icon, src)}}">{{label}}</span>\n  </template>\n\n  \n</dom-module>',document.head.appendChild(n.content),Object(s.a)({is:"paper-fab",behaviors:[r.a],properties:{src:{type:String,value:""},icon:{type:String,value:""},mini:{type:Boolean,value:!1,reflectToAttribute:!0},label:{type:String,observer:"_labelChanged"}},_labelChanged:function(){this.setAttribute("aria-label",this.label)},_computeIsIconFab:function(e,t){return e.length>0||t.length>0}})},392:function(e,t,a){"use strict";a.r(t),a(91);var r=a(8),s=a(15),n=a(0),i=a(4),o=a(82),p=(a(243),a(121),a(155),a(200),a(207),a(13)),l=a(14);let d=!1;customElements.define("ha-user-picker",class extends(Object(l.a)(Object(o.a)(Object(p.a)(i.a)))){static get template(){return n["a"]`
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
`}static get properties(){return{hass:Object,users:Array}}connectedCallback(){super.connectedCallback(),d||(d=!0,this.fire("register-dialog",{dialogShowEvent:"show-add-user",dialogTag:"ha-dialog-add-user",dialogImport:()=>a.e(46).then(a.bind(null,653))}))}_withDefault(e,t){return e||t}_computeUrl(e){return`/config/users/${e.id}`}_addUser(){this.fire("show-add-user",{hass:this.hass,dialogClosedCallback:async({userId:e})=>{this.fire("reload-users"),e&&this.navigate(`/config/users/${e}`)}})}}),a(55),customElements.define("ha-user-editor",class extends(Object(l.a)(Object(o.a)(Object(p.a)(i.a)))){static get template(){return n["a"]`
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
`}static get properties(){return{hass:Object,user:Object}}_computeName(e){return e&&(e.name||"Unnamed user")}async _deleteUser(e){if(confirm(`Are you sure you want to delete ${this._computeName(this.user)}`)){try{await this.hass.callWS({type:"config/auth/delete",user_id:this.user.id})}catch(e){return void alert(e.code)}this.fire("reload-users"),this.navigate("/config/users")}else e.target.blur()}}),customElements.define("ha-config-users",class extends(Object(o.a)(i.a)){static get template(){return n["a"]`
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
`}static get properties(){return{hass:Object,route:{type:Object,observer:"_checkRoute"},_routeData:Object,_user:{type:Object,value:null},_users:{type:Array,value:null}}}ready(){super.ready(),this._loadData(),this.addEventListener("reload-users",()=>this._loadData())}_handlePickUser(e){this._user=e.detail.user}_checkRoute(e){e&&"/users"===e.path.substr(0,6)&&(this.fire("iron-resize"),this._debouncer=s.a.debounce(this._debouncer,r.timeOut.after(0),()=>{"/users"===e.path&&this.navigate("/config/users/picker",!0)}))}_computeUser(e,t){return e&&e.filter(e=>e.id===t)[0]}_equals(e,t){return e===t}async _loadData(){this._users=await this.hass.callWS({type:"config/auth/list"})}})}}]);
//# sourceMappingURL=b7d11bc701419ef0dfc5.chunk.js.map