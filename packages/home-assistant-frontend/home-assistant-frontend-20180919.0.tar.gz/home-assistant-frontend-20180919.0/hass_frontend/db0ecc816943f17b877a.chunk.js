/*! For license information please see db0ecc816943f17b877a.chunk.js.LICENSE */
(window.webpackJsonp=window.webpackJsonp||[]).push([[49],{197:function(t,e,i){"use strict";i(2),i(26),i(30),i(43);var a=i(3),n=i(0);Object(a.a)({_template:n["a"]`
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
`,is:"paper-item-body"})},199:function(t,e,i){"use strict";var a=i(0),n=i(4);i(121),customElements.define("ha-config-section",class extends n.a{static get template(){return a["a"]`
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
`}static get properties(){return{hass:{type:Object},narrow:{type:Boolean},showMenu:{type:Boolean,value:!1},isWide:{type:Boolean,value:!1}}}computeContentClasses(t){return t?"content ":"content narrow"}computeClasses(t){return"together layout "+(t?"horizontal":"vertical narrow")}})},207:function(t,e,i){"use strict";i(155),i(154),i(122),i(62);var a=i(0),n=i(4);customElements.define("hass-subpage",class extends n.a{static get template(){return a["a"]`
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
`}static get properties(){return{header:String}}_backTapped(){history.back()}})},219:function(t,e,i){"use strict";i(2),i(26),i(43),i(130);var a=i(3),n=i(0),o=i(98);Object(a.a)({_template:n["a"]`
    <style include="paper-item-shared-styles"></style>
    <style>
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
        @apply --paper-icon-item;
      }

      .content-icon {
        @apply --layout-horizontal;
        @apply --layout-center;

        width: var(--paper-item-icon-width, 56px);
        @apply --paper-item-icon;
      }
    </style>

    <div id="contentIcon" class="content-icon">
      <slot name="item-icon"></slot>
    </div>
    <slot></slot>
`,is:"paper-icon-item",behaviors:[o.a]})},257:function(t,e,i){"use strict";i(2);var a=i(3),n=i(1),o=i(0);Object(a.a)({_template:o["a"]`
    <style>
      :host {
        display: block;
        position: absolute;
        outline: none;
        z-index: 1002;
        -moz-user-select: none;
        -ms-user-select: none;
        -webkit-user-select: none;
        user-select: none;
        cursor: default;
      }

      #tooltip {
        display: block;
        outline: none;
        @apply --paper-font-common-base;
        font-size: 10px;
        line-height: 1;
        background-color: var(--paper-tooltip-background, #616161);
        color: var(--paper-tooltip-text-color, white);
        padding: 8px;
        border-radius: 2px;
        @apply --paper-tooltip;
      }

      @keyframes keyFrameScaleUp {
        0% {
          transform: scale(0.0);
        }
        100% {
          transform: scale(1.0);
        }
      }

      @keyframes keyFrameScaleDown {
        0% {
          transform: scale(1.0);
        }
        100% {
          transform: scale(0.0);
        }
      }

      @keyframes keyFrameFadeInOpacity {
        0% {
          opacity: 0;
        }
        100% {
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
      }

      @keyframes keyFrameFadeOutOpacity {
        0% {
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
        100% {
          opacity: 0;
        }
      }

      @keyframes keyFrameSlideDownIn {
        0% {
          transform: translateY(-2000px);
          opacity: 0;
        }
        10% {
          opacity: 0.2;
        }
        100% {
          transform: translateY(0);
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
      }

      @keyframes keyFrameSlideDownOut {
        0% {
          transform: translateY(0);
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
        10% {
          opacity: 0.2;
        }
        100% {
          transform: translateY(-2000px);
          opacity: 0;
        }
      }

      .fade-in-animation {
        opacity: 0;
        animation-delay: var(--paper-tooltip-delay-in, 500ms);
        animation-name: keyFrameFadeInOpacity;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-in, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .fade-out-animation {
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 0ms);
        animation-name: keyFrameFadeOutOpacity;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .scale-up-animation {
        transform: scale(0);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-in, 500ms);
        animation-name: keyFrameScaleUp;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-in, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .scale-down-animation {
        transform: scale(1);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameScaleDown;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .slide-down-animation {
        transform: translateY(-2000px);
        opacity: 0;
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameSlideDownIn;
        animation-iteration-count: 1;
        animation-timing-function: cubic-bezier(0.0, 0.0, 0.2, 1);
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .slide-down-animation-out {
        transform: translateY(0);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameSlideDownOut;
        animation-iteration-count: 1;
        animation-timing-function: cubic-bezier(0.4, 0.0, 1, 1);
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .cancel-animation {
        animation-delay: -30s !important;
      }

      /* Thanks IE 10. */

      .hidden {
        display: none !important;
      }
    </style>

    <div id="tooltip" class="hidden">
      <slot></slot>
    </div>
`,is:"paper-tooltip",hostAttributes:{role:"tooltip",tabindex:-1},properties:{for:{type:String,observer:"_findTarget"},manualMode:{type:Boolean,value:!1,observer:"_manualModeChanged"},position:{type:String,value:"bottom"},fitToVisibleBounds:{type:Boolean,value:!1},offset:{type:Number,value:14},marginTop:{type:Number,value:14},animationDelay:{type:Number,value:500,observer:"_delayChange"},animationEntry:{type:String,value:""},animationExit:{type:String,value:""},animationConfig:{type:Object,value:function(){return{entry:[{name:"fade-in-animation",node:this,timing:{delay:0}}],exit:[{name:"fade-out-animation",node:this}]}}},_showing:{type:Boolean,value:!1}},listeners:{webkitAnimationEnd:"_onAnimationEnd"},get target(){var t=Object(n.b)(this).parentNode,e=Object(n.b)(this).getOwnerRoot();return this.for?Object(n.b)(e).querySelector("#"+this.for):t.nodeType==Node.DOCUMENT_FRAGMENT_NODE?e.host:t},attached:function(){this._findTarget()},detached:function(){this.manualMode||this._removeListeners()},playAnimation:function(t){"entry"===t?this.show():"exit"===t&&this.hide()},cancelAnimation:function(){this.$.tooltip.classList.add("cancel-animation")},show:function(){if(!this._showing){if(""===Object(n.b)(this).textContent.trim()){for(var t=!0,e=Object(n.b)(this).getEffectiveChildNodes(),i=0;i<e.length;i++)if(""!==e[i].textContent.trim()){t=!1;break}if(t)return}this._showing=!0,this.$.tooltip.classList.remove("hidden"),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.updatePosition(),this._animationPlaying=!0,this.$.tooltip.classList.add(this._getAnimationType("entry"))}},hide:function(){if(this._showing){if(this._animationPlaying)return this._showing=!1,void this._cancelAnimation();this._onAnimationFinish(),this._showing=!1,this._animationPlaying=!0}},updatePosition:function(){if(this._target&&this.offsetParent){var t=this.offset;14!=this.marginTop&&14==this.offset&&(t=this.marginTop);var e,i,a=this.offsetParent.getBoundingClientRect(),n=this._target.getBoundingClientRect(),o=this.getBoundingClientRect(),s=(n.width-o.width)/2,r=(n.height-o.height)/2,p=n.left-a.left,l=n.top-a.top;switch(this.position){case"top":e=p+s,i=l-o.height-t;break;case"bottom":e=p+s,i=l+n.height+t;break;case"left":e=p-o.width-t,i=l+r;break;case"right":e=p+n.width+t,i=l+r}this.fitToVisibleBounds?(a.left+e+o.width>window.innerWidth?(this.style.right="0px",this.style.left="auto"):(this.style.left=Math.max(0,e)+"px",this.style.right="auto"),a.top+i+o.height>window.innerHeight?(this.style.bottom=a.height-l+t+"px",this.style.top="auto"):(this.style.top=Math.max(-a.top,i)+"px",this.style.bottom="auto")):(this.style.left=e+"px",this.style.top=i+"px")}},_addListeners:function(){this._target&&(this.listen(this._target,"mouseenter","show"),this.listen(this._target,"focus","show"),this.listen(this._target,"mouseleave","hide"),this.listen(this._target,"blur","hide"),this.listen(this._target,"tap","hide")),this.listen(this.$.tooltip,"animationend","_onAnimationEnd"),this.listen(this,"mouseenter","hide")},_findTarget:function(){this.manualMode||this._removeListeners(),this._target=this.target,this.manualMode||this._addListeners()},_delayChange:function(t){500!==t&&this.updateStyles({"--paper-tooltip-delay-in":t+"ms"})},_manualModeChanged:function(){this.manualMode?this._removeListeners():this._addListeners()},_cancelAnimation:function(){this.$.tooltip.classList.remove(this._getAnimationType("entry")),this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.add("hidden")},_onAnimationFinish:function(){this._showing&&(this.$.tooltip.classList.remove(this._getAnimationType("entry")),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.add(this._getAnimationType("exit")))},_onAnimationEnd:function(){this._animationPlaying=!1,this._showing||(this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.$.tooltip.classList.add("hidden"))},_getAnimationType:function(t){if("entry"===t&&""!==this.animationEntry)return this.animationEntry;if("exit"===t&&""!==this.animationExit)return this.animationExit;if(this.animationConfig[t]&&"string"==typeof this.animationConfig[t][0].name){if(this.animationConfig[t][0].timing&&this.animationConfig[t][0].timing.delay&&0!==this.animationConfig[t][0].timing.delay){var e=this.animationConfig[t][0].timing.delay;"entry"===t?this.updateStyles({"--paper-tooltip-delay-in":e+"ms"}):"exit"===t&&this.updateStyles({"--paper-tooltip-delay-out":e+"ms"})}return this.animationConfig[t][0].name}},_removeListeners:function(){this._target&&(this.unlisten(this._target,"mouseenter","show"),this.unlisten(this._target,"focus","show"),this.unlisten(this._target,"mouseleave","hide"),this.unlisten(this._target,"blur","hide"),this.unlisten(this._target,"tap","hide")),this.unlisten(this.$.tooltip,"animationend","_onAnimationEnd"),this.unlisten(this,"mouseenter","hide")}})},622:function(t,e,i){"use strict";i.r(e),i(89);var a=i(0),n=i(4),o=i(15),s=i(8),r=(i(31),i(257),i(55),i(153),i(75),i(120),i(197),i(87),i(114));customElements.define("ha-state-icon",class extends n.a{static get template(){return a["a"]`<ha-icon icon="[[computeIcon(stateObj)]]"></ha-icon>`}static get properties(){return{stateObj:{type:Object}}}computeIcon(t){return Object(r.a)(t)}}),i(207),i(121),i(199);var p=i(14),l=i(13),c=i(28);let d=!1;customElements.define("ha-config-entries-dashboard",class extends(Object(l.a)(Object(p.a)(n.a))){static get template(){return a["a"]`
  <style include="iron-flex ha-style">
    paper-button {
      color: var(--primary-color);
      font-weight: 500;
      top: 3px;
      margin-right: -.57em;
    }
    paper-card:last-child {
      margin-top: 12px;
    }
    .config-entry-row {
      display: flex;
      padding: 0 16px;
    }
    ha-state-icon {
      cursor: pointer;
    }
    a paper-item {
      color: var(--primary-text-color);
    }
  </style>

  <hass-subpage header="Integrations">
    <template is="dom-if" if="[[progress.length]]">
      <ha-config-section>
        <span slot="header">Discovered</span>
        <paper-card>
          <template is="dom-repeat" items="[[progress]]">
            <div class="config-entry-row">
              <paper-item-body>
                [[_computeIntegrationTitle(localize, item.handler)]]
              </paper-item-body>
              <paper-button on-click="_continueFlow">Configure</paper-button>
            </div>
          </template>
        </paper-card>
      </ha-config-section>
    </template>

    <ha-config-section>
      <span slot="header">Configured</span>
      <paper-card>
        <template is="dom-if" if="[[!entries.length]]">
          <div class="config-entry-row">
            <paper-item-body two-line>
              <div>Nothing configured yet</div>
            </paper-item-body>
          </div>
        </template>
        <template is="dom-repeat" items="[[entries]]">
          <a href='/config/integrations/[[item.entry_id]]'>
            <paper-item>
              <paper-item-body two-line>
                <div>[[_computeIntegrationTitle(localize, item.domain)]]: [[item.title]]</div>
                <div secondary>
                  <template is='dom-repeat' items='[[_computeConfigEntryEntities(hass, item, entities)]]'>
                    <span>
                      <ha-state-icon state-obj='[[item]]' on-click='_handleMoreInfo'></ha-state-icon>
                      <paper-tooltip position="bottom">[[_computeStateName(item)]]</paper-tooltip>
                    </span>
                  </template>
                </div>
              </paper-item-body>
              <iron-icon icon='hass:chevron-right'></iron-icon>
            </paper-item>
          </a>
        </template>
      </paper-card>
    </ha-config-section>

    <ha-config-section>
      <span slot="header">Set up a new integration</span>
      <paper-card>
        <template is="dom-repeat" items="[[handlers]]">
          <div class="config-entry-row">
            <paper-item-body>
              [[_computeIntegrationTitle(localize, item)]]
            </paper-item-body>
            <paper-button on-click="_createFlow">Configure</paper-button>
          </div>
        </template>
      </paper-card>
    </ha-config-section>
  </hass-subpage>
`}static get properties(){return{hass:Object,isWide:Boolean,entries:Array,entities:Array,progress:Array,handlers:Array}}connectedCallback(){super.connectedCallback(),d||(d=!0,this.fire("register-dialog",{dialogShowEvent:"show-config-flow",dialogTag:"ha-config-flow",dialogImport:()=>i.e(59).then(i.bind(null,650))}))}_createFlow(t){this.fire("show-config-flow",{hass:this.hass,newFlowForHandler:t.model.item,dialogClosedCallback:()=>this.fire("hass-reload-entries")})}_continueFlow(t){this.fire("show-config-flow",{hass:this.hass,continueFlowId:t.model.item.flow_id,dialogClosedCallback:()=>this.fire("hass-reload-entries")})}_computeIntegrationTitle(t,e){return t(`component.${e}.config.title`)}_computeConfigEntryEntities(t,e,i){if(!i)return[];const a=[];return i.forEach(i=>{i.config_entry_id===e.entry_id&&i.entity_id in t.states&&a.push(t.states[i.entity_id])}),a}_computeStateName(t){return Object(c.a)(t)}_handleMoreInfo(t){this.fire("hass-more-info",{entityId:t.model.item.entity_id})}}),i(126);var m=(t,e)=>t<e?-1:t>e?1:0;function h(t,e){if(e.name)return e.name;const i=t.states[e.entity_id];return i?Object(c.a)(i):null}i(219),customElements.define("ha-device-card",class extends(Object(p.a)(n.a)){static get template(){return a["a"]`
    <style>
      paper-card {
        display: block;
        padding-bottom: 8px;
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
      .hub-info {
        margin-top: 8px;
      }
      paper-icon-item {
        cursor: pointer;
      }
      .manuf,
      .entity-id {
        color: var(--secondary-text-color);
      }
    </style>
    <paper-card heading='[[device.name]]'>
      <div class='card-content'>
      <!-- <h1>[[configEntry.title]] ([[_computeIntegrationTitle(localize, configEntry.domain)]])</h1> -->
        <div class='info'>
          <div class='model'>[[device.model]]</div>
          <div class='manuf'>by [[device.manufacturer]]</div>
        </div>
        <template is='dom-if' if='[[device.hub_device_id]]'>
          <div class='hub-info'>
            Connected via
            <span class='hub'>[[_computeDeviceName(devices, device.hub_device_id)]]</span>
          </div>
        </template>
      </div>

      <template is='dom-repeat' items='[[_computeDeviceEntities(hass, device, entities)]]' as='entity'>
        <paper-icon-item on-click='_openMoreInfo'>
          <state-badge
            state-obj="[[_computeStateObj(entity, hass)]]"
            slot='item-icon'
          ></state-badge>
          <paper-item-body>
            <div class='name'>[[_computeEntityName(entity, hass)]]</div>
            <div class='secondary entity-id'>[[entity.entity_id]]</div>
          </paper-item-body>
        </paper-icon-item>
      </template>
    </paper-card>

    `}static get properties(){return{device:Object,devices:Array,entities:Array,hass:Object,_childDevices:{type:Array,computed:"_computeChildDevices(device, devices)"}}}_computeChildDevices(t,e){return e.filter(e=>e.hub_device_id===t.id).sort((t,e)=>m(t.name,e.name))}_computeDeviceEntities(t,e,i){return i.filter(t=>t.device_id===e.id).sort((e,i)=>m(h(t,e)||`zzz${e.entity_id}`,h(t,i)||`zzz${i.entity_id}`))}_computeStateObj(t,e){return e.states[t.entity_id]}_computeEntityName(t,e){return h(e,t)||"(entity unavailable)"}_computeDeviceName(t,e){const i=t.find(t=>t.id===e);return i?i.name:"(device unavailable)"}_openMoreInfo(t){this.fire("hass-more-info",{entityId:t.model.entity.entity_id})}});var u=i(81);customElements.define("ha-config-entry-page",class extends(Object(u.a)(Object(p.a)(n.a))){static get template(){return a["a"]`
  <style>
    .content {
      display: flex;
      flex-wrap: wrap;
      padding: 4px;
      justify-content: center;
    }
    ha-device-card {
      flex: 1;
      min-width: 300px;
      max-width: 300px;
      margin: 8px;

    }
    @media(max-width: 600px) {
      ha-device-card {
        max-width: 500px;
        margin-left: auto;
        margin-right: auto;
      }
    }
  </style>
  <hass-subpage header='[[configEntry.title]]'>
    <paper-icon-button
      slot='toolbar-icon'
      icon='hass:delete'
      on-click='_removeEntry'
    ></paper-icon-button>
    <div class='content'>
      <template is='dom-repeat' items='[[_computeConfigEntryDevices(configEntry, devices)]]' as='device'>
        <ha-device-card
          hass='[[hass]]'
          devices='[[devices]]'
          device='[[device]]'
          entities='[[entities]]'
        ></ha-device-card>
      </template>
    </div>
  </hass-subpage>
`}static get properties(){return{hass:Object,isWide:Boolean,configEntry:{type:Object,value:null},_entries:Array,_entities:Array}}_computeConfigEntryDevices(t,e){return e?e.filter(e=>e.config_entries.includes(t.entry_id)).sort((t,e)=>!!t.hub_device_id-!!e.hub_device_id||m(t.name,e.name)):[]}_removeEntry(){if(!confirm("Are you sure you want to delete this integration?"))return;const t=this.configEntry.entry_id;this.hass.callApi("delete",`config/config_entries/entry/${t}`).then(t=>{this.fire("hass-reload-entries"),t.require_restart&&alert("Restart Home Assistant to finish removing this integration"),this.navigate("/config/integrations/dashboard",!0)})}}),customElements.define("ha-config-entries",class extends(Object(u.a)(n.a)){static get template(){return a["a"]`
  <app-route route="[[route]]" pattern="/integrations/:page" data="{{_routeData}}" tail="{{_routeTail}}"></app-route>

  <template is='dom-if' if='[[_configEntry]]'>
    <ha-config-entry-page
      hass='[[hass]]'
      config-entry='[[_configEntry]]'
      entries='[[_entries]]'
      entities='[[_entities]]'
      devices='[[_devices]]'
    ></ha-config-entry-page>
  </template>
  <template is='dom-if' if='[[!_configEntry]]'>
    <ha-config-entries-dashboard
      hass='[[hass]]'
      entries='[[_entries]]'
      entities='[[_entities]]'
      handlers='[[_handlers]]'
      progress='[[_progress]]'
    ></ha-config-entries-dashboard>
  </template>
`}static get properties(){return{hass:Object,isWide:Boolean,route:Object,_configEntry:{type:Object,computed:"_computeConfigEntry(_routeData, _entries)"},_entries:Array,_entities:Array,_devices:Array,_progress:Array,_handlers:Array,_routeData:Object,_routeTail:Object}}ready(){super.ready(),this._loadData(),this.addEventListener("hass-reload-entries",()=>this._loadData())}connectedCallback(){super.connectedCallback(),this.hass.connection.subscribeEvents(()=>{this._debouncer=o.a.debounce(this._debouncer,s.d.after(500),()=>this._loadData())},"config_entry_discovered").then(t=>{this._unsubEvents=t})}disconnectedCallback(){super.disconnectedCallback(),this._unsubEvents&&this._unsubEvents()}_loadData(){this.hass.callApi("get","config/config_entries/entry").then(t=>{this._entries=t.sort((t,e)=>m(t.title,e.title))}),this.hass.callApi("get","config/config_entries/flow").then(t=>{this._progress=t}),this.hass.callApi("get","config/config_entries/flow_handlers").then(t=>{this._handlers=t}),this.hass.callWS({type:"config/entity_registry/list"}).then(t=>{this._entities=t}),this.hass.callWS({type:"config/device_registry/list"}).then(t=>{this._devices=t})}_computeConfigEntry(t,e){return!!e&&!!t&&e.find(e=>e.entry_id===t.page)}})}}]);
//# sourceMappingURL=db0ecc816943f17b877a.chunk.js.map