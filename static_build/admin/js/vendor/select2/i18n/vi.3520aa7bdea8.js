"use strict";!function(){if(jQuery&&jQuery.fn&&jQuery.fn.select2&&jQuery.fn.select2.amd)var n=jQuery.fn.select2.amd;n.define("select2/i18n/vi",[],function(){return{inputTooLong:function(n){var t=n.input.length-n.maximum,u="Vui lòng nhập ít hơn "+t+" ký tự";return 1!=t&&(u+="s"),u},inputTooShort:function(n){return"Vui lòng nhập nhiều hơn "+(n.minimum-n.input.length)+' ký tự"'},loadingMore:function(){return"Đang lấy thêm kết quả…"},maximumSelected:function(n){return"Chỉ có thể chọn được "+n.maximum+" lựa chọn"},noResults:function(){return"Không tìm thấy kết quả"},searching:function(){return"Đang tìm…"}}}),n.define,n.require}();