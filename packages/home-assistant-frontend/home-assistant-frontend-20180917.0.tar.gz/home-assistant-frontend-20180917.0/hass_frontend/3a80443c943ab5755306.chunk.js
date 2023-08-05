/*! For license information please see 3a80443c943ab5755306.chunk.js.LICENSE */
(window.webpackJsonp=window.webpackJsonp||[]).push([[52],{158:function(e,t,i){"use strict";i(2),i(30);var a=i(90),n=i(3),o=i(36),r=i(40);const s=document.createElement("template");s.setAttribute("style","display: none;"),s.innerHTML='<dom-module id="paper-checkbox">\n  <template strip-whitespace="">\n    <style>\n      :host {\n        display: inline-block;\n        white-space: nowrap;\n        cursor: pointer;\n        --calculated-paper-checkbox-size: var(--paper-checkbox-size, 18px);\n        /* -1px is a sentinel for the default and is replaced in `attached`. */\n        --calculated-paper-checkbox-ink-size: var(--paper-checkbox-ink-size, -1px);\n        @apply --paper-font-common-base;\n        line-height: 0;\n        -webkit-tap-highlight-color: transparent;\n      }\n\n      :host([hidden]) {\n        display: none !important;\n      }\n\n      :host(:focus) {\n        outline: none;\n      }\n\n      .hidden {\n        display: none;\n      }\n\n      #checkboxContainer {\n        display: inline-block;\n        position: relative;\n        width: var(--calculated-paper-checkbox-size);\n        height: var(--calculated-paper-checkbox-size);\n        min-width: var(--calculated-paper-checkbox-size);\n        margin: var(--paper-checkbox-margin, initial);\n        vertical-align: var(--paper-checkbox-vertical-align, middle);\n        background-color: var(--paper-checkbox-unchecked-background-color, transparent);\n      }\n\n      #ink {\n        position: absolute;\n\n        /* Center the ripple in the checkbox by negative offsetting it by\n         * (inkWidth - rippleWidth) / 2 */\n        top: calc(0px - (var(--calculated-paper-checkbox-ink-size) - var(--calculated-paper-checkbox-size)) / 2);\n        left: calc(0px - (var(--calculated-paper-checkbox-ink-size) - var(--calculated-paper-checkbox-size)) / 2);\n        width: var(--calculated-paper-checkbox-ink-size);\n        height: var(--calculated-paper-checkbox-ink-size);\n        color: var(--paper-checkbox-unchecked-ink-color, var(--primary-text-color));\n        opacity: 0.6;\n        pointer-events: none;\n      }\n\n      #ink:dir(rtl) {\n        right: calc(0px - (var(--calculated-paper-checkbox-ink-size) - var(--calculated-paper-checkbox-size)) / 2);\n        left: auto;\n      }\n\n      #ink[checked] {\n        color: var(--paper-checkbox-checked-ink-color, var(--primary-color));\n      }\n\n      #checkbox {\n        position: relative;\n        box-sizing: border-box;\n        height: 100%;\n        border: solid 2px;\n        border-color: var(--paper-checkbox-unchecked-color, var(--primary-text-color));\n        border-radius: 2px;\n        pointer-events: none;\n        -webkit-transition: background-color 140ms, border-color 140ms;\n        transition: background-color 140ms, border-color 140ms;\n      }\n\n      /* checkbox checked animations */\n      #checkbox.checked #checkmark {\n        -webkit-animation: checkmark-expand 140ms ease-out forwards;\n        animation: checkmark-expand 140ms ease-out forwards;\n      }\n\n      @-webkit-keyframes checkmark-expand {\n        0% {\n          -webkit-transform: scale(0, 0) rotate(45deg);\n        }\n        100% {\n          -webkit-transform: scale(1, 1) rotate(45deg);\n        }\n      }\n\n      @keyframes checkmark-expand {\n        0% {\n          transform: scale(0, 0) rotate(45deg);\n        }\n        100% {\n          transform: scale(1, 1) rotate(45deg);\n        }\n      }\n\n      #checkbox.checked {\n        background-color: var(--paper-checkbox-checked-color, var(--primary-color));\n        border-color: var(--paper-checkbox-checked-color, var(--primary-color));\n      }\n\n      #checkmark {\n        position: absolute;\n        width: 36%;\n        height: 70%;\n        border-style: solid;\n        border-top: none;\n        border-left: none;\n        border-right-width: calc(2/15 * var(--calculated-paper-checkbox-size));\n        border-bottom-width: calc(2/15 * var(--calculated-paper-checkbox-size));\n        border-color: var(--paper-checkbox-checkmark-color, white);\n        -webkit-transform-origin: 97% 86%;\n        transform-origin: 97% 86%;\n        box-sizing: content-box; /* protect against page-level box-sizing */\n      }\n\n      #checkmark:dir(rtl) {\n        -webkit-transform-origin: 50% 14%;\n        transform-origin: 50% 14%;\n      }\n\n      /* label */\n      #checkboxLabel {\n        position: relative;\n        display: inline-block;\n        vertical-align: middle;\n        padding-left: var(--paper-checkbox-label-spacing, 8px);\n        white-space: normal;\n        line-height: normal;\n        color: var(--paper-checkbox-label-color, var(--primary-text-color));\n        @apply --paper-checkbox-label;\n      }\n\n      :host([checked]) #checkboxLabel {\n        color: var(--paper-checkbox-label-checked-color, var(--paper-checkbox-label-color, var(--primary-text-color)));\n        @apply --paper-checkbox-label-checked;\n      }\n\n      #checkboxLabel:dir(rtl) {\n        padding-right: var(--paper-checkbox-label-spacing, 8px);\n        padding-left: 0;\n      }\n\n      #checkboxLabel[hidden] {\n        display: none;\n      }\n\n      /* disabled state */\n\n      :host([disabled]) #checkbox {\n        opacity: 0.5;\n        border-color: var(--paper-checkbox-unchecked-color, var(--primary-text-color));\n      }\n\n      :host([disabled][checked]) #checkbox {\n        background-color: var(--paper-checkbox-unchecked-color, var(--primary-text-color));\n        opacity: 0.5;\n      }\n\n      :host([disabled]) #checkboxLabel  {\n        opacity: 0.65;\n      }\n\n      /* invalid state */\n      #checkbox.invalid:not(.checked) {\n        border-color: var(--paper-checkbox-error-color, var(--error-color));\n      }\n    </style>\n\n    <div id="checkboxContainer">\n      <div id="checkbox" class$="[[_computeCheckboxClass(checked, invalid)]]">\n        <div id="checkmark" class$="[[_computeCheckmarkClass(checked)]]"></div>\n      </div>\n    </div>\n\n    <div id="checkboxLabel"><slot></slot></div>\n  </template>\n\n  \n</dom-module>',document.head.appendChild(s.content),Object(n.a)({is:"paper-checkbox",behaviors:[a.a],hostAttributes:{role:"checkbox","aria-checked":!1,tabindex:0},properties:{ariaActiveAttribute:{type:String,value:"aria-checked"}},attached:function(){Object(o.a)(this,function(){if("-1px"===this.getComputedStyleValue("--calculated-paper-checkbox-ink-size").trim()){var e=this.getComputedStyleValue("--calculated-paper-checkbox-size").trim(),t="px",i=e.match(/[A-Za-z]+$/);null!==i&&(t=i[0]);var a=parseFloat(e),n=8/3*a;"px"===t&&(n=Math.floor(n))%2!=a%2&&n++,this.updateStyles({"--paper-checkbox-ink-size":n+t})}})},_computeCheckboxClass:function(e,t){var i="";return e&&(i+="checked "),t&&(i+="invalid"),i},_computeCheckmarkClass:function(e){return e?"":"hidden"},_createRipple:function(){return this._rippleContainer=this.$.checkboxContainer,r.b._createRipple.call(this)}})},203:function(e,t,i){"use strict";var a=i(0),n=i(4);i(122),customElements.define("ha-config-section",class extends n.a{static get template(){return a["a"]`
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
`}static get properties(){return{hass:{type:Object},narrow:{type:Boolean},showMenu:{type:Boolean,value:!1},isWide:{type:Boolean,value:!1}}}computeContentClasses(e){return e?"content ":"content narrow"}computeClasses(e){return"together layout "+(e?"horizontal":"vertical narrow")}})},278:function(e,t,i){"use strict";const a={DOMAIN_DEVICE_CLASS:{binary_sensor:["battery","cold","connectivity","door","garage_door","gas","heat","light","lock","moisture","motion","moving","occupancy","opening","plug","power","presence","problem","safety","smoke","sound","vibration","window"],cover:["garage"],sensor:["battery","humidity","illuminance","temperature"]},UNKNOWN_TYPE:"json",ADD_TYPE:"key-value",TYPE_TO_TAG:{string:"ha-customize-string",json:"ha-customize-string",icon:"ha-customize-icon",boolean:"ha-customize-boolean",array:"ha-customize-array","key-value":"ha-customize-key-value"}};a.LOGIC_STATE_ATTRIBUTES=a.LOGIC_STATE_ATTRIBUTES||{entity_picture:void 0,friendly_name:{type:"string",description:"Name"},icon:{type:"icon"},emulated_hue:{type:"boolean",domains:["emulated_hue"]},emulated_hue_name:{type:"string",domains:["emulated_hue"]},haaska_hidden:void 0,haaska_name:void 0,homebridge_hidden:{type:"boolean"},homebridge_name:{type:"string"},supported_features:void 0,attribution:void 0,custom_ui_more_info:{type:"string"},custom_ui_state_card:{type:"string"},device_class:{type:"array",options:a.DOMAIN_DEVICE_CLASS,description:"Device class",domains:["binary_sensor","cover","sensor"]},hidden:{type:"boolean",description:"Hide from UI"},assumed_state:{type:"boolean",domains:["switch","light","cover","climate","fan","group"]},initial_state:{type:"string",domains:["automation"]},unit_of_measurement:{type:"string"}},t.a=a},323:function(e,t,i){"use strict";i.d(t,"a",function(){return n});var a=i(29);function n(e,t){const i=Object(a.a)(e),n=Object(a.a)(t);return i<n?-1:i>n?1:0}},324:function(e,t){const i=document.createElement("template");i.setAttribute("style","display: none;"),i.innerHTML='<dom-module id="ha-form-style">\n  <template>\n    <style>\n      .form-group {\n        @apply --layout-horizontal;\n        @apply --layout-center;\n        padding: 8px 16px;\n      }\n\n      .form-group label {\n        @apply --layout-flex-2;\n      }\n\n      .form-group .form-control {\n        @apply --layout-flex;\n      }\n\n      .form-group.vertical {\n        @apply --layout-vertical;\n        @apply --layout-start;\n      }\n\n      paper-dropdown-menu.form-control {\n        margin: -9px 0;\n      }\n    </style>\n  </template>\n</dom-module>',document.head.appendChild(i.content)},396:function(e,t,i){"use strict";i.r(t),i(157),i(156),i(124),i(63);var a=i(0),n=i(4),o=(i(122),i(203),i(55),i(155),i(125),i(121),i(123),i(126),i(29));customElements.define("ha-entity-config",class extends n.a{static get template(){return a["a"]`
    <style include="iron-flex ha-style">
      paper-card {
        display: block;
      }

      .device-picker {
        @apply --layout-horizontal;
        padding-bottom: 24px;
      }

      .form-placeholder {
        @apply --layout-vertical;
        @apply --layout-center-center;
        height: 96px;
      }

      [hidden]: {
        display: none;
      }

      .card-actions {
        @apply --layout-horizontal;
        @apply --layout-justified;
      }
    </style>
    <paper-card>
      <div class="card-content">
        <div class="device-picker">
          <paper-dropdown-menu label="[[label]]" class="flex" disabled="[[!entities.length]]">
            <paper-listbox slot="dropdown-content" selected="{{selectedEntity}}">
              <template is="dom-repeat" items="[[entities]]" as="state">
                <paper-item>[[computeSelectCaption(state)]]</paper-item>
              </template>
            </paper-listbox>
          </paper-dropdown-menu>
        </div>

        <div class="form-container">
          <template is="dom-if" if="[[computeShowPlaceholder(formState)]]">
            <div class="form-placeholder">
              <template is="dom-if" if="[[computeShowNoDevices(formState)]]">
                No entities found! :-(
              </template>

              <template is="dom-if" if="[[computeShowSpinner(formState)]]">
                <paper-spinner active="" alt="[[formState]]"></paper-spinner>
                [[formState]]
              </template>
            </div>
          </template>

          <div hidden$="[[!computeShowForm(formState)]]" id="form"></div>
        </div>
      </div>
      <div class="card-actions">
        <paper-button on-click="saveEntity" disabled="[[computeShowPlaceholder(formState)]]">SAVE</paper-button>
        <template is="dom-if" if="[[allowDelete]]">
          <paper-button class="warning" on-click="deleteEntity" disabled="[[computeShowPlaceholder(formState)]]">DELETE</paper-button>
        </template>
      </div>
    </paper-card>
`}static get properties(){return{hass:{type:Object,observer:"hassChanged"},label:{type:String,value:"Device"},entities:{type:Array,observer:"entitiesChanged"},allowDelete:{type:Boolean,value:!1},selectedEntity:{type:Number,value:-1,observer:"entityChanged"},formState:{type:String,value:"no-devices"},config:{type:Object}}}connectedCallback(){super.connectedCallback(),this.formEl=document.createElement(this.config.component),this.formEl.hass=this.hass,this.$.form.appendChild(this.formEl),this.entityChanged(this.selectedEntity)}computeSelectCaption(e){return this.config.computeSelectCaption?this.config.computeSelectCaption(e):Object(o.a)(e)}computeShowNoDevices(e){return"no-devices"===e}computeShowSpinner(e){return"loading"===e||"saving"===e}computeShowPlaceholder(e){return"editing"!==e}computeShowForm(e){return"editing"===e}hassChanged(e){this.formEl&&(this.formEl.hass=e)}entitiesChanged(e,t){if(0!==e.length)if(t){var i=t[this.selectedEntity].entity_id,a=e.findIndex(function(e){return e.entity_id===i});-1===a?this.selectedEntity=0:a!==this.selectedEntity&&(this.selectedEntity=a)}else this.selectedEntity=0;else this.formState="no-devices"}entityChanged(e){if(this.entities&&this.formEl){var t=this.entities[e];if(t){this.formState="loading";var i=this;this.formEl.loadEntity(t).then(function(){i.formState="editing"})}}}saveEntity(){this.formState="saving";var e=this;this.formEl.saveEntity().then(function(){e.formState="editing"})}});var r=i(278),s=i(25),c=(i(324),i(14));customElements.define("ha-customize-array",class extends(Object(c.a)(n.a)){static get template(){return a["a"]`
    <style>
      paper-dropdown-menu {
        margin: -9px 0;
      }
    </style>
    <paper-dropdown-menu label="[[item.description]]" disabled="[[item.secondary]]" selected-item-label="{{item.value}}" dynamic-align="">
      <paper-listbox slot="dropdown-content" selected="[[computeSelected(item)]]">
        <template is="dom-repeat" items="[[getOptions(item)]]" as="option">
          <paper-item>[[option]]</paper-item>
        </template>
      </paper-listbox>
    </paper-dropdown-menu>
`}static get properties(){return{item:{type:Object,notifies:!0}}}getOptions(e){const t=e.domain||"*",i=e.options[t]||e.options["*"];return i?i.sort():(this.item.type="string",this.fire("item-changed"),[])}computeSelected(e){return this.getOptions(e).indexOf(e.value)}}),i(158),customElements.define("ha-customize-boolean",class extends n.a{static get template(){return a["a"]`
    <paper-checkbox disabled="[[item.secondary]]" checked="{{item.value}}">
      [[item.description]]
    </paper-checkbox>
`}static get properties(){return{item:{type:Object,notifies:!0}}}}),i(76),i(62),customElements.define("ha-customize-icon",class extends n.a{static get template(){return a["a"]`
    <style>
      :host {
        @apply --layout-horizontal;
      }
      .icon-image {
        border: 1px solid grey;
        padding: 8px;
        margin-right: 20px;
        margin-top: 10px;
      }
    </style>
    <iron-icon class="icon-image" icon="[[item.value]]"></iron-icon>
    <paper-input disabled="[[item.secondary]]" label="icon" value="{{item.value}}">
    </paper-input>
`}static get properties(){return{item:{type:Object,notifies:!0}}}}),customElements.define("ha-customize-key-value",class extends n.a{static get template(){return a["a"]`
    <style>
      :host {
        @apply --layout-horizontal;
      }
      paper-input {
        @apply --layout-flex;
      }
      .key {
        padding-right: 20px;
      }
    </style>
    <paper-input disabled="[[item.secondary]]" class="key" label="Attribute name" value="{{item.attribute}}">
    </paper-input>
    <paper-input disabled="[[item.secondary]]" label="Attribute value" value="{{item.value}}">
    </paper-input>
`}static get properties(){return{item:{type:Object,notifies:!0}}}}),customElements.define("ha-customize-string",class extends n.a{static get template(){return a["a"]`
    <paper-input disabled="[[item.secondary]]" label="[[getLabel(item)]]" value="{{item.value}}">
    </paper-input>
`}static get properties(){return{item:{type:Object,notifies:!0}}}getLabel(e){return e.description+("json"===e.type?" (JSON formatted)":"")}}),customElements.define("ha-customize-attribute",class extends n.a{static get template(){return a["a"]`
    <style include="ha-form-style">
      :host {
        display: block;
        position: relative;
        padding-right: 40px;
      }

      .button {
        position: absolute;
        margin-top: -20px;
        top: 50%;
        right: 0;
      }
    </style>
    <div id="wrapper" class="form-group"></div>
    <paper-icon-button class="button" icon="[[getIcon(item.secondary)]]" on-click="tapButton"></paper-icon-button>
`}static get properties(){return{item:{type:Object,notify:!0,observer:"itemObserver"}}}tapButton(){this.item.secondary?this.item=Object.assign({},this.item,{secondary:!1}):this.item=Object.assign({},this.item,{closed:!0})}getIcon(e){return e?"hass:pencil":"hass:close"}itemObserver(e){const t=this.$.wrapper,i=r.a.TYPE_TO_TAG[e.type].toUpperCase();let a;t.lastChild&&t.lastChild.tagName===i?a=t.lastChild:(t.lastChild&&t.removeChild(t.lastChild),this.$.child=a=document.createElement(i.toLowerCase()),a.className="form-control",a.addEventListener("item-changed",()=>{this.item=Object.assign({},a.item)})),a.setProperties({item:this.item}),null===a.parentNode&&t.appendChild(a)}}),customElements.define("ha-form-customize-attributes",class extends(Object(s.a)(n.a)){static get template(){return a["a"]`
    <style>
      [hidden] {
        display: none;
      }
    </style>
    <template is="dom-repeat" items="{{attributes}}" mutable-data="">
      <ha-customize-attribute item="{{item}}" hidden$="[[item.closed]]">
      </ha-customize-attribute>
    </template>
`}static get properties(){return{attributes:{type:Array,notify:!0}}}});var l=i(24);customElements.define("ha-form-customize",class extends n.a{static get template(){return a["a"]`
    <style include="iron-flex ha-style ha-form-style">
      .warning {
        color: red;
      }

      .attributes-text {
        padding-left: 20px;
      }
    </style>
    <template is="dom-if" if="[[computeShowWarning(localConfig, globalConfig)]]">
      <div class="warning">
        It seems that your configuration.yaml doesn't properly include customize.yaml<br>
        Changes made here won't affect your configuration.
      </div>
    </template>
    <template is="dom-if" if="[[hasLocalAttributes]]">
      <h4 class="attributes-text">
        The following attributes are already set in customize.yaml<br>
      </h4>
      <ha-form-customize-attributes attributes="{{localAttributes}}"></ha-form-customize-attributes>
    </template>
    <template is="dom-if" if="[[hasGlobalAttributes]]">
      <h4 class="attributes-text">
        The following attributes are customized from outside of customize.yaml<br>
        Possibly via a domain, a glob or a different include.
      </h4>
      <ha-form-customize-attributes attributes="{{globalAttributes}}"></ha-form-customize-attributes>
    </template>
    <template is="dom-if" if="[[hasExistingAttributes]]">
      <h4 class="attributes-text">
        The following attributes of the entity are set programatically.<br>
        You can override them if you like.
      </h4>
      <ha-form-customize-attributes attributes="{{existingAttributes}}"></ha-form-customize-attributes>
    </template>
    <template is="dom-if" if="[[hasNewAttributes]]">
      <h4 class="attributes-text">
        The following attributes weren't set. Set them if you like.
      </h4>
      <ha-form-customize-attributes attributes="{{newAttributes}}"></ha-form-customize-attributes>
    </template>
    <div class="form-group">
      <paper-dropdown-menu label="Pick an attribute to override" class="flex" dynamic-align="">
        <paper-listbox slot="dropdown-content" selected="{{selectedNewAttribute}}">
          <template is="dom-repeat" items="[[newAttributesOptions]]" as="option">
            <paper-item>[[option]]</paper-item>
          </template>
        </paper-listbox>
      </paper-dropdown-menu>
    </div>
`}static get properties(){return{hass:{type:Object},entity:Object,localAttributes:{type:Array,computed:"computeLocalAttributes(localConfig)"},hasLocalAttributes:Boolean,globalAttributes:{type:Array,computed:"computeGlobalAttributes(localConfig, globalConfig)"},hasGlobalAttributes:Boolean,existingAttributes:{type:Array,computed:"computeExistingAttributes(localConfig, globalConfig, entity)"},hasExistingAttributes:Boolean,newAttributes:{type:Array,value:[]},hasNewAttributes:Boolean,newAttributesOptions:Array,selectedNewAttribute:{type:Number,value:-1,observer:"selectedNewAttributeObserver"},localConfig:Object,globalConfig:Object}}static get observers(){return["attributesObserver(localAttributes.*, globalAttributes.*, existingAttributes.*, newAttributes.*)"]}_initOpenObject(e,t,i,a){return Object.assign({attribute:e,value:t,closed:!1,domain:Object(l.a)(this.entity),secondary:i,description:e},a)}loadEntity(e){return this.entity=e,this.hass.callApi("GET","config/customize/config/"+e.entity_id).then(e=>{this.localConfig=e.local,this.globalConfig=e.global,this.newAttributes=[]})}saveEntity(){const e={};this.localAttributes.concat(this.globalAttributes,this.existingAttributes,this.newAttributes).forEach(t=>{if(t.closed||t.secondary||!t.attribute||!t.value)return;const i="json"===t.type?JSON.parse(t.value):t.value;i&&(e[t.attribute]=i)});const t=this.entity.entity_id;return this.hass.callApi("POST","config/customize/config/"+t,e)}_computeSingleAttribute(e,t,i){const a=r.a.LOGIC_STATE_ATTRIBUTES[e]||{type:r.a.UNKNOWN_TYPE};return this._initOpenObject(e,"json"===a.type?JSON.stringify(t):t,i,a)}_computeAttributes(e,t,i){return t.map(t=>this._computeSingleAttribute(t,e[t],i))}computeLocalAttributes(e){if(!e)return[];const t=Object.keys(e);return this._computeAttributes(e,t,!1)}computeGlobalAttributes(e,t){if(!e||!t)return[];const i=Object.keys(e),a=Object.keys(t).filter(e=>!i.includes(e));return this._computeAttributes(t,a,!0)}computeExistingAttributes(e,t,i){if(!e||!t||!i)return[];const a=Object.keys(e),n=Object.keys(t),o=Object.keys(i.attributes).filter(e=>!a.includes(e)&&!n.includes(e));return this._computeAttributes(i.attributes,o,!0)}computeShowWarning(e,t){return!(!e||!t)&&Object.keys(e).some(i=>JSON.stringify(t[i])!==JSON.stringify(e[i]))}filterFromAttributes(e){return t=>!e||e.every(e=>e.attribute!==t||e.closed)}getNewAttributesOptions(e,t,i,a){return Object.keys(r.a.LOGIC_STATE_ATTRIBUTES).filter(e=>{const t=r.a.LOGIC_STATE_ATTRIBUTES[e];return t&&(!t.domains||!this.entity||t.domains.includes(Object(l.a)(this.entity)))}).filter(this.filterFromAttributes(e)).filter(this.filterFromAttributes(t)).filter(this.filterFromAttributes(i)).filter(this.filterFromAttributes(a)).sort().concat("Other")}selectedNewAttributeObserver(e){if(e<0)return;const t=this.newAttributesOptions[e];if(e===this.newAttributesOptions.length-1){const e=this._initOpenObject("","",!1,{type:r.a.ADD_TYPE});return this.push("newAttributes",e),void(this.selectedNewAttribute=-1)}let i=this.localAttributes.findIndex(e=>e.attribute===t);if(i>=0)return this.set("localAttributes."+i+".closed",!1),void(this.selectedNewAttribute=-1);if((i=this.globalAttributes.findIndex(e=>e.attribute===t))>=0)return this.set("globalAttributes."+i+".closed",!1),void(this.selectedNewAttribute=-1);if((i=this.existingAttributes.findIndex(e=>e.attribute===t))>=0)return this.set("existingAttributes."+i+".closed",!1),void(this.selectedNewAttribute=-1);if((i=this.newAttributes.findIndex(e=>e.attribute===t))>=0)return this.set("newAttributes."+i+".closed",!1),void(this.selectedNewAttribute=-1);const a=this._computeSingleAttribute(t,"",!1);this.push("newAttributes",a),this.selectedNewAttribute=-1}attributesObserver(){this.hasLocalAttributes=this.localAttributes&&this.localAttributes.some(e=>!e.closed),this.hasGlobalAttributes=this.globalAttributes&&this.globalAttributes.some(e=>!e.closed),this.hasExistingAttributes=this.existingAttributes&&this.existingAttributes.some(e=>!e.closed),this.hasNewAttributes=this.newAttributes&&this.newAttributes.some(e=>!e.closed),this.newAttributesOptions=this.getNewAttributesOptions(this.localAttributes,this.globalAttributes,this.existingAttributes,this.newAttributes)}});var p=i(323),d=i(13);customElements.define("ha-config-customize",class extends(Object(d.a)(n.a)){static get template(){return a["a"]`
    <style include="ha-style">
    </style>

    <app-header-layout has-scrolling-region="">
      <app-header slot="header" fixed="">
        <app-toolbar>
          <paper-icon-button icon="hass:arrow-left" on-click="_backTapped"></paper-icon-button>
          <div main-title="">[[localize('ui.panel.config.customize.caption')]]</div>
        </app-toolbar>
      </app-header>

      <div class$="[[computeClasses(isWide)]]">
        <ha-config-section is-wide="[[isWide]]">
          <span slot="header">Customization</span>
          <span slot="introduction">
            Tweak per-entity attributes.<br>
            Added/edited customizations will take effect immediately. Removed customizations will take effect when the entity is updated.
          </span>
          <ha-entity-config hass="[[hass]]" label="Entity" entities="[[entities]]" config="[[entityConfig]]">
          </ha-entity-config>
        </ha-config-section>
      </div>
    </app-header-layout>
`}static get properties(){return{hass:Object,isWide:Boolean,entities:{type:Array,computed:"computeEntities(hass)"},entityConfig:{type:Object,value:{component:"ha-form-customize",computeSelectCaption:e=>Object(o.a)(e)+" ("+Object(l.a)(e)+")"}}}}computeClasses(e){return e?"content":"content narrow"}_backTapped(){history.back()}computeEntities(e){return Object.keys(e.states).map(t=>e.states[t]).sort(p.a)}})}}]);
//# sourceMappingURL=3a80443c943ab5755306.chunk.js.map