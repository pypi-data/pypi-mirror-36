/*! For license information please see 1aa83272dab571d4a597.chunk.js.LICENSE */
(window.webpackJsonp=window.webpackJsonp||[]).push([[9],{249:function(n,e,o){"use strict";o(2);var t=o(96),a=(o(30),o(27),o(3)),i=o(36),r=document.createElement("template");r.setAttribute("style","display: none;"),r.innerHTML='<dom-module id="paper-radio-button">\n  <template strip-whitespace="">\n    <style>\n      :host {\n        display: inline-block;\n        line-height: 0;\n        white-space: nowrap;\n        cursor: pointer;\n        @apply --paper-font-common-base;\n        --calculated-paper-radio-button-size: var(--paper-radio-button-size, 16px);\n        /* -1px is a sentinel for the default and is replace in `attached`. */\n        --calculated-paper-radio-button-ink-size: var(--paper-radio-button-ink-size, -1px);\n      }\n\n      :host(:focus) {\n        outline: none;\n      }\n\n      #radioContainer {\n        @apply --layout-inline;\n        @apply --layout-center-center;\n        position: relative;\n        width: var(--calculated-paper-radio-button-size);\n        height: var(--calculated-paper-radio-button-size);\n        vertical-align: middle;\n\n        @apply --paper-radio-button-radio-container;\n      }\n\n      #ink {\n        position: absolute;\n        top: 50%;\n        left: 50%;\n        right: auto;\n        width: var(--calculated-paper-radio-button-ink-size);\n        height: var(--calculated-paper-radio-button-ink-size);\n        color: var(--paper-radio-button-unchecked-ink-color, var(--primary-text-color));\n        opacity: 0.6;\n        pointer-events: none;\n        -webkit-transform: translate(-50%, -50%);\n        transform: translate(-50%, -50%);\n      }\n\n      #ink[checked] {\n        color: var(--paper-radio-button-checked-ink-color, var(--primary-color));\n      }\n\n      #offRadio, #onRadio {\n        position: absolute;\n        box-sizing: border-box;\n        top: 0;\n        left: 0;\n        width: 100%;\n        height: 100%;\n        border-radius: 50%;\n      }\n\n      #offRadio {\n        border: 2px solid var(--paper-radio-button-unchecked-color, var(--primary-text-color));\n        background-color: var(--paper-radio-button-unchecked-background-color, transparent);\n        transition: border-color 0.28s;\n      }\n\n      #onRadio {\n        background-color: var(--paper-radio-button-checked-color, var(--primary-color));\n        -webkit-transform: scale(0);\n        transform: scale(0);\n        transition: -webkit-transform ease 0.28s;\n        transition: transform ease 0.28s;\n        will-change: transform;\n      }\n\n      :host([checked]) #offRadio {\n        border-color: var(--paper-radio-button-checked-color, var(--primary-color));\n      }\n\n      :host([checked]) #onRadio {\n        -webkit-transform: scale(0.5);\n        transform: scale(0.5);\n      }\n\n      #radioLabel {\n        line-height: normal;\n        position: relative;\n        display: inline-block;\n        vertical-align: middle;\n        margin-left: var(--paper-radio-button-label-spacing, 10px);\n        white-space: normal;\n        color: var(--paper-radio-button-label-color, var(--primary-text-color));\n\n        @apply --paper-radio-button-label;\n      }\n\n      :host([checked]) #radioLabel {\n        @apply --paper-radio-button-label-checked;\n      }\n\n      #radioLabel:dir(rtl) {\n        margin-left: 0;\n        margin-right: var(--paper-radio-button-label-spacing, 10px);\n      }\n\n      #radioLabel[hidden] {\n        display: none;\n      }\n\n      /* disabled state */\n\n      :host([disabled]) #offRadio {\n        border-color: var(--paper-radio-button-unchecked-color, var(--primary-text-color));\n        opacity: 0.5;\n      }\n\n      :host([disabled][checked]) #onRadio {\n        background-color: var(--paper-radio-button-unchecked-color, var(--primary-text-color));\n        opacity: 0.5;\n      }\n\n      :host([disabled]) #radioLabel {\n        /* slightly darker than the button, so that it\'s readable */\n        opacity: 0.65;\n      }\n    </style>\n\n    <div id="radioContainer">\n      <div id="offRadio"></div>\n      <div id="onRadio"></div>\n    </div>\n\n    <div id="radioLabel"><slot></slot></div>\n  </template>\n\n  \n</dom-module>',document.head.appendChild(r.content),Object(a.a)({is:"paper-radio-button",behaviors:[t.a],hostAttributes:{role:"radio","aria-checked":!1,tabindex:0},properties:{ariaActiveAttribute:{type:String,value:"aria-checked"}},ready:function(){this._rippleContainer=this.$.radioContainer},attached:function(){Object(i.a)(this,function(){if("-1px"===this.getComputedStyleValue("--calculated-paper-radio-button-ink-size").trim()){var n=parseFloat(this.getComputedStyleValue("--calculated-paper-radio-button-size").trim()),e=Math.floor(3*n);e%2!=n%2&&e++,this.updateStyles({"--paper-radio-button-ink-size":e+"px"})}})}})},250:function(n,e,o){"use strict";o(2),o(27),o(76);var t=o(60),a=(o(65),o(48),o(30),o(3)),i=document.createElement("template");i.setAttribute("style","display: none;"),i.innerHTML='<dom-module id="paper-fab">\n  <template strip-whitespace="">\n    <style include="paper-material-styles">\n      :host {\n        @apply --layout-vertical;\n        @apply --layout-center-center;\n\n        background: var(--paper-fab-background, var(--accent-color));\n        border-radius: 50%;\n        box-sizing: border-box;\n        color: var(--text-primary-color);\n        cursor: pointer;\n        height: 56px;\n        min-width: 0;\n        outline: none;\n        padding: 16px;\n        position: relative;\n        -moz-user-select: none;\n        -ms-user-select: none;\n        -webkit-user-select: none;\n        user-select: none;\n        width: 56px;\n        z-index: 0;\n\n        /* NOTE: Both values are needed, since some phones require the value `transparent`. */\n        -webkit-tap-highlight-color: rgba(0,0,0,0);\n        -webkit-tap-highlight-color: transparent;\n\n        @apply --paper-fab;\n      }\n\n      [hidden] {\n        display: none !important;\n      }\n\n      :host([mini]) {\n        width: 40px;\n        height: 40px;\n        padding: 8px;\n\n        @apply --paper-fab-mini;\n      }\n\n      :host([disabled]) {\n        color: var(--paper-fab-disabled-text, var(--paper-grey-500));\n        background: var(--paper-fab-disabled-background, var(--paper-grey-300));\n\n        @apply --paper-fab-disabled;\n      }\n\n      iron-icon {\n        @apply --paper-fab-iron-icon;\n      }\n\n      span {\n        width: 100%;\n        white-space: nowrap;\n        overflow: hidden;\n        text-overflow: ellipsis;\n        text-align: center;\n\n        @apply --paper-fab-label;\n      }\n\n      :host(.keyboard-focus) {\n        background: var(--paper-fab-keyboard-focus-background, var(--paper-pink-900));\n      }\n\n      :host([elevation="1"]) {\n        @apply --paper-material-elevation-1;\n      }\n\n      :host([elevation="2"]) {\n        @apply --paper-material-elevation-2;\n      }\n\n      :host([elevation="3"]) {\n        @apply --paper-material-elevation-3;\n      }\n\n      :host([elevation="4"]) {\n        @apply --paper-material-elevation-4;\n      }\n\n      :host([elevation="5"]) {\n        @apply --paper-material-elevation-5;\n      }\n    </style>\n\n    <iron-icon id="icon" hidden$="{{!_computeIsIconFab(icon, src)}}" src="[[src]]" icon="[[icon]]"></iron-icon>\n    <span hidden$="{{_computeIsIconFab(icon, src)}}">{{label}}</span>\n  </template>\n\n  \n</dom-module>',document.head.appendChild(i.content),Object(a.a)({is:"paper-fab",behaviors:[t.a],properties:{src:{type:String,value:""},icon:{type:String,value:""},mini:{type:Boolean,value:!1,reflectToAttribute:!0},label:{type:String,observer:"_labelChanged"}},_labelChanged:function(){this.setAttribute("aria-label",this.label)},_computeIsIconFab:function(n,e){return n.length>0||e.length>0}})},269:function(n,e,o){"use strict";o(2),o(10);var t=o(153),a=(o(249),o(3)),i=o(0),r=o(46),l=Object.freeze(Object.defineProperties(["\n    <style>\n      :host {\n        display: inline-block;\n      }\n\n      :host ::slotted(*) {\n        padding: var(--paper-radio-group-item-padding, 12px);\n      }\n    </style>\n\n    <slot></slot>\n"],{raw:{value:Object.freeze(["\n    <style>\n      :host {\n        display: inline-block;\n      }\n\n      :host ::slotted(*) {\n        padding: var(--paper-radio-group-item-padding, 12px);\n      }\n    </style>\n\n    <slot></slot>\n"])}}));Object(a.a)({_template:Object(i.a)(l),is:"paper-radio-group",behaviors:[t.a],hostAttributes:{role:"radiogroup"},properties:{attrForSelected:{type:String,value:"name"},selectedAttribute:{type:String,value:"checked"},selectable:{type:String,value:"paper-radio-button"},allowEmptySelection:{type:Boolean,value:!1}},select:function(n){var e=this._valueToItem(n);if(!e||!e.hasAttribute("disabled")){if(this.selected){var o=this._valueToItem(this.selected);if(this.selected==n){if(!this.allowEmptySelection)return void(o&&(o.checked=!0));n=""}o&&(o.checked=!1)}r.a.select.apply(this,[n]),this.fire("paper-radio-group-changed")}},_activateFocusedItem:function(){this._itemActivate(this._valueForItem(this.focusedItem),this.focusedItem)},_onUpKey:function(n){this._focusPrevious(),n.preventDefault(),this._activateFocusedItem()},_onDownKey:function(n){this._focusNext(),n.preventDefault(),this._activateFocusedItem()},_onLeftKey:function(n){t.b._onLeftKey.apply(this,arguments),this._activateFocusedItem()},_onRightKey:function(n){t.b._onRightKey.apply(this,arguments),this._activateFocusedItem()}})},312:function(n,e,o){"use strict";o(2),o(10);var t=o(19),a=o(11),i=o(34),r=(o(76),o(37)),l=o(33),p=(o(128),o(30),o(133),o(132),o(3)),d=o(0),s=o(1),c=o(28),b=Object.freeze(Object.defineProperties(['\n    <style include="paper-dropdown-menu-shared-styles">\n      :host(:focus) {\n        outline: none;\n      }\n\n      :host {\n        width: 200px;  /* Default size of an <input> */\n      }\n\n      /**\n       * All of these styles below are for styling the fake-input display\n       */\n      [slot="dropdown-trigger"] {\n        box-sizing: border-box;\n        position: relative;\n        width: 100%;\n        padding: 16px 0 8px 0;\n      }\n\n      :host([disabled]) [slot="dropdown-trigger"] {\n        pointer-events: none;\n        opacity: var(--paper-dropdown-menu-disabled-opacity, 0.33);\n      }\n\n      :host([no-label-float]) [slot="dropdown-trigger"] {\n        padding-top: 8px;   /* If there\'s no label, we need less space up top. */\n      }\n\n      #input {\n        @apply --paper-font-subhead;\n        @apply --paper-font-common-nowrap;\n        line-height: 1.5;\n        border-bottom: 1px solid var(--paper-dropdown-menu-color, var(--secondary-text-color));\n        color: var(--paper-dropdown-menu-color, var(--primary-text-color));\n        width: 100%;\n        box-sizing: border-box;\n        padding: 12px 20px 0 0;   /* Right padding so that text doesn\'t overlap the icon */\n        outline: none;\n        @apply --paper-dropdown-menu-input;\n      }\n\n      #input:dir(rtl) {\n        padding-right: 0px;\n        padding-left: 20px;\n      }\n\n      :host([disabled]) #input {\n        border-bottom: 1px dashed var(--paper-dropdown-menu-color, var(--secondary-text-color));\n      }\n\n      :host([invalid]) #input {\n        border-bottom: 2px solid var(--paper-dropdown-error-color, var(--error-color));\n      }\n\n      :host([no-label-float]) #input {\n        padding-top: 0;   /* If there\'s no label, we need less space up top. */\n      }\n\n      label {\n        @apply --paper-font-subhead;\n        @apply --paper-font-common-nowrap;\n        display: block;\n        position: absolute;\n        bottom: 0;\n        left: 0;\n        right: 0;\n        /**\n         * The container has a 16px top padding, and there\'s 12px of padding\n         * between the input and the label (from the input\'s padding-top)\n         */\n        top: 28px;\n        box-sizing: border-box;\n        width: 100%;\n        padding-right: 20px;    /* Right padding so that text doesn\'t overlap the icon */\n        text-align: left;\n        transition-duration: .2s;\n        transition-timing-function: cubic-bezier(.4,0,.2,1);\n        color: var(--paper-dropdown-menu-color, var(--secondary-text-color));\n        @apply --paper-dropdown-menu-label;\n      }\n\n      label:dir(rtl) {\n        padding-right: 0px;\n        padding-left: 20px;\n      }\n\n      :host([no-label-float]) label {\n        top: 8px;\n        /* Since the label doesn\'t need to float, remove the animation duration\n        which slows down visibility changes (i.e. when a selection is made) */\n        transition-duration: 0s;\n      }\n\n      label.label-is-floating {\n        font-size: 12px;\n        top: 8px;\n      }\n\n      label.label-is-hidden {\n        visibility: hidden;\n      }\n\n      :host([focused]) label.label-is-floating {\n        color: var(--paper-dropdown-menu-focus-color, var(--primary-color));\n      }\n\n      :host([invalid]) label.label-is-floating {\n        color: var(--paper-dropdown-error-color, var(--error-color));\n      }\n\n      /**\n       * Sets up the focused underline. It\'s initially hidden, and becomes\n       * visible when it\'s focused.\n       */\n      label:after {\n        background-color: var(--paper-dropdown-menu-focus-color, var(--primary-color));\n        bottom: 7px;    /* The container has an 8px bottom padding */\n        content: \'\';\n        height: 2px;\n        left: 45%;\n        position: absolute;\n        transition-duration: .2s;\n        transition-timing-function: cubic-bezier(.4,0,.2,1);\n        visibility: hidden;\n        width: 8px;\n        z-index: 10;\n      }\n\n      :host([invalid]) label:after {\n        background-color: var(--paper-dropdown-error-color, var(--error-color));\n      }\n\n      :host([no-label-float]) label:after {\n        bottom: 7px;    /* The container has a 8px bottom padding */\n      }\n\n      :host([focused]:not([disabled])) label:after {\n        left: 0;\n        visibility: visible;\n        width: 100%;\n      }\n\n      iron-icon {\n        position: absolute;\n        right: 0px;\n        bottom: 8px;    /* The container has an 8px bottom padding */\n        @apply --paper-font-subhead;\n        color: var(--disabled-text-color);\n        @apply --paper-dropdown-menu-icon;\n      }\n\n      iron-icon:dir(rtl) {\n        left: 0;\n        right: auto;\n      }\n\n      :host([no-label-float]) iron-icon {\n        margin-top: 0px;\n      }\n\n      .error {\n        display: inline-block;\n        visibility: hidden;\n        color: var(--paper-dropdown-error-color, var(--error-color));\n        @apply --paper-font-caption;\n        position: absolute;\n        left:0;\n        right:0;\n        bottom: -12px;\n      }\n\n      :host([invalid]) .error {\n        visibility: visible;\n      }\n    </style>\n\n    \x3c!-- this div fulfills an a11y requirement for combobox, do not remove --\x3e\n    <span role="button"></span>\n    <paper-menu-button id="menuButton" vertical-align="[[verticalAlign]]" horizontal-align="[[horizontalAlign]]" vertical-offset="[[_computeMenuVerticalOffset(noLabelFloat, verticalOffset)]]" disabled="[[disabled]]" no-animations="[[noAnimations]]" on-iron-select="_onIronSelect" on-iron-deselect="_onIronDeselect" opened="{{opened}}" close-on-activate="" allow-outside-scroll="[[allowOutsideScroll]]">\n      \x3c!-- support hybrid mode: user might be using paper-menu-button 1.x which distributes via <content> --\x3e\n      <div class="dropdown-trigger" slot="dropdown-trigger">\n        <label class$="[[_computeLabelClass(noLabelFloat,alwaysFloatLabel,hasContent)]]">\n          [[label]]\n        </label>\n        <div id="input" tabindex="-1">&nbsp;</div>\n        <iron-icon icon="paper-dropdown-menu:arrow-drop-down"></iron-icon>\n        <span class="error">[[errorMessage]]</span>\n      </div>\n      <slot id="content" name="dropdown-content" slot="dropdown-content"></slot>\n    </paper-menu-button>\n'],{raw:{value:Object.freeze(['\n    <style include="paper-dropdown-menu-shared-styles">\n      :host(:focus) {\n        outline: none;\n      }\n\n      :host {\n        width: 200px;  /* Default size of an <input> */\n      }\n\n      /**\n       * All of these styles below are for styling the fake-input display\n       */\n      [slot="dropdown-trigger"] {\n        box-sizing: border-box;\n        position: relative;\n        width: 100%;\n        padding: 16px 0 8px 0;\n      }\n\n      :host([disabled]) [slot="dropdown-trigger"] {\n        pointer-events: none;\n        opacity: var(--paper-dropdown-menu-disabled-opacity, 0.33);\n      }\n\n      :host([no-label-float]) [slot="dropdown-trigger"] {\n        padding-top: 8px;   /* If there\'s no label, we need less space up top. */\n      }\n\n      #input {\n        @apply --paper-font-subhead;\n        @apply --paper-font-common-nowrap;\n        line-height: 1.5;\n        border-bottom: 1px solid var(--paper-dropdown-menu-color, var(--secondary-text-color));\n        color: var(--paper-dropdown-menu-color, var(--primary-text-color));\n        width: 100%;\n        box-sizing: border-box;\n        padding: 12px 20px 0 0;   /* Right padding so that text doesn\'t overlap the icon */\n        outline: none;\n        @apply --paper-dropdown-menu-input;\n      }\n\n      #input:dir(rtl) {\n        padding-right: 0px;\n        padding-left: 20px;\n      }\n\n      :host([disabled]) #input {\n        border-bottom: 1px dashed var(--paper-dropdown-menu-color, var(--secondary-text-color));\n      }\n\n      :host([invalid]) #input {\n        border-bottom: 2px solid var(--paper-dropdown-error-color, var(--error-color));\n      }\n\n      :host([no-label-float]) #input {\n        padding-top: 0;   /* If there\'s no label, we need less space up top. */\n      }\n\n      label {\n        @apply --paper-font-subhead;\n        @apply --paper-font-common-nowrap;\n        display: block;\n        position: absolute;\n        bottom: 0;\n        left: 0;\n        right: 0;\n        /**\n         * The container has a 16px top padding, and there\'s 12px of padding\n         * between the input and the label (from the input\'s padding-top)\n         */\n        top: 28px;\n        box-sizing: border-box;\n        width: 100%;\n        padding-right: 20px;    /* Right padding so that text doesn\'t overlap the icon */\n        text-align: left;\n        transition-duration: .2s;\n        transition-timing-function: cubic-bezier(.4,0,.2,1);\n        color: var(--paper-dropdown-menu-color, var(--secondary-text-color));\n        @apply --paper-dropdown-menu-label;\n      }\n\n      label:dir(rtl) {\n        padding-right: 0px;\n        padding-left: 20px;\n      }\n\n      :host([no-label-float]) label {\n        top: 8px;\n        /* Since the label doesn\'t need to float, remove the animation duration\n        which slows down visibility changes (i.e. when a selection is made) */\n        transition-duration: 0s;\n      }\n\n      label.label-is-floating {\n        font-size: 12px;\n        top: 8px;\n      }\n\n      label.label-is-hidden {\n        visibility: hidden;\n      }\n\n      :host([focused]) label.label-is-floating {\n        color: var(--paper-dropdown-menu-focus-color, var(--primary-color));\n      }\n\n      :host([invalid]) label.label-is-floating {\n        color: var(--paper-dropdown-error-color, var(--error-color));\n      }\n\n      /**\n       * Sets up the focused underline. It\'s initially hidden, and becomes\n       * visible when it\'s focused.\n       */\n      label:after {\n        background-color: var(--paper-dropdown-menu-focus-color, var(--primary-color));\n        bottom: 7px;    /* The container has an 8px bottom padding */\n        content: \'\';\n        height: 2px;\n        left: 45%;\n        position: absolute;\n        transition-duration: .2s;\n        transition-timing-function: cubic-bezier(.4,0,.2,1);\n        visibility: hidden;\n        width: 8px;\n        z-index: 10;\n      }\n\n      :host([invalid]) label:after {\n        background-color: var(--paper-dropdown-error-color, var(--error-color));\n      }\n\n      :host([no-label-float]) label:after {\n        bottom: 7px;    /* The container has a 8px bottom padding */\n      }\n\n      :host([focused]:not([disabled])) label:after {\n        left: 0;\n        visibility: visible;\n        width: 100%;\n      }\n\n      iron-icon {\n        position: absolute;\n        right: 0px;\n        bottom: 8px;    /* The container has an 8px bottom padding */\n        @apply --paper-font-subhead;\n        color: var(--disabled-text-color);\n        @apply --paper-dropdown-menu-icon;\n      }\n\n      iron-icon:dir(rtl) {\n        left: 0;\n        right: auto;\n      }\n\n      :host([no-label-float]) iron-icon {\n        margin-top: 0px;\n      }\n\n      .error {\n        display: inline-block;\n        visibility: hidden;\n        color: var(--paper-dropdown-error-color, var(--error-color));\n        @apply --paper-font-caption;\n        position: absolute;\n        left:0;\n        right:0;\n        bottom: -12px;\n      }\n\n      :host([invalid]) .error {\n        visibility: visible;\n      }\n    </style>\n\n    \x3c!-- this div fulfills an a11y requirement for combobox, do not remove --\x3e\n    <span role="button"></span>\n    <paper-menu-button id="menuButton" vertical-align="[[verticalAlign]]" horizontal-align="[[horizontalAlign]]" vertical-offset="[[_computeMenuVerticalOffset(noLabelFloat, verticalOffset)]]" disabled="[[disabled]]" no-animations="[[noAnimations]]" on-iron-select="_onIronSelect" on-iron-deselect="_onIronDeselect" opened="{{opened}}" close-on-activate="" allow-outside-scroll="[[allowOutsideScroll]]">\n      \x3c!-- support hybrid mode: user might be using paper-menu-button 1.x which distributes via <content> --\x3e\n      <div class="dropdown-trigger" slot="dropdown-trigger">\n        <label class\\$="[[_computeLabelClass(noLabelFloat,alwaysFloatLabel,hasContent)]]">\n          [[label]]\n        </label>\n        <div id="input" tabindex="-1">&nbsp;</div>\n        <iron-icon icon="paper-dropdown-menu:arrow-drop-down"></iron-icon>\n        <span class="error">[[errorMessage]]</span>\n      </div>\n      <slot id="content" name="dropdown-content" slot="dropdown-content"></slot>\n    </paper-menu-button>\n'])}}));Object(p.a)({_template:Object(d.a)(b),is:"paper-dropdown-menu-light",behaviors:[t.a,a.a,l.a,i.a,r.a],properties:{selectedItemLabel:{type:String,notify:!0,readOnly:!0},selectedItem:{type:Object,notify:!0,readOnly:!0},value:{type:String,notify:!0,observer:"_valueChanged"},label:{type:String},placeholder:{type:String},opened:{type:Boolean,notify:!0,value:!1,observer:"_openedChanged"},allowOutsideScroll:{type:Boolean,value:!1},noLabelFloat:{type:Boolean,value:!1,reflectToAttribute:!0},alwaysFloatLabel:{type:Boolean,value:!1},noAnimations:{type:Boolean,value:!1},horizontalAlign:{type:String,value:"right"},verticalAlign:{type:String,value:"top"},verticalOffset:Number,hasContent:{type:Boolean,readOnly:!0}},listeners:{tap:"_onTap"},keyBindings:{"up down":"open",esc:"close"},hostAttributes:{tabindex:0,role:"combobox","aria-autocomplete":"none","aria-haspopup":"true"},observers:["_selectedItemChanged(selectedItem)"],attached:function(){var n=this.contentElement;n&&n.selectedItem&&this._setSelectedItem(n.selectedItem)},get contentElement(){for(var n=Object(s.b)(this.$.content).getDistributedNodes(),e=0,o=n.length;e<o;e++)if(n[e].nodeType===Node.ELEMENT_NODE)return n[e]},open:function(){this.$.menuButton.open()},close:function(){this.$.menuButton.close()},_onIronSelect:function(n){this._setSelectedItem(n.detail.item)},_onIronDeselect:function(n){this._setSelectedItem(null)},_onTap:function(n){c.findOriginalTarget(n)===this&&this.open()},_selectedItemChanged:function(n){var e;e=n?n.label||n.getAttribute("label")||n.textContent.trim():"",this.value=e,this._setSelectedItemLabel(e)},_computeMenuVerticalOffset:function(n,e){return e||(n?-4:8)},_getValidity:function(n){return this.disabled||!this.required||this.required&&!!this.value},_openedChanged:function(){var n=this.opened?"true":"false",e=this.contentElement;e&&e.setAttribute("aria-expanded",n)},_computeLabelClass:function(n,e,o){var t="";return!0===n?o?"label-is-hidden":"":((o||!0===e)&&(t+=" label-is-floating"),t)},_valueChanged:function(){this.$.input&&this.$.input.textContent!==this.value&&(this.$.input.textContent=this.value),this._setHasContent(!!this.value)}})}}]);
//# sourceMappingURL=1aa83272dab571d4a597.chunk.js.map