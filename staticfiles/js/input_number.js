
!function(t,e){"function"==typeof define&&define.amd?define([],e):"object"==typeof exports?module.exports=e():t.StringMask=e()}(this,function(){function t(t,e){for(var n=0,r=e-1,i={escape:!0};r>=0&&i&&i.escape;)i=a[t.charAt(r)],n+=i&&i.escape?1:0,r--;return n>0&&n%2===1}function e(t,e){var n=t.replace(/[^0]/g,"").length,r=e.replace(/[^\d]/g,"").length;return r-n}function n(t,e,n,r){return r&&"function"==typeof r.transform&&(e=r.transform(e)),n.reverse?e+t:t+e}function r(t,e,n){var i=t.charAt(e),s=a[i];return""===i?!1:s&&!s.escape?!0:r(t,e+n,n)}function i(t,e,n){var r=t.charAt(e),s=a[r];return""===r?!1:s&&s.recursive?!0:i(t,e+n,n)}function s(t,e,n){var r=t.split("");return r.splice(n,0,e),r.join("")}function o(t,e){this.options=e||{},this.options={reverse:this.options.reverse||!1,usedefaults:this.options.usedefaults||this.options.reverse},this.pattern=t}var a={0:{pattern:/\d/,_default:"0"},9:{pattern:/\d/,optional:!0},"#":{pattern:/\d/,optional:!0,recursive:!0},A:{pattern:/[a-zA-Z0-9]/},S:{pattern:/[a-zA-Z]/},U:{pattern:/[a-zA-Z]/,transform:function(t){return t.toLocaleUpperCase()}},L:{pattern:/[a-zA-Z]/,transform:function(t){return t.toLocaleLowerCase()}},$:{escape:!0}};return o.prototype.process=function(o){function p(t){if(!A&&!g.length&&r(u,l,y.inc))return!0;if(!A&&g.length&&i(u,l,y.inc))return!0;if(A||(A=g.length>0),A){var e=g.shift();if(g.push(e),t.reverse&&h>=0)return l++,u=s(u,e,l),!0;if(!t.reverse&&h<o.length)return u=s(u,e,l),!0}return l<u.length&&l>=0}if(!o)return{result:"",valid:!1};o+="";var u=this.pattern,c=!0,f="",h=this.options.reverse?o.length-1:0,l=0,v=e(u,o),d=!1,g=[],A=!1,y={start:this.options.reverse?u.length-1:0,end:this.options.reverse?-1:u.length,inc:this.options.reverse?-1:1};for(l=y.start;p(this.options);l+=y.inc){var m=o.charAt(h),w=u.charAt(l),z=a[w];if(g.length&&z&&!z.recursive&&(z=null),!A||m){if(this.options.reverse&&t(u,l)){f=n(f,w,this.options,z),l+=y.inc;continue}if(!this.options.reverse&&d){f=n(f,w,this.options,z),d=!1;continue}if(!this.options.reverse&&z&&z.escape){d=!0;continue}}if(!A&&z&&z.recursive)g.push(w);else{if(A&&!m){f=n(f,w,this.options,z);continue}if(!A&&g.length>0&&!m)continue}if(z)if(z.optional){if(z.pattern.test(m)&&v)f=n(f,m,this.options,z),h+=y.inc,v--;else if(g.length>0&&m){c=!1;break}}else if(z.pattern.test(m))f=n(f,m,this.options,z),h+=y.inc;else{if(m||!z._default||!this.options.usedefaults){c=!1;break}f=n(f,z._default,this.options,z)}else f=n(f,w,this.options,z),!A&&g.length&&g.push(w)}return{result:f,valid:c}},o.prototype.apply=function(t){return this.process(t).result},o.prototype.validate=function(t){return this.process(t).valid},o.process=function(t,e,n){return new o(e,n).process(t)},o.apply=function(t,e,n){return new o(e,n).apply(t)},o.validate=function(t,e,n){return new o(e,n).validate(t)},o});
//# sourceMappingURL=./string-mask.min.js.map


(function(app, $, undefined) {
	"use strict";
	app.store = app.store || {
		countryCode: "",
		length: 8,
		placeholder: '9800-0000',
		selectorNum: $('#phone-number'),
		selectorPad: $('.numpad ul'),
		buttonPad: [{
			text: '1',
			type: 'num'
		}, {
			text: '2',
			type: 'num'
		}, {
			text: '3',
			type: 'num'
		}, {
			text: '4',
			type: 'num'
		}, {
			text: '5',
			type: 'num'
		}, {
			text: '6',
			type: 'num'
		}, {
			text: '7',
			type: 'num'
		}, {
			text: '8',
			type: 'num'
		}, {
			text: '9',
			type: 'num'
		}, {
			text: '<i class="backspace">АРИЛГАХ</i>',
			type: 'backspace'
		}, {
			text: '0',
			type: 'num'
		}, {
			text: '<i class="confirm">ҮРГЭЛЖЛҮҮЛЭХ</i>',
			type: 'confirm'
		}],
	};
	app.controller = app.controller || {
		add: function(num, length) {
			if (!app.shortnum.hasClass('active')) {
				app.shortnum.addClass('active')
				this.render(num)
			} else if (length + 1 == app.store.length  ) {
				this.render(app.shortnum.text() + num)
				app.store.selectorNum.addClass('maxlength')
				app.store.selectorPad.children('[data-type = confirm]')
					.addClass('active')
        		app.store.selectorPad.children('[data-type = num]')
					.addClass('disable')
			} else if (length < app.store.length) {
				this.render(app.shortnum.text() + num)
			}
		},
		backspace: function(length) {
			if (app.shortnum.hasClass('active') && length > 1) {
        app.store.selectorPad.children('[data-type = num]')
					  .removeClass('disable')
				this.render(app.shortnum.text().replace(/\D/g, '').replace(/.$/, ''))
			} else {
				this.reset()
			}
			app.store.selectorPad.children('[data-type = confirm]')
				.removeClass('active')
			app.store.selectorNum.removeClass('maxlength')
		},
		confirm: function(length) {
			if (length == app.store.length) {
				app.store.selectorPad.children('[data-type = num]')
					.removeClass('disable')
				app.store.selectorPad.children('[data-type = confirm]')
					.removeClass('disable')	
				var pathArray = window.location.href.split("/");
				var protocol = pathArray[0];
				var host = pathArray[2];
				var path = pathArray[3];
				var url = protocol+"//"+host+"/"+path+"/select_product?number="+app.shortnum.text();
				window.location.href = url;
			}
      		
		},
		reset: function() {
			app.shortnum.text(app.store.placeholder)
			app.shortnum.removeClass('active')
			app.store.selectorNum.removeClass('maxlength')
		},
		render: function(number) {
			var result = StringMask.apply(
				number.replace(/\D/g, ''), app.store.placeholder.replace(/\d/g, '0')
			);
			app.shortnum.text(result)
		},
		input: function(type, command) {
			var length = app.shortnum.text().replace(/\D/g, '').length;
			switch (type) {
				case 'num':
					this.add(command, length);
					break;
				case 'backspace':
					this.backspace(length);
					break;
				case 'confirm':
					this.confirm(length);
					break;
				default:
					return false;
			}
		},
	};
	app.view = app.view || {
		bind: function(num, pad) {
			pad.children().click(function(e) {
				var type = $(this).attr('data-type'),
					command = $(this).text()
				app.controller.input(type, command)
			})
			app.shortnum = num.children('.number')
			app.shortnum.css('min-width', app.shortnum.width())

			window.addEventListener('resize', function() {
        var prev = app.shortnum.text();
				app.shortnum.text(app.store.placeholder)
				app.shortnum.css('min-width', '')
				app.shortnum.css('min-width', app.shortnum.width())
        app.controller.render(prev)
			});
		},
		render: function(num, pad) {
			// Render number
			num.html(
				'<span class="countrycode">' +
				app.store.countryCode +
				' </span><span class="number"> ' +
				app.store.placeholder +
				'</span>'
			)

			// Render numpad
			app.store.buttonPad.forEach(function(item) {
				pad.append(
					'<li data-type="' + item.type + '">' + item.text + '</li>'
				)
			})

			this.bind(num, pad)

		},
		init: function() {
			this.render(app.store.selectorNum, app.store.selectorPad)
		}
	};
	$(document).ready(function() {
		app.view.init()
	});
})(window.app = window.app || {}, jQuery);









