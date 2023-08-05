/*! For license information please see 3c34488ba2d64bbfad18.chunk.js.LICENSE */
(window.webpackJsonp=window.webpackJsonp||[]).push([[54],{200:function(t,i,e){"use strict";e(2),e(27),e(30),e(43);var a=e(3),n=e(0);Object(a.a)({_template:n["a"]`
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
`,is:"paper-item-body"})},203:function(t,i,e){"use strict";var a=e(0),n=e(4);e(122),customElements.define("ha-config-section",class extends n.a{static get template(){return a["a"]`
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
`}static get properties(){return{hass:{type:Object},narrow:{type:Boolean},showMenu:{type:Boolean,value:!1},isWide:{type:Boolean,value:!1}}}computeContentClasses(t){return t?"content ":"content narrow"}computeClasses(t){return"together layout "+(t?"horizontal":"vertical narrow")}})},207:function(t,i,e){"use strict";e(157),e(156),e(124),e(63);var a=e(0),n=e(4);customElements.define("hass-subpage",class extends n.a{static get template(){return a["a"]`
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
`}static get properties(){return{header:String}}_backTapped(){history.back()}})},279:function(t,i,e){"use strict";e(2);var a=e(3),n=e(1),o=e(0);Object(a.a)({_template:o["a"]`
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
`,is:"paper-tooltip",hostAttributes:{role:"tooltip",tabindex:-1},properties:{for:{type:String,observer:"_findTarget"},manualMode:{type:Boolean,value:!1,observer:"_manualModeChanged"},position:{type:String,value:"bottom"},fitToVisibleBounds:{type:Boolean,value:!1},offset:{type:Number,value:14},marginTop:{type:Number,value:14},animationDelay:{type:Number,value:500,observer:"_delayChange"},animationEntry:{type:String,value:""},animationExit:{type:String,value:""},animationConfig:{type:Object,value:function(){return{entry:[{name:"fade-in-animation",node:this,timing:{delay:0}}],exit:[{name:"fade-out-animation",node:this}]}}},_showing:{type:Boolean,value:!1}},listeners:{webkitAnimationEnd:"_onAnimationEnd"},get target(){var t=Object(n.b)(this).parentNode,i=Object(n.b)(this).getOwnerRoot();return this.for?Object(n.b)(i).querySelector("#"+this.for):t.nodeType==Node.DOCUMENT_FRAGMENT_NODE?i.host:t},attached:function(){this._findTarget()},detached:function(){this.manualMode||this._removeListeners()},playAnimation:function(t){"entry"===t?this.show():"exit"===t&&this.hide()},cancelAnimation:function(){this.$.tooltip.classList.add("cancel-animation")},show:function(){if(!this._showing){if(""===Object(n.b)(this).textContent.trim()){for(var t=!0,i=Object(n.b)(this).getEffectiveChildNodes(),e=0;e<i.length;e++)if(""!==i[e].textContent.trim()){t=!1;break}if(t)return}this._showing=!0,this.$.tooltip.classList.remove("hidden"),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.updatePosition(),this._animationPlaying=!0,this.$.tooltip.classList.add(this._getAnimationType("entry"))}},hide:function(){if(this._showing){if(this._animationPlaying)return this._showing=!1,void this._cancelAnimation();this._onAnimationFinish(),this._showing=!1,this._animationPlaying=!0}},updatePosition:function(){if(this._target&&this.offsetParent){var t=this.offset;14!=this.marginTop&&14==this.offset&&(t=this.marginTop);var i,e,a=this.offsetParent.getBoundingClientRect(),n=this._target.getBoundingClientRect(),o=this.getBoundingClientRect(),s=(n.width-o.width)/2,r=(n.height-o.height)/2,p=n.left-a.left,l=n.top-a.top;switch(this.position){case"top":i=p+s,e=l-o.height-t;break;case"bottom":i=p+s,e=l+n.height+t;break;case"left":i=p-o.width-t,e=l+r;break;case"right":i=p+n.width+t,e=l+r}this.fitToVisibleBounds?(a.left+i+o.width>window.innerWidth?(this.style.right="0px",this.style.left="auto"):(this.style.left=Math.max(0,i)+"px",this.style.right="auto"),a.top+e+o.height>window.innerHeight?(this.style.bottom=a.height-l+t+"px",this.style.top="auto"):(this.style.top=Math.max(-a.top,e)+"px",this.style.bottom="auto")):(this.style.left=i+"px",this.style.top=e+"px")}},_addListeners:function(){this._target&&(this.listen(this._target,"mouseenter","show"),this.listen(this._target,"focus","show"),this.listen(this._target,"mouseleave","hide"),this.listen(this._target,"blur","hide"),this.listen(this._target,"tap","hide")),this.listen(this.$.tooltip,"animationend","_onAnimationEnd"),this.listen(this,"mouseenter","hide")},_findTarget:function(){this.manualMode||this._removeListeners(),this._target=this.target,this.manualMode||this._addListeners()},_delayChange:function(t){500!==t&&this.updateStyles({"--paper-tooltip-delay-in":t+"ms"})},_manualModeChanged:function(){this.manualMode?this._removeListeners():this._addListeners()},_cancelAnimation:function(){this.$.tooltip.classList.remove(this._getAnimationType("entry")),this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.add("hidden")},_onAnimationFinish:function(){this._showing&&(this.$.tooltip.classList.remove(this._getAnimationType("entry")),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.add(this._getAnimationType("exit")))},_onAnimationEnd:function(){this._animationPlaying=!1,this._showing||(this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.$.tooltip.classList.add("hidden"))},_getAnimationType:function(t){if("entry"===t&&""!==this.animationEntry)return this.animationEntry;if("exit"===t&&""!==this.animationExit)return this.animationExit;if(this.animationConfig[t]&&"string"==typeof this.animationConfig[t][0].name){if(this.animationConfig[t][0].timing&&this.animationConfig[t][0].timing.delay&&0!==this.animationConfig[t][0].timing.delay){var i=this.animationConfig[t][0].timing.delay;"entry"===t?this.updateStyles({"--paper-tooltip-delay-in":i+"ms"}):"exit"===t&&this.updateStyles({"--paper-tooltip-delay-out":i+"ms"})}return this.animationConfig[t][0].name}},_removeListeners:function(){this._target&&(this.unlisten(this._target,"mouseenter","show"),this.unlisten(this._target,"focus","show"),this.unlisten(this._target,"mouseleave","hide"),this.unlisten(this._target,"blur","hide"),this.unlisten(this._target,"tap","hide")),this.unlisten(this.$.tooltip,"animationend","_onAnimationEnd"),this.unlisten(this,"mouseenter","hide")}})},390:function(t,i,e){"use strict";e.r(i),e(31),e(279),e(55),e(155),e(200);var a=e(0),n=e(4),o=e(15),s=e(8),r=(e(89),e(114));customElements.define("ha-state-icon",class extends n.a{static get template(){return a["a"]`<ha-icon icon="[[computeIcon(stateObj)]]"></ha-icon>`}static get properties(){return{stateObj:{type:Object}}}computeIcon(t){return Object(r.a)(t)}}),e(207),e(122),e(203);var p=e(14),l=e(13),d=e(29);let c=!1;customElements.define("ha-config-entries",class extends(Object(l.a)(Object(p.a)(n.a))){static get template(){return a["a"]`
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
  </style>

  <hass-subpage header="Integrations">
    <template is="dom-if" if="[[_progress.length]]">
      <ha-config-section>
        <span slot="header">Discovered</span>
        <paper-card>
          <template is="dom-repeat" items="[[_progress]]">
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
        <template is="dom-if" if="[[!_entries.length]]">
          <div class="config-entry-row">
            <paper-item-body two-line>
              <div>Nothing configured yet</div>
            </paper-item-body>
          </div>
        </template>
        <template is="dom-repeat" items="[[_entries]]">
          <div class="config-entry-row">
            <paper-item-body three-line>
              <div>[[_computeIntegrationTitle(localize, item.domain)]]: [[item.title]]</div>
              <div secondary>[[item.state]] – added by [[item.source]]</div>
              <div secondary>
                <template is='dom-repeat' items='[[_computeConfigEntryEntities(hass, item, _entities)]]'>
                  <span>
                    <ha-state-icon state-obj='[[item]]' on-click='_handleMoreInfo'></ha-state-icon>
                    <paper-tooltip position="bottom">[[_computeStateName(item)]]</paper-tooltip>
                  </span>
                </template>
              </div>
            </paper-item-body>
            <paper-button on-click="_removeEntry">Remove</paper-button>
          </div>
        </template>
      </paper-card>
    </ha-config-section>

    <ha-config-section>
      <span slot="header">Set up a new integration</span>
      <paper-card>
        <template is="dom-repeat" items="[[_handlers]]">
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
`}static get properties(){return{hass:Object,isWide:Boolean,_entries:Array,_entities:Array,_progress:Array,_handlers:Array}}ready(){super.ready(),this._loadData()}connectedCallback(){super.connectedCallback(),c||(c=!0,this.fire("register-dialog",{dialogShowEvent:"show-config-flow",dialogTag:"ha-config-flow",dialogImport:()=>e.e(45).then(e.bind(null,654))})),this.hass.connection.subscribeEvents(()=>{this._debouncer=o.a.debounce(this._debouncer,s.timeOut.after(500),()=>this._loadData())},"config_entry_discovered").then(t=>{this._unsubEvents=t})}disconnectedCallback(){super.disconnectedCallback(),this._unsubEvents&&this._unsubEvents()}_createFlow(t){this.fire("show-config-flow",{hass:this.hass,newFlowForHandler:t.model.item,dialogClosedCallback:()=>this._loadData()})}_continueFlow(t){this.fire("show-config-flow",{hass:this.hass,continueFlowId:t.model.item.flow_id,dialogClosedCallback:()=>this._loadData()})}_removeEntry(t){if(!confirm("Are you sure you want to delete this integration?"))return;const i=t.model.item.entry_id;this.hass.callApi("delete",`config/config_entries/entry/${i}`).then(t=>{this._entries=this._entries.filter(t=>t.entry_id!==i),t.require_restart&&alert("Restart Home Assistant to finish removing this integration")})}_loadData(){this.hass.callApi("get","config/config_entries/entry").then(t=>{this._entries=t}),this.hass.callApi("get","config/config_entries/flow").then(t=>{this._progress=t}),this.hass.callApi("get","config/config_entries/flow_handlers").then(t=>{this._handlers=t}),this.hass.callWS({type:"config/entity_registry/list"}).then(t=>{this._entities=t})}_computeIntegrationTitle(t,i){return t(`component.${i}.config.title`)}_computeConfigEntryEntities(t,i,e){if(!e)return[];const a=[];return e.forEach(e=>{e.config_entry_id===i.entry_id&&e.entity_id in t.states&&a.push(t.states[e.entity_id])}),a}_computeStateName(t){return Object(d.a)(t)}_handleMoreInfo(t){this.fire("hass-more-info",{entityId:t.model.item.entity_id})}})}}]);
//# sourceMappingURL=3c34488ba2d64bbfad18.chunk.js.map