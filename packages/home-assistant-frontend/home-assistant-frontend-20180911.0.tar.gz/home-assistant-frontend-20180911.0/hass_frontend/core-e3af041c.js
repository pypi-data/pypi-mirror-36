!function(e){function t(t){for(var n,s,o=t[0],i=t[1],c=0,u=[];c<o.length;c++)s=o[c],r[s]&&u.push(r[s][0]),r[s]=0;for(n in i)Object.prototype.hasOwnProperty.call(i,n)&&(e[n]=i[n]);for(a&&a(t);u.length;)u.shift()()}var n={},r={52:0};function s(t){if(n[t])return n[t].exports;var r=n[t]={i:t,l:!1,exports:{}};return e[t].call(r.exports,r,r.exports,s),r.l=!0,r.exports}s.e=function(e){var t=[],n=r[e];if(0!==n)if(n)t.push(n[2]);else{var o=new Promise(function(t,s){n=r[e]=[t,s]});t.push(n[2]=o);var i,c=document.getElementsByTagName("head")[0],a=document.createElement("script");a.charset="utf-8",a.timeout=120,s.nc&&a.setAttribute("nonce",s.nc),a.src=function(e){return s.p+""+{40:"243cdf84d79abec26036"}[e]+".chunk.js"}(e),i=function(t){a.onerror=a.onload=null,clearTimeout(u);var n=r[e];if(0!==n){if(n){var s=t&&("load"===t.type?"missing":t.type),o=t&&t.target&&t.target.src,i=new Error("Loading chunk "+e+" failed.\n("+s+": "+o+")");i.type=s,i.request=o,n[1](i)}r[e]=void 0}};var u=setTimeout(function(){i({type:"timeout",target:a})},12e4);a.onerror=a.onload=i,c.appendChild(a)}return Promise.all(t)},s.m=e,s.c=n,s.d=function(e,t,n){s.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:n})},s.r=function(e){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},s.t=function(e,t){if(1&t&&(e=s(e)),8&t)return e;if(4&t&&"object"==typeof e&&e&&e.__esModule)return e;var n=Object.create(null);if(s.r(n),Object.defineProperty(n,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var r in e)s.d(n,r,function(t){return e[t]}.bind(null,r));return n},s.n=function(e){var t=e&&e.__esModule?function(){return e.default}:function(){return e};return s.d(t,"a",t),t},s.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},s.p="/frontend_latest/",s.oe=function(e){throw console.error(e),e};var o=window.webpackJsonp=window.webpackJsonp||[],i=o.push.bind(o);o.push=t,o=o.slice();for(var c=0;c<o.length;c++)t(o[c]);var a=i;s(s.s=193)}({106:function(e,t,n){"use strict";n.d(t,"a",function(){return s});var r=n(23);const s=(e,t)=>Object(r.d)("_pnl",e=>e.sendMessagePromise({type:"get_panels"}),null,e,t)},107:function(e,t,n){"use strict";n.d(t,"a",function(){return i});var r=n(23);const s=e=>e.sendMessagePromise({type:"frontend/get_themes"}),o=(e,t)=>e.subscribeEvents(e=>t.setState(e.data,!0),"themes_updated"),i=(e,t)=>Object(r.d)("_thm",s,o,e,t)},108:function(e,t,n){"use strict";n.d(t,"a",function(){return s});var r=n(23);const s=(e,t)=>Object(r.d)("_usr",e=>Object(r.g)(e),null,e,t)},193:function(e,t,n){"use strict";n.r(t);var r=n(23),s=n(81),o=n(106),i=n(107),c=n(108);const a=`${location.protocol}//${location.host}`,u=location.search.includes("external_auth=1"),l=u?()=>n.e(40).then(n.bind(null,196)).then(e=>new e.default(a)):()=>Object(r.f)({hassUrl:a,saveTokens:s.d,loadTokens:()=>Promise.resolve(Object(s.c)())});window.hassConnection=l().then(async e=>{try{const t=await Object(r.e)({auth:e});return location.search.includes("auth_callback=1")&&history.replaceState(null,null,location.pathname),{auth:e,conn:t}}catch(t){if(t!==r.b)throw t;return u||Object(s.d)(null),{auth:e=await l(),conn:await Object(r.e)({auth:e})}}}),window.hassConnection.then(({conn:e})=>{const t=()=>{};Object(r.i)(e,t),Object(r.h)(e,t),Object(r.j)(e,t),Object(o.a)(e,t),Object(i.a)(e,t),Object(c.a)(e,t)}),window.addEventListener("error",e=>{const t=document.querySelector("home-assistant");t&&t.hass&&t.hass.callService&&t.hass.callService("system_log","write",{logger:`frontend.js.latest.${"20180911.0".replace(".","")}`,message:`${e.filename}:${e.lineno}:${e.colno} ${e.message}`})})},23:function(e,t,n){"use strict";function r(e,t,n,r){return new(n||(n=Promise))(function(s,o){function i(e){try{a(r.next(e))}catch(e){o(e)}}function c(e){try{a(r.throw(e))}catch(e){o(e)}}function a(e){e.done?s(e.value):new n(function(t){t(e.value)}).then(i,c)}a((r=r.apply(e,t||[])).next())})}function s(e,t){var n,r,s,o,i={label:0,sent:function(){if(1&s[0])throw s[1];return s[1]},trys:[],ops:[]};return o={next:c(0),throw:c(1),return:c(2)},"function"==typeof Symbol&&(o[Symbol.iterator]=function(){return this}),o;function c(o){return function(c){return function(o){if(n)throw new TypeError("Generator is already executing.");for(;i;)try{if(n=1,r&&(s=2&o[0]?r.return:o[0]?r.throw||((s=r.return)&&s.call(r),0):r.next)&&!(s=s.call(r,o[1])).done)return s;switch(r=0,s&&(o=[2&o[0],s.value]),o[0]){case 0:case 1:s=o;break;case 4:return i.label++,{value:o[1],done:!1};case 5:i.label++,r=o[1],o=[0];continue;case 7:o=i.ops.pop(),i.trys.pop();continue;default:if(!(s=(s=i.trys).length>0&&s[s.length-1])&&(6===o[0]||2===o[0])){i=0;continue}if(3===o[0]&&(!s||o[1]>s[0]&&o[1]<s[3])){i.label=o[1];break}if(6===o[0]&&i.label<s[1]){i.label=s[1],s=o;break}if(s&&i.label<s[2]){i.label=s[2],i.ops.push(o);break}s[2]&&i.ops.pop(),i.trys.pop();continue}o=t.call(e,i)}catch(e){o=[6,e],r=0}finally{n=s=0}if(5&o[0])throw o[1];return{value:o[0]?o[1]:void 0,done:!0}}([o,c])}}}n.d(t,"e",function(){return C}),n.d(t,"a",function(){return u}),n.d(t,"f",function(){return l}),n.d(t,"d",function(){return f}),n.d(t,"h",function(){return g}),n.d(t,"j",function(){return j}),n.d(t,"i",function(){return T}),n.d(t,"b",function(){return o}),n.d(t,"g",function(){return v}),n.d(t,"c",function(){return p});var o=2,i=4,c=function(){function e(e,t){this.options=t,this.commandId=1,this.commands={},this.eventListeners={},this.closeRequested=!1,this._handleClose=this._handleClose.bind(this),this.setSocket(e)}return e.prototype.setSocket=function(e){var t=this,n=this.socket;if(this.socket=e,e.addEventListener("message",function(e){return t._handleMessage(e)}),e.addEventListener("close",this._handleClose),n){var r=this.commands;this.commandId=1,this.commands={},Object.keys(r).forEach(function(e){var n=r[e];n.eventType&&t.subscribeEvents(n.eventCallback,n.eventType).then(function(e){n.unsubscribe=e})}),this.fireEvent("ready")}},e.prototype.addEventListener=function(e,t){var n=this.eventListeners[e];n||(n=this.eventListeners[e]=[]),n.push(t)},e.prototype.removeEventListener=function(e,t){var n=this.eventListeners[e];if(n){var r=n.indexOf(t);-1!==r&&n.splice(r,1)}},e.prototype.fireEvent=function(e,t){var n=this;(this.eventListeners[e]||[]).forEach(function(e){return e(n,t)})},e.prototype.close=function(){this.closeRequested=!0,this.socket.close()},e.prototype.subscribeEvents=function(e,t){return r(this,void 0,void 0,function(){var n,o,i=this;return s(this,function(c){switch(c.label){case 0:return n=this._genCmdId(),[4,this.sendMessagePromise(function(e){var t={type:"subscribe_events"};return e&&(t.event_type=e),t}(t),n)];case 1:return c.sent(),this.commands[n]=o={eventCallback:e,eventType:t,unsubscribe:function(){return r(i,void 0,void 0,function(){return s(this,function(e){switch(e.label){case 0:return[4,this.sendMessagePromise((t=n,{type:"unsubscribe_events",subscription:t}))];case 1:return e.sent(),delete this.commands[n],[2]}var t})})}},[2,function(){return o.unsubscribe()}]}})})},e.prototype.ping=function(){return this.sendMessagePromise({type:"ping"})},e.prototype.sendMessage=function(e,t){t||(t=this._genCmdId()),e.id=t,this.socket.send(JSON.stringify(e))},e.prototype.sendMessagePromise=function(e,t){var n=this;return new Promise(function(r,s){t||(t=n._genCmdId()),n.commands[t]={resolve:r,reject:s},n.sendMessage(e,t)})},e.prototype._handleMessage=function(e){var t=JSON.parse(e.data);switch(t.type){case"event":this.commands[t.id].eventCallback(t.event);break;case"result":t.id in this.commands&&(1==t.success?this.commands[t.id].resolve(t.result):this.commands[t.id].reject(t.error),delete this.commands[t.id]);break;case"pong":this.commands[t.id].resolve(),delete this.commands[t.id]}},e.prototype._handleClose=function(){var e=this;if(Object.keys(this.commands).forEach(function(t){var n=e.commands[t].reject;n&&n({type:"result",success:!1,error:{code:3,message:"Connection lost"}})}),!this.closeRequested){this.fireEvent("disconnected");var t=Object.assign({},this.options,{setupRetry:0}),n=function(i){setTimeout(function(){return r(e,void 0,void 0,function(){var e,r;return s(this,function(s){switch(s.label){case 0:s.label=1;case 1:return s.trys.push([1,3,,4]),[4,t.createSocket(t)];case 2:return e=s.sent(),this.setSocket(e),[3,4];case 3:return(r=s.sent())===o?this.fireEvent("reconnect-error",r):n(i+1),[3,4];case 4:return[2]}})})},1e3*Math.min(i,5))};n(0)}},e.prototype._genCmdId=function(){return++this.commandId},e}();function a(e,t,n){return r(this,void 0,void 0,function(){var r,i,c;return s(this,function(s){switch(s.label){case 0:return(r=new FormData).append("client_id",t),Object.keys(n).forEach(function(e){r.append(e,n[e])}),[4,fetch(e+"/auth/token",{method:"POST",credentials:"same-origin",body:r})];case 1:if(!(i=s.sent()).ok)throw 400===i.status||403===i.status?o:new Error("Unable to fetch tokens");return[4,i.json()];case 2:return(c=s.sent()).hassUrl=e,c.clientId=t,c.expires=1e3*c.expires_in+Date.now(),[2,c]}})})}var u=function(){function e(e,t){this.data=e,this._saveTokens=t}return Object.defineProperty(e.prototype,"wsUrl",{get:function(){return"ws"+this.data.hassUrl.substr(4)+"/api/websocket"},enumerable:!0,configurable:!0}),Object.defineProperty(e.prototype,"accessToken",{get:function(){return this.data.access_token},enumerable:!0,configurable:!0}),Object.defineProperty(e.prototype,"expired",{get:function(){return Date.now()>this.data.expires},enumerable:!0,configurable:!0}),e.prototype.refreshAccessToken=function(){return r(this,void 0,void 0,function(){var e;return s(this,function(t){switch(t.label){case 0:return[4,a(this.data.hassUrl,this.data.clientId,{grant_type:"refresh_token",refresh_token:this.data.refresh_token})];case 1:return(e=t.sent()).refresh_token=this.data.refresh_token,this.data=e,this._saveTokens&&this._saveTokens(e),[2]}})})},e.prototype.revoke=function(){return r(this,void 0,void 0,function(){var e;return s(this,function(t){switch(t.label){case 0:return(e=new FormData).append("action","revoke"),e.append("token",this.data.refresh_token),[4,fetch(this.data.hassUrl+"/auth/token",{method:"POST",credentials:"same-origin",body:e})];case 1:return t.sent(),this._saveTokens&&this._saveTokens(null),[2]}})})},e}();function l(e){return void 0===e&&(e={}),r(this,void 0,void 0,function(){var t,n,r,o,c,l,d;return s(this,function(s){switch(s.label){case 0:if(!("auth_callback"in(n=function(e){for(var t={},n=location.search.substr(1).split("&"),r=0;r<n.length;r++){var s=n[r].split("="),o=decodeURIComponent(s[0]),i=s.length>1?decodeURIComponent(s[1]):void 0;t[o]=i}return t}())))return[3,4];r=JSON.parse(atob(n.state)),s.label=1;case 1:return s.trys.push([1,3,,4]),[4,a(r.hassUrl,r.clientId,{code:n.code,grant_type:"authorization_code"})];case 2:return t=s.sent(),e.saveTokens&&e.saveTokens(t),[3,4];case 3:return o=s.sent(),console.log("Unable to fetch access token",o),[3,4];case 4:return t||!e.loadTokens?[3,6]:[4,e.loadTokens()];case 5:t=s.sent(),s.label=6;case 6:if(t)return[2,new u(t,e.saveTokens)];if(void 0===(c=e.hassUrl))throw i;return"/"===c[c.length-1]&&(c=c.substr(0,c.length-1)),l=e.clientId||location.protocol+"//"+location.host+"/",d=e.redirectUrl||location.protocol+"//"+location.host+location.pathname+location.search,function(e,t,n,r){n+=(n.includes("?")?"&":"?")+"auth_callback=1",document.location.href=function(e,t,n,r){var s=e+"/auth/authorize?response_type=code&client_id="+encodeURIComponent(t)+"&redirect_uri="+encodeURIComponent(n);return r&&(s+="&state="+encodeURIComponent(r)),s}(e,t,n,r)}(c,l,d,function(e){return btoa(JSON.stringify(e))}({hassUrl:c,clientId:l})),[2,new Promise(function(){})]}})})}var d=function(){function e(e){this._noSub=e,this.listeners=[]}return e.prototype.action=function(e){var t=this,n=function(e){return t.setState(e,!1)};return function(){for(var r=[],s=0;s<arguments.length;s++)r[s]=arguments[s];var o=e.apply(void 0,[t.state].concat(r));if(null!=o)return"then"in o?o.then(n):n(o)}},e.prototype.setState=function(e,t){this.state=t?e:Object.assign({},this.state,e);for(var n=this.listeners,r=0;r<n.length;r++)n[r](this.state)},e.prototype.subscribe=function(e){var t=this;return this.listeners.push(e),void 0!==this.state&&e(this.state),function(){t.unsubscribe(e)}},e.prototype.unsubscribe=function(e){for(var t=e,n=[],r=this.listeners,s=0;s<r.length;s++)r[s]===t?t=null:n.push(r[s]);this.listeners=n,0===n.length&&this._noSub()},e}();function f(e,t,n,o,i){if(e in o)return o[e](i);var c,a=new d(function(){c&&c.then(function(e){return e()}),o.removeEventListener("ready",u),delete o[e]});function u(){return r(this,void 0,void 0,function(){var e,n;return s(this,function(r){switch(r.label){case 0:return n=(e=a).setState,[4,t(o)];case 1:return n.apply(e,[r.sent(),!0]),[2]}})})}return o[e]=function(e){return a.subscribe(e)},n&&(c=n(o,a)),o.addEventListener("ready",u),u(),a.subscribe(i)}var h=function(e){return e.sendMessagePromise({type:"get_states"})},v=function(e){return e.sendMessagePromise({type:"auth/current_user"})},p=function(e,t,n,r){return e.sendMessagePromise(function(e,t,n){var r={type:"call_service",domain:e,service:t};return n&&(r.service_data=n),r}(t,n,r))};function b(e,t){return void 0===e?null:{components:e.components.concat(t.data.component)}}var m=function(e){return function(e){return e.sendMessagePromise({type:"get_config"})}(e)},y=function(e,t){return e.subscribeEvents(t.action(b),"component_loaded")},g=function(e,t){return f("_cnf",m,y,e,t)};function k(e,t){var n,r;if(void 0===e)return null;var s=t.data,o=s.domain,i=Object.assign({},e[o],((n={})[s.service]={description:"",fields:{}},n));return(r={})[o]=i,r}function w(e,t){var n;if(void 0===e)return null;var r=t.data,s=r.domain,o=r.service,i=e[s];if(!(i&&o in i))return null;var c={};return Object.keys(i).forEach(function(e){e!==o&&(c[e]=i[e])}),(n={})[s]=c,n}var _=function(e){return function(e){return e.sendMessagePromise({type:"get_services"})}(e)},O=function(e,t){return Promise.all([e.subscribeEvents(t.action(k),"service_registered"),e.subscribeEvents(t.action(w),"service_removed")]).then(function(e){return function(){return e.forEach(function(e){return e()})}})},j=function(e,t){return f("_srv",_,O,e,t)};function E(e){return r(this,void 0,void 0,function(){var t,n,r,o;return s(this,function(s){switch(s.label){case 0:return[4,h(e)];case 1:for(t=s.sent(),n={},r=0;r<t.length;r++)n[(o=t[r]).entity_id]=o;return[2,n]}})})}var S=function(e,t){return e.subscribeEvents(function(e){return function(e,t){var n,r=e.state;if(void 0!==r){var s=t.data,o=s.entity_id,i=s.new_state;if(i)e.setState(((n={})[i.entity_id]=i,n));else{var c=Object.assign({},r);delete c[o],e.setState(c,!0)}}}(t,e)},"state_changed")},T=function(e,t){return f("_ent",E,S,e,t)},P={setupRetry:0,createSocket:function(e){if(!e.auth)throw i;var t=e.auth,n=t.wsUrl;return new Promise(function(i,c){return function e(i,c,a){var u=this,l=new WebSocket(n),d=!1,f=function(){if(l.removeEventListener("close",f),d)a(o);else if(0!==i){var t=-1===i?-1:i-1;setTimeout(function(){return e(t,c,a)},1e3)}else a(1)},h=function(e){return r(u,void 0,void 0,function(){var e;return s(this,function(n){switch(n.label){case 0:return n.trys.push([0,3,,4]),t.expired?[4,t.refreshAccessToken()]:[3,2];case 1:n.sent(),n.label=2;case 2:return l.send(JSON.stringify({type:"auth",access_token:t.accessToken})),[3,4];case 3:return e=n.sent(),d=e===o,l.close(),[3,4];case 4:return[2]}})})},v=function(e){return r(u,void 0,void 0,function(){return s(this,function(t){switch(JSON.parse(e.data).type){case"auth_invalid":d=!0,l.close();break;case"auth_ok":l.removeEventListener("open",h),l.removeEventListener("message",v),l.removeEventListener("close",f),l.removeEventListener("error",f),c(l)}return[2]})})};l.addEventListener("open",h),l.addEventListener("message",v),l.addEventListener("close",f),l.addEventListener("error",f)}(e.setupRetry,i,c)})}};function C(e){return r(this,void 0,void 0,function(){var t,n;return s(this,function(r){switch(r.label){case 0:return[4,(t=Object.assign({},P,e)).createSocket(t)];case 1:return n=r.sent(),[2,new c(n,t)]}})})}},81:function(e,t,n){"use strict";n.d(t,"a",function(){return o}),n.d(t,"d",function(){return i}),n.d(t,"b",function(){return c}),n.d(t,"c",function(){return a});const r=window.localStorage||{};let s=window.__tokenCache;function o(){return void 0!==s.tokens&&void 0===s.writeEnabled}function i(e){if(s.tokens=e,s.writeEnabled)try{r.hassTokens=JSON.stringify(e)}catch(e){}}function c(){s.writeEnabled=!0,i(s.tokens)}function a(){if(void 0===s.tokens)try{delete r.tokens;const e=r.hassTokens;e?(s.tokens=JSON.parse(e),s.writeEnabled=!0):s.tokens=null}catch(e){s.tokens=null}return s.tokens}s||(s=window.__tokenCache={tokens:void 0,writeEnabled:void 0})}});
//# sourceMappingURL=core-e3af041c.js.map