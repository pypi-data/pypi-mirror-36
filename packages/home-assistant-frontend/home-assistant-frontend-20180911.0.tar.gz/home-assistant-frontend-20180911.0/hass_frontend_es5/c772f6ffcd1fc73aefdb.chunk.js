/*! For license information please see c772f6ffcd1fc73aefdb.chunk.js.LICENSE */
(window.webpackJsonp=window.webpackJsonp||[]).push([[46],{204:function(e,n,t){"use strict";t.d(n,"b",function(){return r}),t.d(n,"a",function(){return o}),t(2);var a=t(54),i=t(1),r={hostAttributes:{role:"dialog",tabindex:"-1"},properties:{modal:{type:Boolean,value:!1},__readied:{type:Boolean,value:!1}},observers:["_modalChanged(modal, __readied)"],listeners:{tap:"_onDialogClick"},ready:function(){this.__prevNoCancelOnOutsideClick=this.noCancelOnOutsideClick,this.__prevNoCancelOnEscKey=this.noCancelOnEscKey,this.__prevWithBackdrop=this.withBackdrop,this.__readied=!0},_modalChanged:function(e,n){n&&(e?(this.__prevNoCancelOnOutsideClick=this.noCancelOnOutsideClick,this.__prevNoCancelOnEscKey=this.noCancelOnEscKey,this.__prevWithBackdrop=this.withBackdrop,this.noCancelOnOutsideClick=!0,this.noCancelOnEscKey=!0,this.withBackdrop=!0):(this.noCancelOnOutsideClick=this.noCancelOnOutsideClick&&this.__prevNoCancelOnOutsideClick,this.noCancelOnEscKey=this.noCancelOnEscKey&&this.__prevNoCancelOnEscKey,this.withBackdrop=this.withBackdrop&&this.__prevWithBackdrop))},_updateClosingReasonConfirmed:function(e){this.closingReason=this.closingReason||{},this.closingReason.confirmed=e},_onDialogClick:function(e){for(var n=Object(i.b)(e).path,t=0,a=n.indexOf(this);t<a;t++){var r=n[t];if(r.hasAttribute&&(r.hasAttribute("dialog-dismiss")||r.hasAttribute("dialog-confirm"))){this._updateClosingReasonConfirmed(r.hasAttribute("dialog-confirm")),this.close(),e.stopPropagation();break}}}},o=[a.a,r]},207:function(e,n,t){"use strict";t(2),t(27),t(30),t(43),t(64);var a=document.createElement("template");a.setAttribute("style","display: none;"),a.innerHTML='<dom-module id="paper-dialog-shared-styles">\n  <template>\n    <style>\n      :host {\n        display: block;\n        margin: 24px 40px;\n\n        background: var(--paper-dialog-background-color, var(--primary-background-color));\n        color: var(--paper-dialog-color, var(--primary-text-color));\n\n        @apply --paper-font-body1;\n        @apply --shadow-elevation-16dp;\n        @apply --paper-dialog;\n      }\n\n      :host > ::slotted(*) {\n        margin-top: 20px;\n        padding: 0 24px;\n      }\n\n      :host > ::slotted(.no-padding) {\n        padding: 0;\n      }\n\n      \n      :host > ::slotted(*:first-child) {\n        margin-top: 24px;\n      }\n\n      :host > ::slotted(*:last-child) {\n        margin-bottom: 24px;\n      }\n\n      /* In 1.x, this selector was `:host > ::content h2`. In 2.x <slot> allows\n      to select direct children only, which increases the weight of this\n      selector, so we have to re-define first-child/last-child margins below. */\n      :host > ::slotted(h2) {\n        position: relative;\n        margin: 0;\n\n        @apply --paper-font-title;\n        @apply --paper-dialog-title;\n      }\n\n      /* Apply mixin again, in case it sets margin-top. */\n      :host > ::slotted(h2:first-child) {\n        margin-top: 24px;\n        @apply --paper-dialog-title;\n      }\n\n      /* Apply mixin again, in case it sets margin-bottom. */\n      :host > ::slotted(h2:last-child) {\n        margin-bottom: 24px;\n        @apply --paper-dialog-title;\n      }\n\n      :host > ::slotted(.paper-dialog-buttons),\n      :host > ::slotted(.buttons) {\n        position: relative;\n        padding: 8px 8px 8px 24px;\n        margin: 0;\n\n        color: var(--paper-dialog-button-color, var(--primary-color));\n\n        @apply --layout-horizontal;\n        @apply --layout-end-justified;\n      }\n    </style>\n  </template>\n</dom-module>',document.head.appendChild(a.content)},214:function(e,n,t){"use strict";t(2);var a=t(95),i=t(204),r=(t(207),t(3)),o=t(0),s=Object.freeze(Object.defineProperties(['\n    <style include="paper-dialog-shared-styles"></style>\n    <slot></slot>\n'],{raw:{value:Object.freeze(['\n    <style include="paper-dialog-shared-styles"></style>\n    <slot></slot>\n'])}}));Object(r.a)({_template:Object(o.a)(s),is:"paper-dialog",behaviors:[i.a,a.a],listeners:{"neon-animation-finish":"_onNeonAnimationFinish"},_renderOpened:function(){this.cancelAnimation(),this.playAnimation("entry")},_renderClosed:function(){this.cancelAnimation(),this.playAnimation("exit")},_onNeonAnimationFinish:function(){this.opened?this._finishRenderOpened():this._finishRenderClosed()}})},631:function(e,n,t){"use strict";t.r(n),t(55),t(214),t(125);var a=t(0),i=t(4),r=(t(121),t(13)),o=function(){function e(e,n){for(var t=0;t<n.length;t++){var a=n[t];a.enumerable=a.enumerable||!1,a.configurable=!0,"value"in a&&(a.writable=!0),Object.defineProperty(e,a.key,a)}}return function(n,t,a){return t&&e(n.prototype,t),a&&e(n,a),n}}(),s=Object.freeze(Object.defineProperties(["\n    <style include=\"ha-style-dialog\">\n      .error {\n        color: red;\n      }\n      paper-dialog {\n        max-width: 500px;\n      }\n      .username {\n        margin-top: -8px;\n      }\n    </style>\n    <paper-dialog id=\"dialog\" with-backdrop opened=\"{{_opened}}\" on-opened-changed=\"_openedChanged\">\n      <h2>Add user</h2>\n      <div>\n        <template is=\"dom-if\" if=\"[[_errorMsg]]\">\n          <div class='error'>[[_errorMsg]]</div>\n        </template>\n        <paper-input\n          class='name'\n          label='Name'\n          value='{{_name}}'\n          required\n          auto-validate\n          autocapitalize='on'\n          error-message='Required'\n          on-blur='_maybePopulateUsername'\n        ></paper-input>\n        <paper-input\n          class='username'\n          label='Username'\n          value='{{_username}}'\n          required\n          auto-validate\n          autocapitalize='none'\n          error-message='Required'\n        ></paper-input>\n        <paper-input\n          label='Password'\n          type='password'\n          value='{{_password}}'\n          required\n          auto-validate\n          error-message='Required'\n        ></paper-input>\n      </div>\n      <div class=\"buttons\">\n        <template is=\"dom-if\" if=\"[[_loading]]\">\n          <div class='submit-spinner'><paper-spinner active></paper-spinner></div>\n        </template>\n        <template is=\"dom-if\" if=\"[[!_loading]]\">\n          <paper-button on-click=\"_createUser\">Create</paper-button>\n        </template>\n      </div>\n    </paper-dialog>\n"],{raw:{value:Object.freeze(["\n    <style include=\"ha-style-dialog\">\n      .error {\n        color: red;\n      }\n      paper-dialog {\n        max-width: 500px;\n      }\n      .username {\n        margin-top: -8px;\n      }\n    </style>\n    <paper-dialog id=\"dialog\" with-backdrop opened=\"{{_opened}}\" on-opened-changed=\"_openedChanged\">\n      <h2>Add user</h2>\n      <div>\n        <template is=\"dom-if\" if=\"[[_errorMsg]]\">\n          <div class='error'>[[_errorMsg]]</div>\n        </template>\n        <paper-input\n          class='name'\n          label='Name'\n          value='{{_name}}'\n          required\n          auto-validate\n          autocapitalize='on'\n          error-message='Required'\n          on-blur='_maybePopulateUsername'\n        ></paper-input>\n        <paper-input\n          class='username'\n          label='Username'\n          value='{{_username}}'\n          required\n          auto-validate\n          autocapitalize='none'\n          error-message='Required'\n        ></paper-input>\n        <paper-input\n          label='Password'\n          type='password'\n          value='{{_password}}'\n          required\n          auto-validate\n          error-message='Required'\n        ></paper-input>\n      </div>\n      <div class=\"buttons\">\n        <template is=\"dom-if\" if=\"[[_loading]]\">\n          <div class='submit-spinner'><paper-spinner active></paper-spinner></div>\n        </template>\n        <template is=\"dom-if\" if=\"[[!_loading]]\">\n          <paper-button on-click=\"_createUser\">Create</paper-button>\n        </template>\n      </div>\n    </paper-dialog>\n"])}})),l=function(e){function n(){return function(e,t){if(!(e instanceof n))throw new TypeError("Cannot call a class as a function")}(this),function(e,n){if(!e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return!n||"object"!=typeof n&&"function"!=typeof n?e:n}(this,(n.__proto__||Object.getPrototypeOf(n)).apply(this,arguments))}return function(e,n){if("function"!=typeof n&&null!==n)throw new TypeError("Super expression must either be null or a function, not "+typeof n);e.prototype=Object.create(n&&n.prototype,{constructor:{value:e,enumerable:!1,writable:!0,configurable:!0}}),n&&(Object.setPrototypeOf?Object.setPrototypeOf(e,n):e.__proto__=n)}(n,Object(r.a)(i.a)),o(n,[{key:"ready",value:function(){var e=this;(function e(n,t,a){null===n&&(n=Function.prototype);var i=Object.getOwnPropertyDescriptor(n,t);if(void 0===i){var r=Object.getPrototypeOf(n);return null===r?void 0:e(r,t,a)}if("value"in i)return i.value;var o=i.get;return void 0!==o?o.call(a):void 0})(n.prototype.__proto__||Object.getPrototypeOf(n.prototype),"ready",this).call(this),this.addEventListener("keypress",function(n){13===n.keyCode&&e._createUser()})}},{key:"showDialog",value:function(e){var n=this,t=e.hass,a=e.dialogClosedCallback;this.hass=t,this._dialogClosedCallback=a,this._loading=!1,this._opened=!0,setTimeout(function(){return n.shadowRoot.querySelector("paper-input").focus()},0)}},{key:"_maybePopulateUsername",value:function(){if(!this._username){var e=this._name.split(" ");e.length&&(this._username=e[0].toLowerCase())}}},{key:"_createUser",value:(t=regeneratorRuntime.mark(function e(){var n,t;return regeneratorRuntime.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:if(this._name&&this._username&&this._password){e.next=2;break}return e.abrupt("return");case 2:return this._loading=!0,this._errorMsg=null,n=void 0,e.prev=5,e.next=8,this.hass.callWS({type:"config/auth/create",name:this._name});case 8:t=e.sent,n=t.user.id,e.next=17;break;case 12:return e.prev=12,e.t0=e.catch(5),this._loading=!1,this._errorMsg=e.t0.code,e.abrupt("return");case 17:return e.prev=17,e.next=20,this.hass.callWS({type:"config/auth_provider/homeassistant/create",user_id:n,username:this._username,password:this._password});case 20:e.next=29;break;case 22:return e.prev=22,e.t1=e.catch(17),this._loading=!1,this._errorMsg=e.t1.code,e.next=28,this.hass.callWS({type:"config/auth/delete",user_id:n});case 28:return e.abrupt("return");case 29:this._dialogDone(n);case 30:case"end":return e.stop()}},e,this,[[5,12],[17,22]])}),l=function(){var e=t.apply(this,arguments);return new Promise(function(n,t){return function a(i,r){try{var o=e[i](r),s=o.value}catch(e){return void t(e)}if(!o.done)return Promise.resolve(s).then(function(e){a("next",e)},function(e){a("throw",e)});n(s)}("next")})},function(){return l.apply(this,arguments)})},{key:"_dialogDone",value:function(e){this._dialogClosedCallback({userId:e}),this.setProperties({_errorMsg:null,_username:"",_password:"",_dialogClosedCallback:null,_opened:!1})}},{key:"_equals",value:function(e,n){return e===n}},{key:"_openedChanged",value:function(e){this._dialogClosedCallback&&!e.detail.value&&this._dialogDone()}}],[{key:"template",get:function(){return Object(a.a)(s)}},{key:"properties",get:function(){return{_hass:Object,_dialogClosedCallback:Function,_loading:{type:Boolean,value:!1},_errorMsg:String,_opened:{type:Boolean,value:!1},_name:String,_username:String,_password:String}}}]),n;var t,l}();customElements.define("ha-dialog-add-user",l)}}]);
//# sourceMappingURL=c772f6ffcd1fc73aefdb.chunk.js.map