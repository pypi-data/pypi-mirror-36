(window.webpackJsonp=window.webpackJsonp||[]).push([[38],{614:function(e,t,a){"use strict";a.r(t);var s=a(0),n=a(4),i=a(13);customElements.define("notification-manager",class extends(Object(i.a)(n.a)){static get template(){return s["a"]`
    <style>
      paper-toast {
        z-index: 1;
      }
    </style>

    <ha-toast
      id="toast"
      no-cancel-on-outside-click="[[_cancelOnOutsideClick]]"
    ></ha-toast>
`}static get properties(){return{hass:Object,_cancelOnOutsideClick:{type:Boolean,value:!1}}}ready(){super.ready(),a.e(39).then(a.bind(null,275))}showDialog({message:e}){this.$.toast.show(e)}})}}]);
//# sourceMappingURL=6f0757c1ec2878b3fa38.chunk.js.map