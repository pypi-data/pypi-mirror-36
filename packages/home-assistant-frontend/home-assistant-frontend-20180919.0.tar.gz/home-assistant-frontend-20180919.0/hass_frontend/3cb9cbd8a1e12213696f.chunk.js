(window.webpackJsonp=window.webpackJsonp||[]).push([[34],{654:function(e,t,a){"use strict";a.r(t),a(155),a(154),a(153),a(197),a(120),a(55),a(122);var s=a(0),r=a(4),o=(a(135),a(121),a(14));a(210),a(125),customElements.define("ha-change-password-card",class extends r.a{static get template(){return s["a"]`
    <style include="ha-style">
      .error {
        color: red;
      }
      .status {
        color: var(--primary-color);
      }
      .error, .status {
        position: absolute;
        top: -4px;
      }
      paper-card {
        display: block;
      }
      .currentPassword {
        margin-top: -4px;
      }
    </style>
    <div>
      <paper-card heading="Change Password">
        <div class="card-content">
          <template is="dom-if" if="[[_errorMsg]]">
            <div class='error'>[[_errorMsg]]</div>
          </template>
          <template is="dom-if" if="[[_statusMsg]]">
            <div class="status">[[_statusMsg]]</div>
          </template>
          <paper-input
            class='currentPassword'
            label='Current Password'
            type='password'
            value='{{_currentPassword}}'
            required
            auto-validate
            error-message='Required'
          ></paper-input>
          <template is='dom-if' if='[[_currentPassword]]'>
            <paper-input
              label='New Password'
              type='password'
              value='{{_password1}}'
              required
              auto-validate
              error-message='Required'
            ></paper-input>
            <paper-input
              label='Confirm New Password'
              type='password'
              value='{{_password2}}'
              required
              auto-validate
              error-message='Required'
            ></paper-input>
          </template>
        </div>
        <div class="card-actions">
          <template is="dom-if" if="[[_loading]]">
            <div><paper-spinner active></paper-spinner></div>
          </template>
          <template is="dom-if" if="[[!_loading]]">
            <paper-button on-click="_changePassword">Submit</paper-button>
          </template>
        </div>
      </paper-card>
    </div>
`}static get properties(){return{hass:Object,_loading:{type:Boolean,value:!1},_statusMsg:String,_errorMsg:String,_currentPassword:String,_password1:String,_password2:String}}ready(){super.ready(),this.addEventListener("keypress",e=>{this._statusMsg=null,13===e.keyCode&&this._changePassword()})}async _changePassword(){if(this._statusMsg=null,this._currentPassword&&this._password1&&this._password2)if(this._password1===this._password2)if(this._currentPassword!==this._password1){this._loading=!0,this._errorMsg=null;try{await this.hass.callWS({type:"config/auth_provider/homeassistant/change_password",current_password:this._currentPassword,new_password:this._password1}),this.setProperties({_statusMsg:"Password changed successfully",_currentPassword:null,_password1:null,_password2:null})}catch(e){this._errorMsg=e.message}this._loading=!1}else this._errorMsg="New password must be different than current password";else this._errorMsg="New password confirmation doesn't match"}});var i=a(13);let n=!1;customElements.define("ha-mfa-modules-card",class extends(Object(o.a)(Object(i.a)(r.a))){static get template(){return s["a"]`
    <style include="iron-flex ha-style">
      .error {
        color: red;
      }
      .status {
        color: var(--primary-color);
      }
      .error, .status {
        position: absolute;
        top: -4px;
      }
      paper-card {
        display: block;
        max-width: 600px;
        margin: 16px auto;
      }
      paper-button {
        color: var(--primary-color);
        font-weight: 500;
        margin-right: -.57em;
      }
    </style>
    <paper-card heading="Multi-factor Authentication Modules">
      <template is="dom-repeat" items="[[mfaModules]]" as="module">
        <paper-item>
          <paper-item-body two-line="">
            <div>[[module.name]]</div>
            <div secondary="">[[module.id]]</div>
          </paper-item-body>
          <template is="dom-if" if="[[module.enabled]]">
            <paper-button on-click="_disable">Disable</paper-button>
          </template>
          <template is="dom-if" if="[[!module.enabled]]">
            <paper-button on-click="_enable">Enable</paper-button>
          </template>
        </paper-item>
      </template>
    </paper-card>
`}static get properties(){return{hass:Object,_loading:{type:Boolean,value:!1},_statusMsg:String,_errorMsg:String,mfaModules:Array}}connectedCallback(){super.connectedCallback(),n||(n=!0,this.fire("register-dialog",{dialogShowEvent:"show-mfa-module-setup-flow",dialogTag:"ha-mfa-module-setup-flow",dialogImport:()=>a.e(58).then(a.bind(null,649))}))}_enable(e){this.fire("show-mfa-module-setup-flow",{hass:this.hass,mfaModuleId:e.model.module.id,dialogClosedCallback:()=>this._refreshCurrentUser()})}_disable(e){if(!confirm(`Are you sure you want to disable ${e.model.module.name}?`))return;const t=e.model.module.id;this.hass.callWS({type:"auth/depose_mfa",mfa_module_id:t}).then(()=>{this._refreshCurrentUser()})}_refreshCurrentUser(){this.fire("hass-refresh-current-user")}}),a(62),a(257);var l=a(77);customElements.define("ha-settings-row",class extends r.a{static get template(){return s["a"]`
    <style>
      :host {
        display: flex;
        padding: 0 16px;
        align-content: normal;
        align-self: auto;
        align-items: center;
      }
      :host([narrow]) {
        align-items: normal;
        flex-direction: column;
        border-top: 1px solid var(--divider-color);
        padding-bottom: 8px;
      }
      paper-item-body {
        padding-right: 16px;
      }
    </style>
    <paper-item-body two-line$='[[!threeLine]]' three-line$='[[threeLine]]'>
      <slot name="heading"></slot>
      <div secondary><slot name="description"></slot></div>
    </paper-item-body>
    <slot></slot>
    `}static get properties(){return{narrow:{type:Boolean,reflectToAttribute:!0},threeLine:{type:Boolean,value:!1}}}}),customElements.define("ha-refresh-tokens-card",class extends(Object(i.a)(Object(o.a)(r.a))){static get template(){return s["a"]`
    <style>
      paper-card {
        display: block;
      }
      paper-icon-button {
        color: var(--primary-text-color);
      }
      paper-icon-button[disabled] {
        color: var(--disabled-text-color);
      }
    </style>
    <paper-card heading="[[localize('ui.panel.profile.refresh_tokens.header')]]">
      <div class="card-content">[[localize('ui.panel.profile.refresh_tokens.description')]]</div>
      <template is='dom-repeat' items='[[_computeTokens(refreshTokens)]]'>
        <ha-settings-row three-line>
          <span slot='heading'>[[_formatTitle(item.client_id)]]</span>
          <div slot='description'>[[_formatCreatedAt(item.created_at)]]</div>
          <div slot='description'>[[_formatLastUsed(item)]]</div>
          <div>
            <template is='dom-if' if='[[item.is_current]]'>
              <paper-tooltip
                position="left"
              >[[localize('ui.panel.profile.refresh_tokens.current_token_tooltip')]]</paper-tooltip>
            </template>
            <paper-icon-button
              icon="hass:delete"
              on-click='_handleDelete'
              disabled="[[item.is_current]]"
            ></paper-icon-button>
          </div>
        </ha-settings-row>
      </template>
    </paper-card>
    `}static get properties(){return{hass:Object,refreshTokens:Array}}_computeTokens(e){return e.filter(e=>"normal"===e.type).reverse()}_formatTitle(e){return this.localize("ui.panel.profile.refresh_tokens.token_title","clientId",e)}_formatCreatedAt(e){return this.localize("ui.panel.profile.refresh_tokens.created_at","date",Object(l.a)(new Date(e)))}_formatLastUsed(e){return e.last_used_at?this.localize("ui.panel.profile.refresh_tokens.last_used","date",Object(l.a)(new Date(e.last_used_at)),"location",e.last_used_ip):this.localize("ui.panel.profile.refresh_tokens.not_used")}async _handleDelete(e){if(confirm(this.localize("ui.panel.profile.refresh_tokens.confirm_delete","name",e.model.item.client_id)))try{await this.hass.callWS({type:"auth/delete_refresh_token",refresh_token_id:e.model.item.id}),this.fire("hass-refresh-tokens")}catch(e){console.error(e),alert(this.localize("ui.panel.profile.refresh_tokens.delete_failed"))}}}),customElements.define("ha-long-lived-access-tokens-card",class extends(Object(i.a)(Object(o.a)(r.a))){static get template(){return s["a"]`
    <style include="ha-style">
      paper-card {
        display: block;
      }
      .card-content {
        margin: -1em 0;
      }
      a {
        color: var(--primary-color);
      }
      paper-icon-button {
        color: var(--primary-text-color);
      }
    </style>
    <paper-card heading="[[localize('ui.panel.profile.long_lived_access_tokens.header')]]">
      <div class="card-content">
        <p>
          [[localize('ui.panel.profile.long_lived_access_tokens.description')]]
          <a href='https://developers.home-assistant.io/docs/en/auth_api.html#making-authenticated-requests' target='_blank'>
            [[localize('ui.panel.profile.long_lived_access_tokens.learn_auth_requests')]]
          </a>
        </p>
        <template is='dom-if' if='[[!_tokens.length]]'>
          <p>[[localize('ui.panel.profile.long_lived_access_tokens.empty_state')]]</p>
        </template>
      </div>
      <template is='dom-repeat' items='[[_tokens]]'>
        <ha-settings-row three-line>
          <span slot='heading'>[[item.client_name]]</span>
          <div slot='description'>[[_formatCreatedAt(item.created_at)]]</div>
          <div slot='description'>[[_formatLastUsed(item)]]</div>
          <paper-icon-button icon="hass:delete" on-click='_handleDelete'></paper-icon-button>
        </ha-settings-row>
      </template>
      <div class='card-actions'>
        <paper-button on-click='_handleCreate'>
          [[localize('ui.panel.profile.long_lived_access_tokens.create')]]
        </paper-button>
      </div>
    </paper-card>
    `}static get properties(){return{hass:Object,refreshTokens:Array,_tokens:{type:Array,computed:"_computeTokens(refreshTokens)"}}}_computeTokens(e){return e.filter(e=>"long_lived_access_token"===e.type).reverse()}_formatTitle(e){return this.localize("ui.panel.profile.long_lived_access_tokens.token_title","name",e)}_formatCreatedAt(e){return this.localize("ui.panel.profile.long_lived_access_tokens.created_at","date",Object(l.a)(new Date(e)))}_formatLastUsed(e){return e.last_used_at?this.localize("ui.panel.profile.refresh_tokens.last_used","date",Object(l.a)(new Date(e.last_used_at)),"location",e.last_used_ip):this.localize("ui.panel.profile.refresh_tokens.not_used")}async _handleCreate(){const e=prompt(this.localize("ui.panel.profile.long_lived_access_tokens.prompt_name"));if(e)try{const t=await this.hass.callWS({type:"auth/long_lived_access_token",lifespan:3650,client_name:e});prompt(this.localize("ui.panel.profile.long_lived_access_tokens.prompt_copy_token"),t),this.fire("hass-refresh-tokens")}catch(e){console.error(e),alert(this.localize("ui.panel.profile.long_lived_access_tokens.create_failed"))}}async _handleDelete(e){if(confirm(this.localize("ui.panel.profile.long_lived_access_tokens.confirm_delete","name",e.model.item.client_name)))try{await this.hass.callWS({type:"auth/delete_refresh_token",refresh_token_id:e.model.item.id}),this.fire("hass-refresh-tokens")}catch(e){console.error(e),alert(this.localize("ui.panel.profile.long_lived_access_tokens.delete_failed"))}}}),a(124),a(123),customElements.define("ha-pick-language-row",class extends(Object(i.a)(Object(o.a)(r.a))){static get template(){return s["a"]`
    <style>
      a { color: var(--primary-color); }
    </style>
    <ha-settings-row narrow='[[narrow]]'>
      <span slot='heading'>[[localize('ui.panel.profile.language.header')]]</span>
      <span slot='description'>
        <a
          href='https://developers.home-assistant.io/docs/en/internationalization_translation.html'
          target='_blank'>[[localize('ui.panel.profile.language.link_promo')]]</a>
      </span>
      <paper-dropdown-menu label="[[localize('ui.panel.profile.language.dropdown_label')]]" dynamic-align="">
        <paper-listbox slot="dropdown-content" attr-for-selected="language-tag" selected="{{languageSelection}}">
          <template is="dom-repeat" items="[[languages]]">
            <paper-item language-tag$="[[item.tag]]">[[item.nativeName]]</paper-item>
          </template>
        </paper-listbox>
      </paper-dropdown-menu>
    </ha-settings-row>
    `}static get properties(){return{hass:Object,narrow:Boolean,languageSelection:{type:String,observer:"languageSelectionChanged"},languages:{type:Array,computed:"computeLanguages(hass)"}}}static get observers(){return["setLanguageSelection(language)"]}computeLanguages(e){return e&&e.translationMetadata?Object.keys(e.translationMetadata.translations).map(t=>({tag:t,nativeName:e.translationMetadata.translations[t].nativeName})):[]}setLanguageSelection(e){this.languageSelection=e}languageSelectionChanged(e){e!==this.language&&this.fire("hass-language-select",{language:e})}}),customElements.define("ha-pick-theme-row",class extends(Object(i.a)(Object(o.a)(r.a))){static get template(){return s["a"]`
    <style>
      a { color: var(--primary-color); }
    </style>
    <ha-settings-row narrow='[[narrow]]'>
      <span slot='heading'>[[localize('ui.panel.profile.themes.header')]]</span>
      <span slot='description'>
        <template is='dom-if' if='[[!_hasThemes]]'>
        [[localize('ui.panel.profile.themes.error_no_theme')]]
        </template>
        <a
          href='https://www.home-assistant.io/components/frontend/#defining-themes'
          target='_blank'>[[localize('ui.panel.profile.themes.link_promo')]]</a>
      </span>
      <paper-dropdown-menu
        label="[[localize('ui.panel.profile.themes.dropdown_label')]]"
        dynamic-align
        disabled='[[!_hasThemes]]'
      >
        <paper-listbox slot="dropdown-content" selected="{{selectedTheme}}">
          <template is="dom-repeat" items="[[themes]]" as="theme">
            <paper-item>[[theme]]</paper-item>
          </template>
        </paper-listbox>
      </paper-dropdown-menu>
    </ha-settings-row>
    `}static get properties(){return{hass:Object,narrow:Boolean,_hasThemes:{type:Boolean,computed:"_compHasThemes(hass)"},themes:{type:Array,computed:"_computeThemes(hass)"},selectedTheme:{type:Number}}}static get observers(){return["selectionChanged(hass, selectedTheme)"]}_compHasThemes(e){return e.themes&&e.themes.themes&&Object.keys(e.themes.themes).length}ready(){super.ready(),this.hass.selectedTheme&&this.themes.indexOf(this.hass.selectedTheme)>0?this.selectedTheme=this.themes.indexOf(this.hass.selectedTheme):this.hass.selectedTheme||(this.selectedTheme=0)}_computeThemes(e){return e?["Backend-selected","default"].concat(Object.keys(e.themes.themes).sort()):[]}selectionChanged(e,t){t>0&&t<this.themes.length?e.selectedTheme!==this.themes[t]&&this.fire("settheme",this.themes[t]):0===t&&""!==e.selectedTheme&&this.fire("settheme","")}}),a(31),a(441);var p=a(136);a(159);const c="serviceWorker"in navigator&&"PushManager"in window&&("https:"===document.location.protocol||"localhost"===document.location.hostname||"127.0.0.1"===document.location.hostname);customElements.define("ha-push-notifications-toggle",class extends(Object(o.a)(r.a)){static get template(){return s["a"]`
    <paper-toggle-button
      disabled="[[_compDisabled(disabled, loading)]]"
      checked="{{pushChecked}}"
    ></paper-toggle-button>
`}static get properties(){return{hass:{type:Object,value:null},disabled:{type:Boolean,value:!1},pushChecked:{type:Boolean,value:"Notification"in window&&"granted"===Notification.permission,observer:"handlePushChange"},loading:{type:Boolean,value:!0}}}async connectedCallback(){if(super.connectedCallback(),c)try{const e=await navigator.serviceWorker.ready;if(!e.pushManager)return;e.pushManager.getSubscription().then(e=>{this.loading=!1,this.pushChecked=!!e})}catch(e){}}handlePushChange(e){c&&(e?this.subscribePushNotifications():this.unsubscribePushNotifications())}async subscribePushNotifications(){const e=await navigator.serviceWorker.ready;try{const t=await e.pushManager.subscribe({userVisibleOnly:!0});let a;a=navigator.userAgent.toLowerCase().indexOf("firefox")>-1?"firefox":"chrome",await this.hass.callApi("POST","notify.html5",{subscription:t,browser:a})}catch(e){const t=e.message||"Notification registration failed.";console.error(e),this.fire("hass-notification",{message:t}),this.pushChecked=!1}}async unsubscribePushNotifications(){const e=await navigator.serviceWorker.ready;try{const t=await e.pushManager.getSubscription();if(!t)return;await this.hass.callApi("DELETE","notify.html5",{subscription:t}),await t.unsubscribe()}catch(e){const t=e.message||"Failed unsubscribing for push notifications.";console.error("Error in unsub push",e),this.fire("hass-notification",{message:t}),this.pushChecked=!0}}_compDisabled(e,t){return e||t}}),customElements.define("ha-push-notifications-row",class extends(Object(i.a)(r.a)){static get template(){return s["a"]`
    <style>
      a { color: var(--primary-color); }
    </style>
    <ha-settings-row narrow='[[narrow]]'>
      <span slot='heading'>[[localize('ui.panel.profile.push_notifications.header')]]</span>
      <span
        slot='description'
      >
        [[_description(_platformLoaded, _pushSupported)]]
        <a
          href='https://www.home-assistant.io/components/notify.html5/'
          target='_blank'>[[localize('ui.panel.profile.push_notifications.link_promo')]]</a>
      </span>
      <ha-push-notifications-toggle
        hass="[[hass]]"
        disabled='[[_error]]'
      ></ha-push-notifications-toggle>
    </ha-settings-row>
    `}static get properties(){return{hass:Object,narrow:Boolean,_platformLoaded:{type:Boolean,computed:"_compPlatformLoaded(hass)"},_pushSupported:{type:Boolean,value:c},_error:{type:Boolean,computed:"_compError(_platformLoaded, _pushSupported)"}}}_compPlatformLoaded(e){return Object(p.a)(e,"notify.html5")}_compError(e,t){return!e||!t}_description(e,t){let a;return a=t?e?"description":"error_load_platform":"error_use_https",this.localize(`ui.panel.profile.push_notifications.${a}`)}}),customElements.define("ha-panel-profile",class extends(Object(o.a)(r.a)){static get template(){return s["a"]`
    <style include="ha-style">
      :host {
        -ms-user-select: initial;
        -webkit-user-select: initial;
        -moz-user-select: initial;
      }

      .content {
        display: block;
        max-width: 600px;
        margin: 0 auto;
      }

      .content > * {
        display: block;
        margin: 24px 0;
      }
    </style>

    <app-header-layout has-scrolling-region>
      <app-header slot="header" fixed>
        <app-toolbar>
          <ha-menu-button narrow='[[narrow]]' show-menu='[[showMenu]]'></ha-menu-button>
          <div main-title>Profile</div>
        </app-toolbar>
      </app-header>

      <div class='content'>
        <paper-card heading='[[hass.user.name]]'>
          <div class='card-content'>
            You are currently logged in as [[hass.user.name]].
            <template is='dom-if' if='[[hass.user.is_owner]]'>You are an owner.</template>
          </div>

          <ha-pick-language-row
            narrow="[[narrow]]"
            hass="[[hass]]"
          ></ha-pick-language-row>
          <ha-pick-theme-row
            narrow="[[narrow]]"
            hass="[[hass]]"
          ></ha-pick-theme-row>
          <ha-push-notifications-row
            narrow="[[narrow]]"
            hass="[[hass]]"
          ></ha-push-notifications-row>

          <div class='card-actions'>
            <paper-button
              class='warning'
              on-click='_handleLogOut'
            >Log out</paper-button>
          </div>
        </paper-card>

        <template is="dom-if" if="[[_canChangePassword(hass.user)]]">
          <ha-change-password-card hass="[[hass]]"></ha-change-password-card>
        </template>

        <ha-mfa-modules-card
          hass='[[hass]]'
          mfa-modules='[[hass.user.mfa_modules]]'
        ></ha-mfa-modules-card>

        <ha-refresh-tokens-card
          hass='[[hass]]'
          refresh-tokens='[[_refreshTokens]]'
          on-hass-refresh-tokens='_refreshRefreshTokens'
        ></ha-refresh-tokens-card>

        <ha-long-lived-access-tokens-card
          hass='[[hass]]'
          refresh-tokens='[[_refreshTokens]]'
          on-hass-refresh-tokens='_refreshRefreshTokens'
        ></ha-long-lived-access-tokens-card>
      </div>
    </app-header-layout>
    `}static get properties(){return{hass:Object,narrow:Boolean,showMenu:Boolean,_refreshTokens:Array}}connectedCallback(){super.connectedCallback(),this._refreshRefreshTokens()}async _refreshRefreshTokens(){this._refreshTokens=await this.hass.callWS({type:"auth/refresh_tokens"})}_handleLogOut(){this.fire("hass-logout")}_canChangePassword(e){return e.credentials.some(e=>"homeassistant"===e.auth_provider_type)}})}}]);
//# sourceMappingURL=3cb9cbd8a1e12213696f.chunk.js.map