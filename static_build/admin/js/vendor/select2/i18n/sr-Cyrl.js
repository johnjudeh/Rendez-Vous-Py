"use strict";!function(){if(jQuery&&jQuery.fn&&jQuery.fn.select2&&jQuery.fn.select2.amd)var n=jQuery.fn.select2.amd;n.define("select2/i18n/sr-Cyrl",[],function(){function u(n,e,r,u){return n%10==1&&n%100!=11?e:2<=n%10&&n%10<=4&&(n%100<12||14<n%100)?r:u}return{errorLoading:function(){return"Преузимање није успело."},inputTooLong:function(n){var e=n.input.length-n.maximum,r="Обришите "+e+" симбол";return r+=u(e,"","а","а")},inputTooShort:function(n){var e=n.minimum-n.input.length,r="Укуцајте бар још "+e+" симбол";return r+=u(e,"","а","а")},loadingMore:function(){return"Преузимање још резултата…"},maximumSelected:function(n){var e="Можете изабрати само "+n.maximum+" ставк";return e+=u(n.maximum,"у","е","и")},noResults:function(){return"Ништа није пронађено"},searching:function(){return"Претрага…"}}}),n.define,n.require}();