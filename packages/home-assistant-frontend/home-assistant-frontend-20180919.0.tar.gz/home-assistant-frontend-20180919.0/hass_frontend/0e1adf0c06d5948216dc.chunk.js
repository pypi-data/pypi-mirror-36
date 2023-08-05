/*! For license information please see 0e1adf0c06d5948216dc.chunk.js.LICENSE */
(window.webpackJsonp=window.webpackJsonp||[]).push([[52],{197:function(e,t,a){"use strict";a(2),a(26),a(30),a(43);var o=a(3),i=a(0);Object(o.a)({_template:i["a"]`
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
`,is:"paper-item-body"})},199:function(e,t,a){"use strict";var o=a(0),i=a(4);a(121),customElements.define("ha-config-section",class extends i.a{static get template(){return o["a"]`
    <style include="iron-flex ha-style">
      .content {
        padding: 28px 20px 0;
        max-width: 1040px;
        margin: 0 auto;
      }

      .header {
        @apply --paper-font-display1;
        opacity: var(--dark-primary-opacity);
      }

      .together {
        margin-top: 32px;
      }

      .intro {
        @apply --paper-font-subhead;
        width: 100%;
        max-width: 400px;
        margin-right: 40px;
        opacity: var(--dark-primary-opacity);
      }

      .panel {
        margin-top: -24px;
      }

      .panel ::slotted(*) {
        margin-top: 24px;
        display: block;
      }

      .narrow.content {
        max-width: 640px;
      }
      .narrow .together {
        margin-top: 20px;
      }
      .narrow .header {
        @apply --paper-font-headline;
      }
      .narrow .intro {
        font-size: 14px;
        padding-bottom: 20px;
        margin-right: 0;
        max-width: 500px;
      }
    </style>
    <div class$="[[computeContentClasses(isWide)]]">
      <div class="header"><slot name="header"></slot></div>
      <div class$="[[computeClasses(isWide)]]">
        <div class="intro">
          <slot name="introduction"></slot>
        </div>
        <div class="panel flex-auto">
          <slot></slot>
        </div>
      </div>
    </div>
`}static get properties(){return{hass:{type:Object},narrow:{type:Boolean},showMenu:{type:Boolean,value:!1},isWide:{type:Boolean,value:!1}}}computeContentClasses(e){return e?"content ":"content narrow"}computeClasses(e){return"together layout "+(e?"horizontal":"vertical narrow")}})},627:function(e,t,a){"use strict";a.r(t),a(155),a(154),a(122),a(75),a(153),a(197),a(120);var o=a(0),i=a(4),n=(a(135),a(199),a(81)),r=a(13),p=a(136);const s=["core","customize"];customElements.define("ha-config-navigation",class extends(Object(r.a)(Object(n.a)(i.a))){static get template(){return o["a"]`
  <style include="iron-flex">
    paper-card {
      display: block;
    }
    paper-item {
      cursor: pointer;
    }
  </style>
  <paper-card>
    <template is="dom-repeat" items="[[pages]]">
      <template is="dom-if" if="[[_computeLoaded(hass, item)]]">
        <paper-item on-click="_navigate">
          <paper-item-body two-line="">
            [[_computeCaption(item, localize)]]
            <div secondary="">[[_computeDescription(item, localize)]]</div>
          </paper-item-body>
          <iron-icon icon="hass:chevron-right"></iron-icon>
        </paper-item>
      </template>
    </template>
  </paper-card>
`}static get properties(){return{hass:{type:Object},pages:{type:Array,value:["core","customize","automation","script","zwave"]}}}_computeLoaded(e,t){return s.includes(t)||Object(p.a)(e,t)}_computeCaption(e,t){return t(`ui.panel.config.${e}.caption`)}_computeDescription(e,t){return t(`ui.panel.config.${e}.description`)}_navigate(e){this.navigate("/config/"+e.model.item)}}),customElements.define("ha-config-dashboard",class extends(Object(n.a)(Object(r.a)(i.a))){static get template(){return o["a"]`
    <style include="iron-flex ha-style">
      .content {
        padding-bottom: 32px;
      }
      paper-card {
        display: block;
      }
      a {
        text-decoration: none;
        color: var(--primary-text-color);
      }
    </style>

    <app-header-layout has-scrolling-region="">
      <app-header slot="header" fixed="">
        <app-toolbar>
          <ha-menu-button narrow="[[narrow]]" show-menu="[[showMenu]]"></ha-menu-button>
          <div main-title="">[[localize('panel.configuration')]]</div>
        </app-toolbar>
      </app-header>

      <div class="content">
        <ha-config-section is-wide="[[isWide]]">
          <span slot="header">[[localize('ui.panel.config.header')]]</span>
          <span slot="introduction">[[localize('ui.panel.config.introduction')]]</span>

          <template is="dom-if" if="[[computeIsLoaded(hass, 'cloud')]]">
            <paper-card>
              <a href='/config/cloud' tabindex="-1">
                <paper-item on-click="_navigate">
                  <paper-item-body two-line="">
                    Home Assistant Cloud
                    <template is="dom-if" if="[[account]]">
                      <div secondary="">Logged in as [[account.email]]</div>
                    </template>
                    <template is="dom-if" if="[[!account]]">
                      <div secondary="">Not logged in</div>
                    </template>
                  </paper-item-body>
                  <iron-icon icon="hass:chevron-right"></iron-icon>
                </paper-item>
              </paper-card>
            </a>
          </template>

          <paper-card>
            <a href='/config/integrations/dashboard' tabindex="-1">
              <paper-item>
                <paper-item-body two-line>
                  Integrations
                  <div secondary>Manage connected devices and services</div>
                </paper-item-body>
                <iron-icon icon="hass:chevron-right"></iron-icon>
              </paper-item>
            </a>

            <a href='/config/users' tabindex="-1">
              <paper-item>
                <paper-item-body two-line>
                  [[localize('ui.panel.config.users.caption')]]
                  <div secondary>
                    [[localize('ui.panel.config.users.description')]]
                  </div>
                </paper-item-body>
                <iron-icon icon="hass:chevron-right"></iron-icon>
              </paper-item>
            </a>
          </paper-card>

          <ha-config-navigation hass="[[hass]]"></ha-config-navigation>
        </ha-config-section>
      </div>
    </app-header-layout>
`}static get properties(){return{hass:Object,isWide:Boolean,account:Object,narrow:Boolean,showMenu:Boolean}}computeIsLoaded(e,t){return Object(p.a)(e,t)}})}}]);
//# sourceMappingURL=0e1adf0c06d5948216dc.chunk.js.map