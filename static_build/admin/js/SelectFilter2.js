"use strict";!function(N){window.SelectFilter={init:function(n,e,t){if(!n.match(/__prefix__/)){var l=document.getElementById(n);l.id+="_from",l.className="filtered";for(var i=l.parentNode.getElementsByTagName("p"),o=0;o<i.length;o++)-1!==i[o].className.indexOf("info")?l.parentNode.removeChild(i[o]):-1!==i[o].className.indexOf("help")&&l.parentNode.insertBefore(i[o],l.parentNode.firstChild);var c=quickElement("div",l.parentNode);c.className=t?"selector stacked":"selector";var r=quickElement("div",c);r.className="selector-available";var a=quickElement("h2",r,interpolate(gettext("Available %s")+" ",[e]));quickElement("span",a,"","class","help help-tooltip help-icon","title",interpolate(gettext('This is the list of available %s. You may choose some by selecting them in the box below and then clicking the "Choose" arrow between the two boxes.'),[e]));var s=quickElement("p",r,"","id",n+"_filter");s.className="selector-filter";var d=quickElement("label",s,"","for",n+"_input");quickElement("span",d,"","class","help-tooltip search-label-icon","title",interpolate(gettext("Type into this box to filter down the list of available %s."),[e])),s.appendChild(document.createTextNode(" "));var m=quickElement("input",s,"","type","text","placeholder",gettext("Filter"));m.id=n+"_input",r.appendChild(l);var h=quickElement("a",r,gettext("Choose all"),"title",interpolate(gettext("Click to choose all %s at once."),[e]),"href","#","id",n+"_add_all_link");h.className="selector-chooseall";var f=quickElement("ul",c);f.className="selector-chooser";var _=quickElement("a",quickElement("li",f),gettext("Choose"),"title",gettext("Choose"),"href","#","id",n+"_add_link");_.className="selector-add";var u=quickElement("a",quickElement("li",f),gettext("Remove"),"title",gettext("Remove"),"href","#","id",n+"_remove_link");u.className="selector-remove";var v=quickElement("div",c);v.className="selector-chosen";var k=quickElement("h2",v,interpolate(gettext("Chosen %s")+" ",[e]));quickElement("span",k,"","class","help help-tooltip help-icon","title",interpolate(gettext('This is the list of chosen %s. You may remove some by selecting them in the box below and then clicking the "Remove" arrow between the two boxes.'),[e])),quickElement("select",v,"","id",n+"_to","multiple","multiple","size",l.size,"name",l.getAttribute("name")).className="filtered";var g=quickElement("a",v,gettext("Remove all"),"title",interpolate(gettext("Click to remove all chosen %s at once."),[e]),"href","#","id",n+"_remove_all_link");g.className="selector-clearall",l.setAttribute("name",l.getAttribute("name")+"_old");var p=function(e,t,l,i,o){-1!==t.className.indexOf("active")&&(l(i,o),SelectFilter.refresh_icons(n)),e.preventDefault()};if(h.addEventListener("click",function(e){p(e,this,SelectBox.move_all,n+"_from",n+"_to")}),_.addEventListener("click",function(e){p(e,this,SelectBox.move,n+"_from",n+"_to")}),u.addEventListener("click",function(e){p(e,this,SelectBox.move,n+"_to",n+"_from")}),g.addEventListener("click",function(e){p(e,this,SelectBox.move_all,n+"_to",n+"_from")}),m.addEventListener("keypress",function(e){SelectFilter.filter_key_press(e,n)}),m.addEventListener("keyup",function(e){SelectFilter.filter_key_up(e,n)}),m.addEventListener("keydown",function(e){SelectFilter.filter_key_down(e,n)}),c.addEventListener("change",function(e){"SELECT"===e.target.tagName&&SelectFilter.refresh_icons(n)}),c.addEventListener("dblclick",function(e){"OPTION"===e.target.tagName&&(e.target.closest("select").id===n+"_to"?SelectBox.move(n+"_to",n+"_from"):SelectBox.move(n+"_from",n+"_to"),SelectFilter.refresh_icons(n))}),function e(t){return"form"!==t.tagName.toLowerCase()?e(t.parentNode):t}(l).addEventListener("submit",function(){SelectBox.select_all(n+"_to")}),SelectBox.init(n+"_from"),SelectBox.init(n+"_to"),SelectBox.move(n+"_from",n+"_to"),!t){var x=N("#"+n+"_from"),E=N("#"+n+"_to"),y=function(){E.height(N(s).outerHeight()+x.outerHeight())};0<x.outerHeight()?y():E.closest("fieldset").one("show.fieldset",y)}SelectFilter.refresh_icons(n)}},any_selected:function(t){var l=!1;try{t.attr("required","required"),l=t.is(":valid"),t.removeAttr("required")}catch(e){l=0<t.find("option:selected").length}return l},refresh_icons:function(e){var t=N("#"+e+"_from"),l=N("#"+e+"_to");N("#"+e+"_add_link").toggleClass("active",SelectFilter.any_selected(t)),N("#"+e+"_remove_link").toggleClass("active",SelectFilter.any_selected(l)),N("#"+e+"_add_all_link").toggleClass("active",0<t.find("option").length),N("#"+e+"_remove_all_link").toggleClass("active",0<l.find("option").length)},filter_key_press:function(e,t){var l=document.getElementById(t+"_from");if(e.which&&13===e.which||e.keyCode&&13===e.keyCode)return l.selectedIndex=0,SelectBox.move(t+"_from",t+"_to"),l.selectedIndex=0,e.preventDefault(),!1},filter_key_up:function(e,t){var l=document.getElementById(t+"_from"),i=l.selectedIndex;return SelectBox.filter(t+"_from",document.getElementById(t+"_input").value),l.selectedIndex=i,!0},filter_key_down:function(e,t){var l=document.getElementById(t+"_from");if(e.which&&39===e.which||e.keyCode&&39===e.keyCode){var i=l.selectedIndex;return SelectBox.move(t+"_from",t+"_to"),l.selectedIndex=i===l.length?l.length-1:i,!1}return(e.which&&40===e.which||e.keyCode&&40===e.keyCode)&&(l.selectedIndex=l.length===l.selectedIndex+1?0:l.selectedIndex+1),(e.which&&38===e.which||e.keyCode&&38===e.keyCode)&&(l.selectedIndex=0===l.selectedIndex?l.length-1:l.selectedIndex-1),!0}},window.addEventListener("load",function(e){N("select.selectfilter, select.selectfilterstacked").each(function(){var e=N(this),t=e.data();SelectFilter.init(e.attr("id"),t.fieldName,parseInt(t.isStacked,10))})})}(django.jQuery);