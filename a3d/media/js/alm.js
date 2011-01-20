/*
 * JavaScript Creole 1.0 Wiki Markup Parser
 * $Id: creole.js 14 2009-03-21 16:15:08Z ifomichev $
 *
 * Copyright (c) 2009 Ivan Fomichev
 *
 * Portions Copyright (c) 2007 Chris Purcell
 *
 * Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files (the "Software"),
 * to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included
 * in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
 * THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
 * DEALINGS IN THE SOFTWARE.
 */

if (!Parse) { var Parse = {}; }
if (!Parse.Simple) { Parse.Simple = {}; }

Parse.Simple.Base = function(grammar, options) {
    if (!arguments.length) { return; }

    this.grammar = grammar;
    this.grammar.root = new this.ruleConstructor(this.grammar.root);
    this.options = options;
};

Parse.Simple.Base.prototype = {
    ruleConstructor: null,
    grammar: null,
    options: null,

    parse: function(node, data, options) {
        if (options) {
            for (i in this.options) {
                if (typeof options[i] == 'undefined') { options[i] = this.options[i]; }
            }
        }
        else {
            options = this.options;
        }
        data = data.replace(/\r\n?/g, '\n');
        this.grammar.root.apply(node, data, options);
        if (options && options.forIE) { node.innerHTML = node.innerHTML.replace(/\r?\n/g, '\r\n'); }
    }
};

Parse.Simple.Base.prototype.constructor = Parse.Simple.Base;

Parse.Simple.Base.Rule = function(params) {
    if (!arguments.length) { return; }

    for (var p in params) { this[p] = params[p]; }
    if (!this.children) { this.children = []; }
};

Parse.Simple.Base.prototype.ruleConstructor = Parse.Simple.Base.Rule;

Parse.Simple.Base.Rule.prototype = {
    regex: null,
    capture: null,
    replaceRegex: null,
    replaceString: null,
    tag: null,
    attrs: null,
    children: null,

    match: function(data, options) {
        return data.match(this.regex);
    },

    build: function(node, r, options) {
        var data;
        if (this.capture !== null) {
            data = r[this.capture];
        }

        var target;
        if (this.tag) {
            target = document.createElement(this.tag);
            node.appendChild(target);
        }
        else { target = node; }

        if (data) {
            if (this.replaceRegex) {
                data = data.replace(this.replaceRegex, this.replaceString);
            }
            this.apply(target, data, options);
        }

        if (this.attrs) {
            for (var i in this.attrs) {
                target.setAttribute(i, this.attrs[i]);
                if (options && options.forIE && i == 'class') { target.className = this.attrs[i]; }
            }
        }
        return this;
    },

    apply: function(node, data, options) {
        var tail = '' + data;
        var matches = [];

        if (!this.fallback.apply) {
            this.fallback = new this.constructor(this.fallback);
        }

        while (true) {
            var best = false;
            var rule  = false;
            for (var i = 0; i < this.children.length; i++) {
                if (typeof matches[i] == 'undefined') {
                    if (!this.children[i].match) {
                        this.children[i] = new this.constructor(this.children[i]);
                    }
                    matches[i] = this.children[i].match(tail, options);
                }
                if (matches[i] && (!best || best.index > matches[i].index)) {
                    best = matches[i];
                    rule = this.children[i];
                    if (best.index == 0) { break; }
                }
            }
                
            var pos = best ? best.index : tail.length;
            if (pos > 0) {
                this.fallback.apply(node, tail.substring(0, pos), options);
            }
            
            if (!best) { break; }

            if (!rule.build) { rule = new this.constructor(rule); }
            rule.build(node, best, options);

            var chopped = best.index + best[0].length;
            tail = tail.substring(chopped);
            for (var i = 0; i < this.children.length; i++) {
                if (matches[i]) {
                    if (matches[i].index >= chopped) {
                        matches[i].index -= chopped;
                    }
                    else {
                        matches[i] = void 0;
                    }
                }
            }
        }

        return this;
    },

    fallback: {
        apply: function(node, data, options) {
            if (options && options.forIE) {
                // workaround for bad IE
                data = data.replace(/\n/g, ' \r');
            }
            //TODO: There should be some agreement on this - sanitization happens serverside anyway.
//            //node.appendChild(document.createTextNode(data));
            $(node).append(data);
        }
    }    
};

Parse.Simple.Base.Rule.prototype.constructor = Parse.Simple.Base.Rule;

Parse.Simple.Creole = function(options) {
    var rx = {};
	rx.img = /\{\{([^{][\S]+?[^~])(\s([^\}]+?[^~]))?\}\}/;
	rx.autoimg = /(?:^|\b)(http:\/\/\S+(?:(jpg|jpeg|gif|png)(\s|$)))/;
    rx.autolink =/\b(?:(?:https?|ftp):\/\/)((\S+?)(?!\.jpg|\.gif|\.png|\jpeg)\S{4})(?=[.,;:!?]\W|\s|$)/;
	rx.link = /\[\[([^[][\S]+?[^~])(\s([^\]]+?[^~]))?\]\]/;

	
    var g = {
        br: { regex: /\n/,
			build: function(node, r, options)  {
				$(node).append('<br />');
			} 
		},
        
        codeBlock: { tag: 'code', capture: 1,
            regex: /\{\{\{([\s\S]*?[^~])\}\}\}/,
			replaceRegex: /["'<>]/g,
			replaceString: function(m) {return {'"':'&quot;', "'":'&#39;', "<":'&lt;', ">":'&gt;'}[m];}
            },
        blockQuote: { tag: 'blockquote', capture: 1,
            regex: /(?:^|\n)(>[\s\S]*?)(?:$|\n(?!>))/,
			replaceRegex: /(^|\n)>\s?/g, replaceString: '$1'
			},
        ulist: { tag: 'ul', capture: 0,
            regex: /(?:^|\n)([ \t]*\.\s.*(\n|$)([ \t]*[^\s.#].*(\n|$))*([ \t]*[.#]{2}.*(?:\n|$))*)+/ },
        olist: { tag: 'ol', capture: 0,
            regex: /(?:^|\n)([ \t]*#\s.*(\n|$)([ \t]*[^\s.#].*(\n|$))*([ \t]*[.#]{2}.*(?:\n|$))*)+/ },
        li: { tag: 'li', capture: 0,
            regex: /[ \t]*([.#]).+(\n[ \t]*[^.#\s].*)*(\n[ \t]*\1[.#].+)*/,
            replaceRegex: /(^|\n)[ \t]*[.#]/g, replaceString: '$1' },
        text: { capture: 0, regex: /(?:^|\n)([ \t]*[^\s].*(\n|$))+/ },
        force: { capture: 1, regex: /\|([\s\S]*?[^~])\|/ },		

        spoiler: { tag: 'span', capture: 1, attrs: {'class':'spoiler'},
            regex: /(?=^|\b|_)\^([\s\S]*?[^~])\^(?=_|\b|$)/},
        strong: { tag: 'strong', capture: 1,
            regex: /(?!\b)\*([^*][\s\S]*?[^~*])\*\B/ },
        em: { tag: 'em', capture: 1,
            regex: /(?=^|\b)_([^_][\s\S]*?[^~])_(?=\b|$)/},
        del: { tag: 'del', capture: 1,
            regex: /--([\s\S]*?[^~])--/},
        ins: { tag: 'ins', capture: 1,
            regex: /(?=^|\b)__([^_][\s\S]*?[^~])__(?=\b|$)/},
        q: { tag: 'q', capture: 1,
            regex: /""([^"][\s\S]*?[^~])""/},

        left: { tag: 'div', capture: 1,
            regex: /<-([\s\S]*?[^~])<-/, attrs:{'class':"text-left"}},
        right: { tag: 'div', capture: 1,
            regex: /->([\s\S]*?[^~])->/, attrs:{'class':"text-right"}},
        center: { tag: 'div', capture: 1,
            regex: /->([\s\S]*?[^~])<-/, attrs:{'class':"text-center"}},

		raw: {tag:'', capture: 1,
			regex: /==([^=][\s\S]*?[^~])==/,
			replaceRegex: /["'<>]/g, replaceString: function(m) {return {'"':'&quot;', "'":'&#39;', "<":'&lt;', ">":'&gt;'}[m];}
		},
		autoimg: { regex: rx.autoimg,
            build: function(node, r, options) {
                var img = document.createElement('img');
                img.alt = img.src = r[1];
                node.appendChild(img);
            } },
		
        img: { regex: rx.img,
            build: function(node, r, options) {
                var img = document.createElement('img');
                img.src = r[1];
                img.alt = r[3] === undefined
                    ? (options && options.defaultImageText ? options.defaultImageText : '')
                    : r[3].replace(/~(.)/g, '$1');
                node.appendChild(img);
            } },

        link: { regex: rx.link,
            build: function(node, r, options) {
                var link = document.createElement('a');
                link.href=r[1];
                if(r[3]) {
                	this.apply(link, r[3], options);
                } else {
                	link.appendChild(document.createTextNode(r[1]));
                }
                node.appendChild(link);
            	}
            },
        autolink: { regex: rx.autolink,
                build: function(node, r, options) {
                    var link = document.createElement('a');
                    link.href=r[0];
                   	link.appendChild(document.createTextNode(r[0]));
                    node.appendChild(link);
                	}
                },

        hashtag: { regex: /(?=^|(?!\b|_))(?:@|#)((?:\[[^\]]+\]|[-\w]+))(?=\W|$)/,
                build: function(node, r, options) {
                    var link = document.createElement('a');
                   	link.appendChild(document.createTextNode(r[0]));
                    node.appendChild(link);
                	}
                },
            
            
        escapedSequence: { regex: '~(' + rx.rawUri + '|.)', capture: 1,
            tag: 'span', attrs: { 'class': 'escaped' } },
        escapedSymbol: { regex: /~(.)/, capture: 1,
            tag: 'span', attrs: { 'class': 'escaped' } }
    };

    g.link.children = [ g.escapedSymbol, g.img, g.strong, g.em, g.ins, g.del, g.autoimg ];

   
    for (var i = 1; i <= 3; i++) {
        g['h' + i] = { tag: 'h' + i, capture: 2,
        	regex:'(?:^|\\n)(\\!{'+(5-i)+'}\\s?(.+?)\\s?\\!{'+(5-i)+'})(?=\\n|$)'
        	};
    }

    g.ulist.children = g.olist.children = [ g.li ];
    g.li.children = [ g.ulist, g.olist ];
    g.li.fallback = g.text;

    g.h1.children = g.h2.children = g.h3.children = g.force.children = 
            g.text.children = g.strong.children = g.em.children = 
			g.blockQuote.children = 
			g.spoiler.children = g.ins.children = g.del.children = 
			g.center.children = g.left.children = g.right.children =
        [ g.escapedSequence, 
          	g.strong, g.em, g.spoiler, g.ins, g.del, g.q, g.force, g.raw, 
          	g.br, g.link, g.autolink, g.hashtag,
			g.center, g.left, g.right, g.codeBlock,
            g.img, g.autoimg ];
	
	g.blockQuote.children.push(g.blockQuote);

    g.root = {
        children: [ g.h1, g.h2, g.h3, g.raw,
            g.ulist, g.olist, g.blockQuote, g.force, g.br],
        fallback: { children: [ g.text ] }
    };

    Parse.Simple.Base.call(this, g, options);
};

Parse.Simple.Creole.prototype = new Parse.Simple.Base();

Parse.Simple.Creole.prototype.constructor = Parse.Simple.Creole;