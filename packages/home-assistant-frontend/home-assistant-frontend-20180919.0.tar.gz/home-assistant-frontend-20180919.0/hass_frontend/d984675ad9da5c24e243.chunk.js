/*! For license information please see d984675ad9da5c24e243.chunk.js.LICENSE */
(window.webpackJsonp=window.webpackJsonp||[]).push([[4],{194:function(e,t,o){"use strict";o.d(t,"c",function(){return l}),o.d(t,"b",function(){return d}),o.d(t,"a",function(){return F}),o.d(t,"e",function(){return R}),o.d(t,"d",function(){return r});var n=function(){},r={},a=[],i=[];function l(e,t){var o,l,p,s,d=i;for(s=arguments.length;s-- >2;)a.push(arguments[s]);for(t&&null!=t.children&&(a.length||a.push(t.children),delete t.children);a.length;)if((l=a.pop())&&void 0!==l.pop)for(s=l.length;s--;)a.push(l[s]);else"boolean"==typeof l&&(l=null),(p="function"!=typeof e)&&(null==l?l="":"number"==typeof l?l=String(l):"string"!=typeof l&&(p=!1)),p&&o?d[d.length-1]+=l:d===i?d=[l]:d.push(l),o=p;var c=new n;return c.nodeName=e,c.children=d,c.attributes=null==t?void 0:t,c.key=null==t?void 0:t.key,void 0!==r.vnode&&r.vnode(c),c}function p(e,t){for(var o in t)e[o]=t[o];return e}var s="function"==typeof Promise?Promise.resolve().then.bind(Promise.resolve()):setTimeout;function d(e,t){return l(e.nodeName,p(p({},e.attributes),t),arguments.length>2?[].slice.call(arguments,2):e.children)}var c=/acit|ex(?:s|g|n|p|$)|rph|ows|mnc|ntw|ine[ch]|zoo|^ord/i,u=[];function h(e){!e._dirty&&(e._dirty=!0)&&1==u.push(e)&&(r.debounceRendering||s)(b)}function b(){var e,t=u;for(u=[];e=t.pop();)e._dirty&&T(e)}function f(e,t){return e.normalizedNodeName===t||e.nodeName.toLowerCase()===t.toLowerCase()}function v(e){var t=p({},e.attributes);t.children=e.children;var o=e.nodeName.defaultProps;if(void 0!==o)for(var n in o)void 0===t[n]&&(t[n]=o[n]);return t}function m(e){var t=e.parentNode;t&&t.removeChild(e)}function g(e,t,o,n,r){if("className"===t&&(t="class"),"key"===t);else if("ref"===t)o&&o(null),n&&n(e);else if("class"!==t||r)if("style"===t){if(n&&"string"!=typeof n&&"string"!=typeof o||(e.style.cssText=n||""),n&&"object"==typeof n){if("string"!=typeof o)for(var a in o)a in n||(e.style[a]="");for(var a in n)e.style[a]="number"==typeof n[a]&&!1===c.test(a)?n[a]+"px":n[a]}}else if("dangerouslySetInnerHTML"===t)n&&(e.innerHTML=n.__html||"");else if("o"==t[0]&&"n"==t[1]){var i=t!==(t=t.replace(/Capture$/,""));t=t.toLowerCase().substring(2),n?o||e.addEventListener(t,y,i):e.removeEventListener(t,y,i),(e._listeners||(e._listeners={}))[t]=n}else if("list"!==t&&"type"!==t&&!r&&t in e){try{e[t]=null==n?"":n}catch(e){}null!=n&&!1!==n||"spellcheck"==t||e.removeAttribute(t)}else{var l=r&&t!==(t=t.replace(/^xlink:?/,""));null==n||!1===n?l?e.removeAttributeNS("http://www.w3.org/1999/xlink",t.toLowerCase()):e.removeAttribute(t):"function"!=typeof n&&(l?e.setAttributeNS("http://www.w3.org/1999/xlink",t.toLowerCase(),n):e.setAttribute(t,n))}else e.className=n||""}function y(e){return this._listeners[e.type](r.event&&r.event(e)||e)}var _=[],x=0,w=!1,k=!1;function C(){for(var e;e=_.pop();)r.afterMount&&r.afterMount(e),e.componentDidMount&&e.componentDidMount()}function S(e,t,o,n,r,a){x++||(w=null!=r&&void 0!==r.ownerSVGElement,k=null!=e&&!("__preactattr_"in e));var i=function e(t,o,n,r,a){var i=t,l=w;if(null!=o&&"boolean"!=typeof o||(o=""),"string"==typeof o||"number"==typeof o)return t&&void 0!==t.splitText&&t.parentNode&&(!t._component||a)?t.nodeValue!=o&&(t.nodeValue=o):(i=document.createTextNode(o),t&&(t.parentNode&&t.parentNode.replaceChild(i,t),N(t,!0))),i.__preactattr_=!0,i;var p=o.nodeName;if("function"==typeof p)return function(e,t,o,n){for(var r=e&&e._component,a=r,i=e,l=r&&e._componentConstructor===t.nodeName,p=l,s=v(t);r&&!p&&(r=r._parentComponent);)p=r.constructor===t.nodeName;return r&&p&&(!n||r._component)?(B(r,s,3,o,n),e=r.base):(a&&!l&&(O(a),e=i=null),r=L(t.nodeName,s,o),e&&!r.nextBase&&(r.nextBase=e,i=null),B(r,s,1,o,n),e=r.base,i&&e!==i&&(i._component=null,N(i,!1))),e}(t,o,n,r);if(w="svg"===p||"foreignObject"!==p&&w,p=String(p),(!t||!f(t,p))&&(s=p,d=w,c=d?document.createElementNS("http://www.w3.org/2000/svg",s):document.createElement(s),c.normalizedNodeName=s,i=c,t)){for(;t.firstChild;)i.appendChild(t.firstChild);t.parentNode&&t.parentNode.replaceChild(i,t),N(t,!0)}var s,d,c;var u=i.firstChild,h=i.__preactattr_,b=o.children;if(null==h){h=i.__preactattr_={};for(var y=i.attributes,_=y.length;_--;)h[y[_].name]=y[_].value}return!k&&b&&1===b.length&&"string"==typeof b[0]&&null!=u&&void 0!==u.splitText&&null==u.nextSibling?u.nodeValue!=b[0]&&(u.nodeValue=b[0]):(b&&b.length||null!=u)&&function(t,o,n,r,a){var i,l,p,s,d,c,u,h,b=t.childNodes,v=[],g={},y=0,_=0,x=b.length,w=0,k=o?o.length:0;if(0!==x)for(var C=0;C<x;C++){var S=b[C],I=S.__preactattr_,z=k&&I?S._component?S._component.__key:I.key:null;null!=z?(y++,g[z]=S):(I||(void 0!==S.splitText?!a||S.nodeValue.trim():a))&&(v[w++]=S)}if(0!==k)for(var C=0;C<k;C++){s=o[C],d=null;var z=s.key;if(null!=z)y&&void 0!==g[z]&&(d=g[z],g[z]=void 0,y--);else if(_<w)for(i=_;i<w;i++)if(void 0!==v[i]&&(c=l=v[i],h=a,"string"==typeof(u=s)||"number"==typeof u?void 0!==c.splitText:"string"==typeof u.nodeName?!c._componentConstructor&&f(c,u.nodeName):h||c._componentConstructor===u.nodeName)){d=l,v[i]=void 0,i===w-1&&w--,i===_&&_++;break}d=e(d,s,n,r),p=b[C],d&&d!==t&&d!==p&&(null==p?t.appendChild(d):d===p.nextSibling?m(p):t.insertBefore(d,p))}if(y)for(var C in g)void 0!==g[C]&&N(g[C],!1);for(;_<=w;)void 0!==(d=v[w--])&&N(d,!1)}(i,b,n,r,k||null!=h.dangerouslySetInnerHTML),function(e,t,o){var n;for(n in o)t&&null!=t[n]||null==o[n]||g(e,n,o[n],o[n]=void 0,w);for(n in t)"children"===n||"innerHTML"===n||n in o&&t[n]===("value"===n||"checked"===n?e[n]:o[n])||g(e,n,o[n],o[n]=t[n],w)}(i,o.attributes,h),w=l,i}(e,t,o,n,a);return r&&i.parentNode!==r&&r.appendChild(i),--x||(k=!1,a||C()),i}function N(e,t){var o=e._component;o?O(o):(null!=e.__preactattr_&&e.__preactattr_.ref&&e.__preactattr_.ref(null),!1!==t&&null!=e.__preactattr_||m(e),I(e))}function I(e){for(e=e.lastChild;e;){var t=e.previousSibling;N(e,!0),e=t}}var z=[];function L(e,t,o){var n,r=z.length;for(e.prototype&&e.prototype.render?(n=new e(t,o),F.call(n,t,o)):((n=new F(t,o)).constructor=e,n.render=A);r--;)if(z[r].constructor===e)return n.nextBase=z[r].nextBase,z.splice(r,1),n;return n}function A(e,t,o){return this.constructor(e,o)}function B(e,t,o,n,a){e._disable||(e._disable=!0,e.__ref=t.ref,e.__key=t.key,delete t.ref,delete t.key,void 0===e.constructor.getDerivedStateFromProps&&(!e.base||a?e.componentWillMount&&e.componentWillMount():e.componentWillReceiveProps&&e.componentWillReceiveProps(t,n)),n&&n!==e.context&&(e.prevContext||(e.prevContext=e.context),e.context=n),e.prevProps||(e.prevProps=e.props),e.props=t,e._disable=!1,0!==o&&(1!==o&&!1===r.syncComponentUpdates&&e.base?h(e):T(e,1,a)),e.__ref&&e.__ref(e))}function T(e,t,o,n){if(!e._disable){var a,i,l,s=e.props,d=e.state,c=e.context,u=e.prevProps||s,h=e.prevState||d,b=e.prevContext||c,f=e.base,m=e.nextBase,g=f||m,y=e._component,w=!1,k=b;if(e.constructor.getDerivedStateFromProps&&(d=p(p({},d),e.constructor.getDerivedStateFromProps(s,d)),e.state=d),f&&(e.props=u,e.state=h,e.context=b,2!==t&&e.shouldComponentUpdate&&!1===e.shouldComponentUpdate(s,d,c)?w=!0:e.componentWillUpdate&&e.componentWillUpdate(s,d,c),e.props=s,e.state=d,e.context=c),e.prevProps=e.prevState=e.prevContext=e.nextBase=null,e._dirty=!1,!w){a=e.render(s,d,c),e.getChildContext&&(c=p(p({},c),e.getChildContext())),f&&e.getSnapshotBeforeUpdate&&(k=e.getSnapshotBeforeUpdate(u,h));var I,z,A=a&&a.nodeName;if("function"==typeof A){var F=v(a);(i=y)&&i.constructor===A&&F.key==i.__key?B(i,F,1,c,!1):(I=i,e._component=i=L(A,F,c),i.nextBase=i.nextBase||m,i._parentComponent=e,B(i,F,0,c,!1),T(i,1,o,!0)),z=i.base}else l=g,(I=y)&&(l=e._component=null),(g||1===t)&&(l&&(l._component=null),z=S(l,a,c,o||!f,g&&g.parentNode,!0));if(g&&z!==g&&i!==y){var R=g.parentNode;R&&z!==R&&(R.replaceChild(z,g),I||(g._component=null,N(g,!1)))}if(I&&O(I),e.base=z,z&&!n){for(var U=e,D=e;D=D._parentComponent;)(U=D).base=z;z._component=U,z._componentConstructor=U.constructor}}for(!f||o?_.unshift(e):w||(e.componentDidUpdate&&e.componentDidUpdate(u,h,k),r.afterUpdate&&r.afterUpdate(e));e._renderCallbacks.length;)e._renderCallbacks.pop().call(e);x||n||C()}}function O(e){r.beforeUnmount&&r.beforeUnmount(e);var t=e.base;e._disable=!0,e.componentWillUnmount&&e.componentWillUnmount(),e.base=null;var o=e._component;o?O(o):t&&(t.__preactattr_&&t.__preactattr_.ref&&t.__preactattr_.ref(null),e.nextBase=t,m(t),z.push(e),I(t)),e.__ref&&e.__ref(null)}function F(e,t){this._dirty=!0,this.context=t,this.props=e,this.state=this.state||{},this._renderCallbacks=[]}function R(e,t,o){return S(o,e,{},!1,t,!1)}p(F.prototype,{setState:function(e,t){this.prevState||(this.prevState=this.state),this.state=p(p({},this.state),"function"==typeof e?e(this.state,this.props):e),t&&this._renderCallbacks.push(t),h(this)},forceUpdate:function(e){e&&this._renderCallbacks.push(e),T(this,2)},render:function(){}})},236:function(e,t,o){"use strict";o(2),o(26),o(75),o(64),o(48),o(30);var n=o(59),r=o(3),a=o(0);const i=a["a"]`
  <style include="paper-material-styles">
    :host {
      @apply --layout-vertical;
      @apply --layout-center-center;

      background: var(--paper-fab-background, var(--accent-color));
      border-radius: 50%;
      box-sizing: border-box;
      color: var(--text-primary-color);
      cursor: pointer;
      height: 56px;
      min-width: 0;
      outline: none;
      padding: 16px;
      position: relative;
      -moz-user-select: none;
      -ms-user-select: none;
      -webkit-user-select: none;
      user-select: none;
      width: 56px;
      z-index: 0;

      /* NOTE: Both values are needed, since some phones require the value \`transparent\`. */
      -webkit-tap-highlight-color: rgba(0,0,0,0);
      -webkit-tap-highlight-color: transparent;

      @apply --paper-fab;
    }

    [hidden] {
      display: none !important;
    }

    :host([mini]) {
      width: 40px;
      height: 40px;
      padding: 8px;

      @apply --paper-fab-mini;
    }

    :host([disabled]) {
      color: var(--paper-fab-disabled-text, var(--paper-grey-500));
      background: var(--paper-fab-disabled-background, var(--paper-grey-300));

      @apply --paper-fab-disabled;
    }

    iron-icon {
      @apply --paper-fab-iron-icon;
    }

    span {
      width: 100%;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      text-align: center;

      @apply --paper-fab-label;
    }

    :host(.keyboard-focus) {
      background: var(--paper-fab-keyboard-focus-background, var(--paper-pink-900));
    }

    :host([elevation="1"]) {
      @apply --paper-material-elevation-1;
    }

    :host([elevation="2"]) {
      @apply --paper-material-elevation-2;
    }

    :host([elevation="3"]) {
      @apply --paper-material-elevation-3;
    }

    :host([elevation="4"]) {
      @apply --paper-material-elevation-4;
    }

    :host([elevation="5"]) {
      @apply --paper-material-elevation-5;
    }
  </style>

  <iron-icon id="icon" hidden\$="{{!_computeIsIconFab(icon, src)}}" src="[[src]]" icon="[[icon]]"></iron-icon>
  <span hidden\$="{{_computeIsIconFab(icon, src)}}">{{label}}</span>
`;i.setAttribute("strip-whitespace",""),Object(r.a)({_template:i,is:"paper-fab",behaviors:[n.a],properties:{src:{type:String,value:""},icon:{type:String,value:""},mini:{type:Boolean,value:!1,reflectToAttribute:!0},label:{type:String,observer:"_labelChanged"}},_labelChanged:function(){this.setAttribute("aria-label",this.label)},_computeIsIconFab:function(e,t){return e.length>0||t.length>0}})},252:function(e,t,o){"use strict";o(2),o(30),o(26);var n=o(90),r=o(3),a=o(0),i=o(36);const l=a["a"]`
<style>
  :host {
    display: inline-block;
    line-height: 0;
    white-space: nowrap;
    cursor: pointer;
    @apply --paper-font-common-base;
    --calculated-paper-radio-button-size: var(--paper-radio-button-size, 16px);
    /* -1px is a sentinel for the default and is replace in \`attached\`. */
    --calculated-paper-radio-button-ink-size: var(--paper-radio-button-ink-size, -1px);
  }

  :host(:focus) {
    outline: none;
  }

  #radioContainer {
    @apply --layout-inline;
    @apply --layout-center-center;
    position: relative;
    width: var(--calculated-paper-radio-button-size);
    height: var(--calculated-paper-radio-button-size);
    vertical-align: middle;

    @apply --paper-radio-button-radio-container;
  }

  #ink {
    position: absolute;
    top: 50%;
    left: 50%;
    right: auto;
    width: var(--calculated-paper-radio-button-ink-size);
    height: var(--calculated-paper-radio-button-ink-size);
    color: var(--paper-radio-button-unchecked-ink-color, var(--primary-text-color));
    opacity: 0.6;
    pointer-events: none;
    -webkit-transform: translate(-50%, -50%);
    transform: translate(-50%, -50%);
  }

  #ink[checked] {
    color: var(--paper-radio-button-checked-ink-color, var(--primary-color));
  }

  #offRadio, #onRadio {
    position: absolute;
    box-sizing: border-box;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    border-radius: 50%;
  }

  #offRadio {
    border: 2px solid var(--paper-radio-button-unchecked-color, var(--primary-text-color));
    background-color: var(--paper-radio-button-unchecked-background-color, transparent);
    transition: border-color 0.28s;
  }

  #onRadio {
    background-color: var(--paper-radio-button-checked-color, var(--primary-color));
    -webkit-transform: scale(0);
    transform: scale(0);
    transition: -webkit-transform ease 0.28s;
    transition: transform ease 0.28s;
    will-change: transform;
  }

  :host([checked]) #offRadio {
    border-color: var(--paper-radio-button-checked-color, var(--primary-color));
  }

  :host([checked]) #onRadio {
    -webkit-transform: scale(0.5);
    transform: scale(0.5);
  }

  #radioLabel {
    line-height: normal;
    position: relative;
    display: inline-block;
    vertical-align: middle;
    margin-left: var(--paper-radio-button-label-spacing, 10px);
    white-space: normal;
    color: var(--paper-radio-button-label-color, var(--primary-text-color));

    @apply --paper-radio-button-label;
  }

  :host([checked]) #radioLabel {
    @apply --paper-radio-button-label-checked;
  }

  #radioLabel:dir(rtl) {
    margin-left: 0;
    margin-right: var(--paper-radio-button-label-spacing, 10px);
  }

  #radioLabel[hidden] {
    display: none;
  }

  /* disabled state */

  :host([disabled]) #offRadio {
    border-color: var(--paper-radio-button-unchecked-color, var(--primary-text-color));
    opacity: 0.5;
  }

  :host([disabled][checked]) #onRadio {
    background-color: var(--paper-radio-button-unchecked-color, var(--primary-text-color));
    opacity: 0.5;
  }

  :host([disabled]) #radioLabel {
    /* slightly darker than the button, so that it's readable */
    opacity: 0.65;
  }
</style>

<div id="radioContainer">
  <div id="offRadio"></div>
  <div id="onRadio"></div>
</div>

<div id="radioLabel"><slot></slot></div>`;l.setAttribute("strip-whitespace",""),Object(r.a)({_template:l,is:"paper-radio-button",behaviors:[n.a],hostAttributes:{role:"radio","aria-checked":!1,tabindex:0},properties:{ariaActiveAttribute:{type:String,value:"aria-checked"}},ready:function(){this._rippleContainer=this.$.radioContainer},attached:function(){Object(i.a)(this,function(){if("-1px"===this.getComputedStyleValue("--calculated-paper-radio-button-ink-size").trim()){var e=parseFloat(this.getComputedStyleValue("--calculated-paper-radio-button-size").trim()),t=Math.floor(3*e);t%2!=e%2&&t++,this.updateStyles({"--paper-radio-button-ink-size":t+"px"})}})}})},273:function(e,t,o){"use strict";o(2),o(10),o(252);var n=o(150),r=o(47),a=o(3),i=o(0);Object(a.a)({_template:i["a"]`
    <style>
      :host {
        display: inline-block;
      }

      :host ::slotted(*) {
        padding: var(--paper-radio-group-item-padding, 12px);
      }
    </style>

    <slot></slot>
`,is:"paper-radio-group",behaviors:[n.a],hostAttributes:{role:"radiogroup"},properties:{attrForSelected:{type:String,value:"name"},selectedAttribute:{type:String,value:"checked"},selectable:{type:String,value:"paper-radio-button"},allowEmptySelection:{type:Boolean,value:!1}},select:function(e){var t=this._valueToItem(e);if(!t||!t.hasAttribute("disabled")){if(this.selected){var o=this._valueToItem(this.selected);if(this.selected==e){if(!this.allowEmptySelection)return void(o&&(o.checked=!0));e=""}o&&(o.checked=!1)}r.a.select.apply(this,[e]),this.fire("paper-radio-group-changed")}},_activateFocusedItem:function(){this._itemActivate(this._valueForItem(this.focusedItem),this.focusedItem)},_onUpKey:function(e){this._focusPrevious(),e.preventDefault(),this._activateFocusedItem()},_onDownKey:function(e){this._focusNext(),e.preventDefault(),this._activateFocusedItem()},_onLeftKey:function(e){n.b._onLeftKey.apply(this,arguments),this._activateFocusedItem()},_onRightKey:function(e){n.b._onRightKey.apply(this,arguments),this._activateFocusedItem()}})},316:function(e,t,o){"use strict";o(2),o(10),o(75),o(128),o(30),o(132),o(133);var n=o(18),r=o(11),a=o(34),i=o(37),l=o(33),p=o(3),s=o(1),d=o(27),c=o(0);Object(p.a)({_template:c["a"]`
    <style include="paper-dropdown-menu-shared-styles">
      :host(:focus) {
        outline: none;
      }

      :host {
        width: 200px;  /* Default size of an <input> */
      }

      /**
       * All of these styles below are for styling the fake-input display
       */
      [slot="dropdown-trigger"] {
        box-sizing: border-box;
        position: relative;
        width: 100%;
        padding: 16px 0 8px 0;
      }

      :host([disabled]) [slot="dropdown-trigger"] {
        pointer-events: none;
        opacity: var(--paper-dropdown-menu-disabled-opacity, 0.33);
      }

      :host([no-label-float]) [slot="dropdown-trigger"] {
        padding-top: 8px;   /* If there's no label, we need less space up top. */
      }

      #input {
        @apply --paper-font-subhead;
        @apply --paper-font-common-nowrap;
        line-height: 1.5;
        border-bottom: 1px solid var(--paper-dropdown-menu-color, var(--secondary-text-color));
        color: var(--paper-dropdown-menu-color, var(--primary-text-color));
        width: 100%;
        box-sizing: border-box;
        padding: 12px 20px 0 0;   /* Right padding so that text doesn't overlap the icon */
        outline: none;
        @apply --paper-dropdown-menu-input;
      }

      #input:dir(rtl) {
        padding-right: 0px;
        padding-left: 20px;
      }

      :host([disabled]) #input {
        border-bottom: 1px dashed var(--paper-dropdown-menu-color, var(--secondary-text-color));
      }

      :host([invalid]) #input {
        border-bottom: 2px solid var(--paper-dropdown-error-color, var(--error-color));
      }

      :host([no-label-float]) #input {
        padding-top: 0;   /* If there's no label, we need less space up top. */
      }

      label {
        @apply --paper-font-subhead;
        @apply --paper-font-common-nowrap;
        display: block;
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        /**
         * The container has a 16px top padding, and there's 12px of padding
         * between the input and the label (from the input's padding-top)
         */
        top: 28px;
        box-sizing: border-box;
        width: 100%;
        padding-right: 20px;    /* Right padding so that text doesn't overlap the icon */
        text-align: left;
        transition-duration: .2s;
        transition-timing-function: cubic-bezier(.4,0,.2,1);
        color: var(--paper-dropdown-menu-color, var(--secondary-text-color));
        @apply --paper-dropdown-menu-label;
      }

      label:dir(rtl) {
        padding-right: 0px;
        padding-left: 20px;
      }

      :host([no-label-float]) label {
        top: 8px;
        /* Since the label doesn't need to float, remove the animation duration
        which slows down visibility changes (i.e. when a selection is made) */
        transition-duration: 0s;
      }

      label.label-is-floating {
        font-size: 12px;
        top: 8px;
      }

      label.label-is-hidden {
        visibility: hidden;
      }

      :host([focused]) label.label-is-floating {
        color: var(--paper-dropdown-menu-focus-color, var(--primary-color));
      }

      :host([invalid]) label.label-is-floating {
        color: var(--paper-dropdown-error-color, var(--error-color));
      }

      /**
       * Sets up the focused underline. It's initially hidden, and becomes
       * visible when it's focused.
       */
      label:after {
        background-color: var(--paper-dropdown-menu-focus-color, var(--primary-color));
        bottom: 7px;    /* The container has an 8px bottom padding */
        content: '';
        height: 2px;
        left: 45%;
        position: absolute;
        transition-duration: .2s;
        transition-timing-function: cubic-bezier(.4,0,.2,1);
        visibility: hidden;
        width: 8px;
        z-index: 10;
      }

      :host([invalid]) label:after {
        background-color: var(--paper-dropdown-error-color, var(--error-color));
      }

      :host([no-label-float]) label:after {
        bottom: 7px;    /* The container has a 8px bottom padding */
      }

      :host([focused]:not([disabled])) label:after {
        left: 0;
        visibility: visible;
        width: 100%;
      }

      iron-icon {
        position: absolute;
        right: 0px;
        bottom: 8px;    /* The container has an 8px bottom padding */
        @apply --paper-font-subhead;
        color: var(--disabled-text-color);
        @apply --paper-dropdown-menu-icon;
      }

      iron-icon:dir(rtl) {
        left: 0;
        right: auto;
      }

      :host([no-label-float]) iron-icon {
        margin-top: 0px;
      }

      .error {
        display: inline-block;
        visibility: hidden;
        color: var(--paper-dropdown-error-color, var(--error-color));
        @apply --paper-font-caption;
        position: absolute;
        left:0;
        right:0;
        bottom: -12px;
      }

      :host([invalid]) .error {
        visibility: visible;
      }
    </style>

    <!-- this div fulfills an a11y requirement for combobox, do not remove -->
    <span role="button"></span>
    <paper-menu-button id="menuButton" vertical-align="[[verticalAlign]]" horizontal-align="[[horizontalAlign]]" vertical-offset="[[_computeMenuVerticalOffset(noLabelFloat, verticalOffset)]]" disabled="[[disabled]]" no-animations="[[noAnimations]]" on-iron-select="_onIronSelect" on-iron-deselect="_onIronDeselect" opened="{{opened}}" close-on-activate allow-outside-scroll="[[allowOutsideScroll]]">
      <!-- support hybrid mode: user might be using paper-menu-button 1.x which distributes via <content> -->
      <div class="dropdown-trigger" slot="dropdown-trigger">
        <label class\$="[[_computeLabelClass(noLabelFloat,alwaysFloatLabel,hasContent)]]">
          [[label]]
        </label>
        <div id="input" tabindex="-1">&nbsp;</div>
        <iron-icon icon="paper-dropdown-menu:arrow-drop-down"></iron-icon>
        <span class="error">[[errorMessage]]</span>
      </div>
      <slot id="content" name="dropdown-content" slot="dropdown-content"></slot>
    </paper-menu-button>
`,is:"paper-dropdown-menu-light",behaviors:[n.a,r.a,l.a,a.a,i.a],properties:{selectedItemLabel:{type:String,notify:!0,readOnly:!0},selectedItem:{type:Object,notify:!0,readOnly:!0},value:{type:String,notify:!0,observer:"_valueChanged"},label:{type:String},placeholder:{type:String},opened:{type:Boolean,notify:!0,value:!1,observer:"_openedChanged"},allowOutsideScroll:{type:Boolean,value:!1},noLabelFloat:{type:Boolean,value:!1,reflectToAttribute:!0},alwaysFloatLabel:{type:Boolean,value:!1},noAnimations:{type:Boolean,value:!1},horizontalAlign:{type:String,value:"right"},verticalAlign:{type:String,value:"top"},verticalOffset:Number,hasContent:{type:Boolean,readOnly:!0}},listeners:{tap:"_onTap"},keyBindings:{"up down":"open",esc:"close"},hostAttributes:{tabindex:0,role:"combobox","aria-autocomplete":"none","aria-haspopup":"true"},observers:["_selectedItemChanged(selectedItem)"],attached:function(){var e=this.contentElement;e&&e.selectedItem&&this._setSelectedItem(e.selectedItem)},get contentElement(){for(var e=Object(s.b)(this.$.content).getDistributedNodes(),t=0,o=e.length;t<o;t++)if(e[t].nodeType===Node.ELEMENT_NODE)return e[t]},open:function(){this.$.menuButton.open()},close:function(){this.$.menuButton.close()},_onIronSelect:function(e){this._setSelectedItem(e.detail.item)},_onIronDeselect:function(e){this._setSelectedItem(null)},_onTap:function(e){d.findOriginalTarget(e)===this&&this.open()},_selectedItemChanged:function(e){var t;t=e?e.label||e.getAttribute("label")||e.textContent.trim():"",this.value=t,this._setSelectedItemLabel(t)},_computeMenuVerticalOffset:function(e,t){return t||(e?-4:8)},_getValidity:function(e){return this.disabled||!this.required||this.required&&!!this.value},_openedChanged:function(){var e=this.opened?"true":"false",t=this.contentElement;t&&t.setAttribute("aria-expanded",e)},_computeLabelClass:function(e,t,o){var n="";return!0===e?o?"label-is-hidden":"":((o||!0===t)&&(n+=" label-is-floating"),n)},_valueChanged:function(){this.$.input&&this.$.input.textContent!==this.value&&(this.$.input.textContent=this.value),this._setHasContent(!!this.value)}})}}]);
//# sourceMappingURL=d984675ad9da5c24e243.chunk.js.map