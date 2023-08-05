(window.webpackJsonp=window.webpackJsonp||[]).push([[19],{632:function(e,a,t){"use strict";t.r(a),t(89),t(137);var i=t(0),s=t(4),o=(t(168),t(136)),n=t(81);Promise.all([t.e(0),t.e(1),t.e(4),t.e(5),t.e(47)]).then(t.bind(null,619)),t.e(48).then(t.bind(null,623)),t.e(49).then(t.bind(null,622)),t.e(50).then(t.bind(null,626)),t.e(51).then(t.bind(null,620)),t.e(52).then(t.bind(null,627)),Promise.all([t.e(0),t.e(1),t.e(4),t.e(5),t.e(53)]).then(t.bind(null,624)),t.e(54).then(t.bind(null,625)),t.e(55).then(t.bind(null,621)),customElements.define("ha-panel-config",class extends(Object(n.a)(s.a)){static get template(){return i["a"]`
    <app-route
      route='[[route]]'
      pattern='/:page'
      data="{{_routeData}}"
    ></app-route>

    <iron-media-query query="(min-width: 1040px)" query-matches="{{wide}}">
    </iron-media-query>
    <iron-media-query query="(min-width: 1296px)" query-matches="{{wideSidebar}}">
    </iron-media-query>

    <template is="dom-if" if='[[_equals(_routeData.page, "core")]]' restamp>
      <ha-config-core
        page-name='core'
        hass='[[hass]]'
        is-wide='[[isWide]]'
      ></ha-config-core>
    </template>

    <template is="dom-if" if='[[_equals(_routeData.page, "cloud")]]' restamp>
      <ha-config-cloud
        page-name='cloud'
        route='[[route]]'
        hass='[[hass]]'
        is-wide='[[isWide]]'
        account='[[account]]'
      ></ha-config-cloud>
    </template>

    <template is="dom-if" if='[[_equals(_routeData.page, "dashboard")]]'>
      <ha-config-dashboard
        page-name='dashboard'
        hass='[[hass]]'
        is-wide='[[isWide]]'
        account='[[account]]'
        narrow='[[narrow]]'
        show-menu='[[showMenu]]'
      ></ha-config-dashboard>
    </template>

    <template is="dom-if" if='[[_equals(_routeData.page, "automation")]]' restamp>
      <ha-config-automation
        page-name='automation'
        route='[[route]]'
        hass='[[hass]]'
        is-wide='[[isWide]]'
      ></ha-config-automation>
    </template>

    <template is="dom-if" if='[[_equals(_routeData.page, "script")]]' restamp>
      <ha-config-script
        page-name='script'
        route='[[route]]'
        hass='[[hass]]'
        is-wide='[[isWide]]'
      ></ha-config-script>
    </template>

    <template is="dom-if" if='[[_equals(_routeData.page, "zwave")]]' restamp>
      <ha-config-zwave
        page-name='zwave'
        hass='[[hass]]'
        is-wide='[[isWide]]'
      ></ha-config-zwave>
    </template>

    <template is="dom-if" if='[[_equals(_routeData.page, "customize")]]' restamp>
      <ha-config-customize
        page-name='customize'
        hass='[[hass]]'
        is-wide='[[isWide]]'
      ></ha-config-customize>
    </template>

    <template is="dom-if" if='[[_equals(_routeData.page, "integrations")]]' restamp>
      <ha-config-entries
        route='[[route]]'
        page-name='integrations'
        hass='[[hass]]'
        is-wide='[[isWide]]'
      ></ha-config-entries>
    </template>

    <template is="dom-if" if='[[_equals(_routeData.page, "users")]]' restamp>
      <ha-config-users
        page-name='users'
        route='[[route]]'
        hass='[[hass]]'
      ></ha-config-users>
    </template>
    `}static get properties(){return{hass:Object,narrow:Boolean,showMenu:Boolean,account:{type:Object,value:null},route:{type:Object,observer:"_routeChanged"},_routeData:Object,wide:Boolean,wideSidebar:Boolean,isWide:{type:Boolean,computed:"computeIsWide(showMenu, wideSidebar, wide)"}}}ready(){super.ready(),Object(o.a)(this.hass,"cloud")&&this.hass.callApi("get","cloud/account").then(e=>{this.account=e},()=>{}),this.addEventListener("ha-account-refreshed",e=>{this.account=e.detail.account})}computeIsWide(e,a,t){return e?a:t}_routeChanged(e){""===e.path&&"/config"===e.prefix&&this.navigate("/config/dashboard",!0)}_equals(e,a){return e===a}})}}]);
//# sourceMappingURL=5e44981ff689b50c888b.chunk.js.map