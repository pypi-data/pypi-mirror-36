(window.webpackJsonp=window.webpackJsonp||[]).push([[56],{617:function(e,o,t){"use strict";t.r(o),t(220),t(210);var a=t(0),s=t(4),l=(t(121),t(14));customElements.define("ha-loaded-components",class extends(Object(l.a)(s.a)){static get template(){return a["a"]`
    <style include="ha-style-dialog">
      paper-dialog {
        max-width: 500px;
      }
    </style>
    <paper-dialog id="dialog" with-backdrop="" opened="{{_opened}}">
      <h2>Loaded Components</h2>
      <paper-dialog-scrollable id="scrollable">
       <p>The following components are currently loaded:</p>
       <ul>
        <template is='dom-repeat' items='[[_components]]'>
          <li>[[item]]</li>
        </template>
       </ul>
      </paper-dialog-scrollable>
    </paper-dialog>
    `}static get properties(){return{_hass:Object,_components:Array,_opened:{type:Boolean,value:!1}}}ready(){super.ready()}showDialog({hass:e}){this.hass=e,this._opened=!0,this._components=this.hass.config.components.sort(),setTimeout(()=>this.$.dialog.center(),0)}})}}]);
//# sourceMappingURL=b2a776f0eace80de0f03.chunk.js.map