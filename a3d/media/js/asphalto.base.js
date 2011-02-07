jQuery(document).ready(function($){ // Makes me feel safer
    a3d.htmlToAlm = function($$){
        $$.find('blockquote').each(function(i, e){
            var $this = $(this);
            var text = a3d.htmlToAlm($this).replace(/^|\n/g, '\n> ');
            //text = '> @['+$this.attr('data-related-user')+'] #'+$this.attr('data-related-post')+'\n'+text;
            $this.replaceWith(text + '\n');
        });
        return $$.text();
    };
    
    a3d.updateQS = function(url, arg){
        var qsstart = url.indexOf('?');
        if (qsstart >= 0) {
            return url + '&' + arg;
        }
        else {
            return url + '?' + arg;
        }
    };
    
    a3d.toggleNonMatchingPosts = function(s){
        if (s) {
            var ls = s.toggleClass('selected').selector;
            if (a3d.selected[ls]) {
                s1 = a3d.selected[ls];
            }
            else {
                s1 = a3d.selected[ls] = Math.ceil(Math.random() * 10000000);
            }
            $('article.post').not(s.parents('article.post')).toggleClass('hidden-for-' + s1);
        }
        else {
            for (sel in a3d.selected) {
                $('article.post').not($(sel).addClass('selected').parents('article.post')).addClass('hidden-for-' + a3d.selected[sel]);
            }
        }
        
        $('article.post').filter(':hidden:not([class*=hidden-for])').show('fast').end().filter('[class*=hidden-for]').hide('fast');
    };
    
    (function(){ //Updates almSettings to add macros
        var macroMenu = {
            name: 'Macro',
            className: 'buttonMacro',
            key: 'M'
        }, dropMenu = [];
        for (n in a3d.alm_available_macros) {
            var m = a3d.alm_available_macros[n];
            dropMenu.push({
                title: m.title,
                name: m.name,
                openWith: '{\%' + m.name + (m.content_required ? ':' : ''),
                placeHolder: (m.content_required ? 'info required' : ''),
                closeWith: '%}'
            });
        }
        macroMenu.dropMenu = dropMenu;
        almSettings.markupSet.push(macroMenu);
        // almSettings.markupSet.push({separator:'',className:'clear-li'});		
    })();
    
    $.fn.extend({
        removeDuplicate: function(){
            // Find another object with the same #id - this should be applied before attaching $this to the document
            var id = this.id;
            if (!id) {
                return this;
            }
            return this;
        },
        childrenWidth: function(){
            var w = 0;
            $(this).children().each(function(){
                w += this.clientWidth;
            });
            return w;
        },
        addMore: function(){
            $.each(this, function(i, e){
                var $e = $(e);
                $e.toggleClass('more', ($e.childrenWidth() > $e.width() || e.scrollHeight > $e.height()));
            });
            return this;
        },
        MIUSetup: function(){
            $.each(this, function(i, e){
                var is_reply = $('article.parent-post').length > 0;
                //Ok, done with the macros now
                $(e).toggleClass('reply', is_reply).markItUp(almSettings).keyup(function(ev){
                    var $p = $('div.previewtext'), $this = $(this);
                    if ($p.length == '0') {
                        // location.hash = 'post-form';
                        $this.focus();
                        //For the very first time, we will scroll the post-form into view.
                        $p = $('<div class="previewtext post post-text"></div>').draggable({
                            helper: 'clone',
                            cursorAt: {
                                top: 10,
                                left: 10
                            },
                            revert: 'invalid',
                            snap: true
                        });
                        $this.parents('form')                        /*.find('textarea')*/
                        .after($p);
                        $p.toggleClass('reply', is_reply);
                    }
                    $p.html('');
                    a3d.creole.parse($p[0], $this[0].value);
                    return true;
                }).scroll(function(ev){
                    var p = $('div.previewtext'), t = this.scrollTop / this.scrollHeight, padding = p.width() - this.scrollWidth, w = p.width() - padding;
                    
                    p.animate({
                        scrollTop: t * p[0].scrollHeight
                    }, 100);
                });
                
            });
            return this;
        }
    });
    
    $.ajaxSetup({
        ifModified: true,
        beforeSend: function(req){
            $('body').addClass('ajaxInProgress');
            return req;
        },
        complete: function(req, code){
            $('body').removeClass('ajaxInProgress');
            return arguments;
        }
    });
    
    $('a.auth-hidden').live('click', function(ev){
        $(this).hide().siblings('ul.auth-hidden').slideDown();
        return false;
    });
    
    //The form type used to post new items.
    $('form.append-to-target').submit(function(){
        var $form = $(this), $target = $($form.attr("data-attach-element")), postData = $form.serializeArray();
        postData.push({
            name: 'is_reply',
            value: $('.parent-post').length > 0?1:0
        });
        if ($target) {
            $.ajax({
                type: 'POST',
                url: $form.attr('action'),
                data: postData,
                dataType: 'html',
                success: function(data, statusText, xhrequest){
                    var val, $form = xhrequest.active_form, $target = xhrequest.target_anchor;
                    try {
                        errors = $.parseJSON(data);
                    } 
                    catch (e) {
                        errors = false;
                    }
                    if (errors) {
                        for (error in errors) {
                            $('#id_' + error).after(' <span class="error">' + errors[error] + '</span>');
                        }
                    }
                    else {
						var $data = $(data);
						//FIXME: This doesn't actually work in replies. Needs immediate fixing.
						$target.attr('data-items-left', $data.attr('data-items-left'));
						$target.attr('data-source-href', $data.attr('data-source-href'));

						//If we attach the *children* we can use the same approach for both replies and threads.
						//TODO: Use the duplicates removing function.
                        $target[$form.attr('data-attach-method')]($data.html());
                        
						
						// reset all fields
                        $form[0].reset();
                        $form.siblings('.previewtext').empty().hide();
                        $form.find('input[name=next_item]').val($data.attr('data-next-item'));
                    }
                },
                beforeSend: function(xhrequest){
                    $form.slideUp('fast');
                    xhrequest.active_form = $form;
                    xhrequest.target_anchor = $target;
                    return xhrequest;
                },
                complete: function(xhrequest){
                    xhrequest.active_form.slideDown('fast');
//                    location.hash = $form.attr("data-attach-element");
                    $('document').trigger('postsAppended');
                    return xhrequest;
                }
            });
            return false;
        }
        else { // No attach element, proceed as usual
            return true;
        }
    });
    
    $('form.quick-submit').live('keypress', function(ev){
        if (ev.ctrlKey && (ev.keyCode == 10 || ev.keyCode == 13)) {
            $(this).submit();
        }
        else {
            return true;
        }
        
    });
    
    
    $('a.tag-link-new').live('click', function(){
        var that = this, $that = $(this);
        
        this.attachTag = function(tag){
            var target_post_id = $that.attr('data-tag-target-object'), target_url = that.href, data = {
                post_id: target_post_id,
                tag_title: tag
            };
            // Now we POST the new association to the view
            $.post(target_url, data, function(responseText, textStatus, XMLHttpRequest){
                $('#post-id-' + target_post_id + '>.post-info .tags-on-post') //Sensible pattern, isn't it? This way only the relevant post is updated even when nested 
					.find('.tag-link:not(.hashtag-link)')
					.remove()
					.end()
					.prepend(responseText)
					.find('input.tag-link-new')
					.hide('fast');
            });
        };
        $that.siblings('input').show().focus().autocomplete({
            source: function(req, add){
                $.getJSON(a3d.url.api_tags_list + "?callback=?", req, function(data){
                    //create array for response objects  
                    var suggestions = [];
                    //process response  
                    $.each(data, function(i, val){
                        suggestions.push(val.title);
                    });
                    //pass array to callback  
                    add(suggestions);
                });
            },
            select: function(e, ui){
                that.attachTag(ui.item.value);
            }
        });
        return false; // We don't wanna move away, do we?
    });
    
    $('input.tag-link-new').live('keypress', function(ev){
        if ((ev.keyCode == 10 || ev.keyCode == 13)) {
            $(this).siblings('a')[0].attachTag($(this).val());
        }
    });
    
    $('ul.post-info .tags-on-post').live('hover', function(event){
        $t = $(this);
        if (event.type == 'mouseover') {
            $t.addClass('show-all').addMore();
        }
        else {
            $t.removeClass('show-all').addMore();
        }
    }).parent().addMore();
    
    
    $('.tag-link-container').live('hover', function(event){
        var $this = $(this);
        if (event.type == 'mouseover') {
            $this.find('a.tag-link-detach').fadeIn('fast');
        }
        else {
            $this.find('a.tag-link-detach').hide();
        }
    });
    
    $('ul.post-info .tags-on-post a.tag-link-detach').live('click', function(){
        var that = this, target_tag = $(that).siblings('a.tag-link').text().substr(1), target_post_id = $(that).attr('data-tag-target-object'), target_url = that.href, data = {
            post_id: target_post_id,
            tag_title: target_tag,
            _method: 'DELETE'
        };
        // Now we POST the new association to the view
        $.post(target_url, data, function(responseText, textStatus, XMLHttpRequest){
            $('#post-id-' + target_post_id + '>.post-info .tags-on-post').find('.tag-link:not(.hashtag-link)').remove().end().prepend(responseText);
        });
        return false;
    });
    
    
    
    /* TODO: Update this */
    $('a.follow-post, blockquote a.post-link').live('click', function(){
        var $this = $(this);
        if ($this.is('blockquote a.post-link')) { // blockquote post-links should follow ONLY when they're the actual cited post
            if ($this.parent('blockquote').attr('data-related-post') != $this.text().replace(/^#/, '')) {
                return true;
            }
        }
        var followedPost = $this.attr('data-followed-post') || $this.text().replace(/^#/, '');
        a3d.toggleNonMatchingPosts($('#post-id-' + followedPost + '>.post-info .follow a, a.post-link:contains(#' + followedPost + ')'));
        return false;
    });
    $('a.follow-tag').live('click', function(){
        a3d.toggleNonMatchingPosts($('a.tag-link:contains(' + $(this).text().replace(/^#/, '') + ')'));
        return false;
    });
    
    $('.follow-user, blockquote a.user-link').live('click', function(){
        var $this = $(this);
        var followedUser = $this.attr('data-followed-user') || escape($this.text().replace(/^@\[?(.*?)\]?$/, '$1'));
        if ($this.is('blockquote a.user-link')) { // blockquote user-links should follow ONLY when they're the actual cited user
            if ($this.parent('blockquote').attr('data-related-user') != followedUser) {
                return true;
            }
        }
        a3d.toggleNonMatchingPosts($('a.user-link:contains(' + unescape(followedUser) + '), a.follow-user[data-followed-user=' + followedUser + ']'));
        return false;
    });
    
    $('a.endless-paginator').live('click', function(){
        var that = this;
        var paginate_type = this.href.match("start=-") ? 'down' : 'up';
        $.get(this.href + '&' + paginate_type + '=true', function(data){
            var $items = $(data).children('li');
            $.each($items, function(i, e){ //TODO: Update this to reflect changes in structure
                var id = e.id;
                if (id) {
                    var oldel = $('#' + id);
                    if (oldel.length) {
                        // oldel.replaceWith(e);
                        oldel.remove();
                        $(e).addClass('updated');
                    }
                }
            });
			var $target = $('.new-content'); //TODO: Must be specified further
            $target[$(that).attr('data-attach-method')]($items);
			$target.attr('data-items-left', $(data).attr('data-items-left'));
			$target.attr('data-source-href', $(data).attr('data-source-href'));
            $('#post-form').find('input[name=next_item]').val($('#new-content').attr('data-next-item'));
			// Replace the current paginators.
			$(that).replaceWith($('<p/>').html(data).find('a.endless-paginator[rel='+that.rel+']'));
			
            a3d.toggleNonMatchingPosts(); //Update the filtered posts
        });
        return false;
    });
    
    
    $(".markitup textarea").MIUSetup();
    
    $('div.previewtext').live('dragstart', function(ev){
        $('#preview-anchor-right, #preview-anchor-bottom').show('fast');
    }).live('dragstop', function(ev){
        $('#preview-anchor-right, #preview-anchor-bottom').hide();
    });
    
    $('#preview-anchor-right, #preview-anchor-bottom').droppable({
        accept: 'div.previewtext',
        hoverClass: 'preview-anchor-hover',
        tolerance: 'touch',
        drop: function(event, ui){
            var $anchor = $(this), $preview = $(ui.draggable), $form = $('#post-form');
            if ($anchor.is('#preview-anchor-right')) {
                var w = ($form.width() / 2 - 5) * 0.9;
                $form.find('form').width(w);
                $preview.width(w).position({
                    my: 'left',
                    at: 'right',
                    of: $('#post-form textarea'),
                    offset: '10 0'
                });
            }
            else {
                // .position({my:'top',at:'bottom left',of:$('#post-form input[type=submit]'),offset:'0 10'});
                $preview.removeAttr('style');
                $form.find('form').width('100%');
            }
            
        }
    });
    
    
    $('body').mousemove(function(ev){
        var p = $(ev.target).parents('article.post'), t = p.length ? p[0] : false;
        a3d.hover_on_post = t;
        
    });
    
    /**
     * Add replies' hashtags to parent article
     */
    $('article.parent-post').mouseenter(function(){
        var $this = $(this).children('ul.post-info'), ht = {}, $storage = $('<p>');
        $('.hashtag-link').each(function(i, e){
            var t = $(e).text();
            if (!ht[t]) {
                ht[t] = true;
                $storage.append($(e).clone());
                $storage.html($storage.html() + ' ');
            }
        });
        $storage.children('a.hashtag-link').wrap('<li />');
        $this.find('.tags-on-post li:has(.hashtag-link)').remove().end().find('.tags-on-post').append($storage.html());
    }).mouseenter();
    
    
    $('article.post').live('hover', function(event){
        var that = this, $i = $(this).children('ul.post-info'), // Only the first child needs to be updated, I think.
 $items = $i.find('.on-request');
        if (event.type == 'mouseover') {
            window.setTimeout(function(){
                if (a3d.hover_on_post == that) {
                    $(that).addClass('unhide');
                    $i.find('.tags-on-post').addClass('enlarged').addMore();
                    $items.show();
                }
            }, 150);
        }
        else {
            if ($(this).is('.parent-post')) {
                return;
            }
            window.setTimeout(function(){
                if (!a3d.hover_on_post || a3d.hover_on_post != that) {
                    $items.hide('fast');
                    $i.find('.tags-on-post').removeClass('enlarged').addMore();
                    $(that).removeClass('unhide');
                }
            }, 1500);
        }
    }).live('mousedown', function(ev){
        var $t = $(ev.target);
        if ($t.is('#linked_quote') || $t.parent('.previewtext').length) {
            return;
        }
        if ($t.is('div.post-text, div.post-text *')) {
            a3d.clicked_on_post = $t.closest('article.post');
        }
        else {
            a3d.clicked_on_post = false;
        }
    }).live('mouseup', function(ev){
        if ($(ev.target).parent('.previewtext').length) {
            return;
        }
        if (!$('#post-form form').length) {
            return; // No post form, pointless to proceed.
        }
        
        var t = '', lq = $("#linked_quote");
        lq = (lq.length) ? lq : $('<a id="linked_quote" class="interaction">&#8220;&#8221;</a>');
        // A different take on retrieving the selection; this one would actually allow to also copy ALM tags.
        s = window.getSelection ? window.getSelection() : document.selection.createRange();
        try {
            r = s.getRangeAt(0);
            df = r.cloneContents();
            $c = $('<p>').append(df);
            t = a3d.htmlToAlm($c);
            
        } 
        catch (e) {
            t = '';
        }
        
        if (t.length && a3d.clicked_on_post) {
			//FIXME: Doesn't work when clicked_on_post is the parent and the mouseover is on a child.
            var $tg = $(this);
			var xy = $tg.prepend(lq).offset(); 
			var left = Math.min(Math.max(ev.pageX - xy.left, 0), $tg.width() - lq.width()); 
			var top = Math.min(Math.max(ev.pageY - xy.top, 0), $tg.height() - lq.height());
            lq.css({
                'left': left,
                'top': top,
                'display': 'block'
            }).data('quoted_text', t);
        }
        else {
            lq.fadeOut('fast');
        }
    });
    
    $("#linked_quote").live('click', function(ev){
        var quote = '> @[' + $(a3d.clicked_on_post).children('.post-info').find('.user-link[rel=author]').text() +
        '] #' +
        a3d.clicked_on_post.attr('id').replace('post-id-', '') +
        '\n' +
        $(this).data('quoted_text').replace(/(^|\n)/g, '$1> ') +
        '\n\n'; //TODO: Improve this to also copy some/all markup
        $.markItUp({
            target: '#post-form form textarea',
            replaceWith: quote
        });
        $('#post-form form textarea').keyup();
        $(this).fadeOut('fast');
        return false;
    });
    
    $('article.post>ul.post-info span.rate-actions a').live('click', function(ev){
        var $this = $(this); 
		var $target = $this.closest('article.post');
		var href = $this.attr('href').replace(/([\?&]next_page=)[^&]+/, '$1' + location.pathname);
        $.get(href + '&as_reply=' + $target.hasClass('reply'), function(data, request){
			//TODO: Deal with 403 Forbidden!
            $target.children('.post-info')
				.replaceWith(data)
				.mouseenter(); //Nice way of dealing with navigation issues.
        });
        return false;
    });
    
    $('a.mark-read,a.mark-unread').live('click', function(ev){
        var $this = $(this);
        $.get($this.attr('href'), function(data, request){
            $this.parents('ul.post-info').replaceWith(data).closest('.post').mouseenter();
        });
        return false;
    });
    
    $('#post-form input#id_title').autocomplete({
        minLength: 2,
        search: function(ev, ui){
            var v = this.value, li = v[0] == '@' ? 0 : v.lastIndexOf('[');
            if ((v[0] != '@' && v[0] != '[') || li <= v.lastIndexOf(']') || v.substr(li + 1).length < 2) {
                return false;
            }
        },
        source: function(req, add){
            var url;
            if (req.term[0] == '@') {
                url = a3d.url.api_users_list;
                req.term = req.term.substr(1);
            }
            else {
                url = a3d.url.api_tags_list;
                req.term = req.term.substr(req.term.lastIndexOf('[') + 1);
            }
            $.getJSON(url, req, function(data){
                //create array for response objects  
                var suggestions = [];
                //process response  
                $.each(data, function(i, val){
                    suggestions.push({
                        label: val.title || val.username,
                        value: val.username ? '@[' + val.username + ']' : '[' + val.title + ']'
                    });
                });
                //pass array to callback  
                add(suggestions);
            });
        },
        focus: function(e, ui){
            return false;
        },
        select: function(e, ui){
            this.value = this.value.substr(0, this.value.lastIndexOf('[')) + ui.item.value;
            return false;
        }
    });
    
	/*
	 * Show the few last elements of a list in a floating window
	 */
	$('a.brief-available').live('hover', function(ev){
		var $this=$(this);
		var timeout = $this.data('timeout');
		var $floater = $('ol.brief');
		if(timeout) {
			window.clearTimeout($this.data('timeout'));	
		}
		if(ev.type=='mouseover') {
			timeout = window.setTimeout(function() {
				$.get($this.attr('data-brief-href'), function(data) {
					$('.ajaxInProgress').removeClass('ajaxInProgress');
					$floater = $(data).appendTo('body');
					$floater.css({position:'absolute',left:ev.clientX, top:ev.clientY})
				})				
			},250);
			$this.data('timeout', timeout);
		} else {
			if($floater.length) {
				$floater.remove();	
			}
		}
	});
	
    
    //In-place editing
    $('a.post-edit-link').live('click', function(ev){
        // Retrieve the form and use it to replace the relevant bits
        $('a.edit-revert').click(); //this is supposed to revert everything, right?
        var $this = $(this);
        $this.data('revert', $this.closest('.post').clone(true))
			.addClass('edit-revert')
			.attr('title', 'cancel')
			.html('&ne;') //TODO: Cleaner solution required
			.click(function(ev){
	            $this.closest('form').replaceWith($this.data('revert'));
	            $this.attr('title', 'edit').html('&equiv;').parent().addClass('on-request');
	            return false;
	        }).parent().removeClass('on-request');
        $.get(this.href, function(data, req){
            /*
             * This function sets up the form for the in-place editing.
             */
            var $form = $(data),
				post_div = $($form.attr('data-replace-element')),
				title_input_original = $form.find('#id_edit-title'), 
				title_input = title_input_original.clone(), 
				body_markup_input_original = $form.find('#id_edit-body_markup'), 
				body_markup_input = body_markup_input_original.clone();
			post_div.children('header').find('.post-title').replaceWith(title_input); //TODO: Should we allow users to add a title when editing?
            if (post_div.children('.post-text').length) {
                post_div.children('.post-text').replaceWith(body_markup_input);
            }
            else {
                post_div.append(body_markup_input);
            }
            post_div.addClass('editing');
            post_div.before($form);
            $form.children('input[type=submit]').hide();
            $form.find('.replace-with-content').replaceWith(post_div);
            $form.find('textarea').MIUSetup();
        });
        return false;
    });
    
    $('form.replace-target').live('submit', function(ev){
        var url = this.action, $this = $(this);
        $.ajax({
            url: url,
            data: $this.serializeArray(),
            success: function(data, req){
				var $target = $('#'+$(data).attr('id'));
				if($target.find('form.replace-target').length > 0) {
					$target.replaceWith(data); //Replies					
				} else {
					$this.replaceWith(data); //Main posts
				}
				
            },
            context: $this,
            type: 'POST'
        });
        return false;
    });
    
    
    
    /*  Menus stuff */
    $('#menu').accordion({
        clearStyle: true,
        autoHeight: false,
        collapsible: false,
        active: (function(){
            if ($('#auth a.logout-user-link').length === 0) {
                return 0;
            }
            else 
                if ($('#mentions-list ul li a.fresh-content').length > 0) {
                    return 1;
                }
                else 
                    if ($('#fave-list ul li a.fresh-content').length > 0) {
                        return 2;
                    }
            return $('#tags-list').index('#menu div');
        })()
    });
    
    $('#tags-list input#tags-lookup').autocomplete({
        source: function(req, add){
            $.getJSON(a3d.url.api_tags_list, req, function(data){ //FIXME: This shouldn't come from API, I think.
                var suggestions = [];
                $.each(data, function(i, val){
                    suggestions.push(val.title);
                });
                add(suggestions);
            });
        },
        select: function(e, ui){
            location.href = a3d.url.board_post_list_by_tag_title.replace('dummy', ui.item.value);
        }
    });
    
    updateTagsList = function(){ // I don't like this version very much but whatever.
    	/*
    	 * TODO: Normalize this -> use data-source-href etc.
    	 */
        if (a3d.stop_updates) {
            return;
        }
		var $tags = $('#tags-list ul'); 
		$.get(a3d.updateQS($tags.attr('data-source-href'), 'after='+$tags.attr('data-next-item')), 
			function(data, result, req) {
			if (result == 'success') {
				var $data = $(data);
				$tags.attr('data-next-item', $data.attr('data-next-item'));
				$data.children('li').each(function(i, e) {
					$tags.find('#'+e.id).remove();
				});
				$tags.prepend($data.html());
				}
			});
        
    };
    
    updateMentionsList = function(){
        if (a3d.stop_updates) {
            return;
        }
        var oc = $('#mentions-list ul');
        if (!oc.length) {
            return;
        }
        $.get(a3d.url.board_own_mentions_list + '?after=' + oc.attr('data-latest-mention'), function(data, result, req){
            if (result == 'success') {
                var $d = $(data), latest = $d.attr('data-latest-mention');
                oc.attr('data-latest-mention', latest);
                $d.children('li').prependTo(oc);
                $('#menu').accordion('activate', $('#mentions-list').index('#menu div'));
            }
        });
    };
    
    
    
    redrawFaveList = function(data){
        /*var l = $('#fave-list'), oc = l.find('ul');
         l.css({overflow:'hidden', height:l.height()});
         $(data).hide().prependTo(l).slideDown(function() {
         oc.remove();
         // l.height('auto').css({overflow:'visible'});
         });*/
        $('#fave-list ul').replaceWith(data); // Simpler, and I think I actually like it more - if anybody comes up with a different transition we'll talk.
    };
    updateFaveList = function(){
        if (a3d.stop_updates) {
            return;
        }
        
        $.get(a3d.url.board_fave_list, function(data, req){
            redrawFaveList(data);
        });
    };
    
    //FIXME: This still doesn't really work with click and move (as opposed to click and drag)
    $('a.post-link, a.user-link, a.tag-link').draggable({
        delay: 100,
        scope: 'stars',
        helper: 'clone',
        distance: 20,
        revert: 'invalid',
        zIndex: 1000,
        start: function(ev, ui){
            var p = $(this).offsetParent('.post');
            p.css('overflow', 'visible');
            $('#menu').accordion('activate', $('#fave-list').index('#menu div'));
        },
        stop: function(ev, ui){
            $(this).offsetParent('.post').css('overflow', 'hidden');
        }
        
    });
    
    $('#fave-list').droppable({
        greedy: true,
        tolerance: 'touch',
        scope: 'stars',
        activeClass: 'fave-droppable-active',
        drop: function(ev, ui){
            $.post('/star/', {
                link_href: ui.draggable.attr('href')
            }, function(data, req){
                redrawFaveList(data);
            });
        }
    });
    
    $('.toggle-star a').live('click', function(ev){
        a3d.fave_link = $(this);
        $.post(this.href, function(data){
            var was_added = a3d.fave_link.hasClass('add-star');
            a3d.fave_link.attr('href', data.new_href).toggleClass('on-request', !was_added).switchClass('add-star', 'remove-star').html(was_added ? '&diams;' : '&loz;').attr('title', was_added ? 'unstar' : 'star');
            updateFaveList();
        });
        return false;
    });
    
    
    $('.scroller').live('mousemove', function(event){
        var percentile = (event.clientY - this.offsetTop) / this.offsetHeight; //TODO: Check clientTop
        var speed, steps;
        if (this.scrollHeight > this.clientHeight) {
            speed = Math.abs(0.5 - Math.abs(percentile)) * 250;
            if (percentile < 0.15 && percentile > 0) {
                steps = this.scrollTop / 15;
                $(this).animate({
                    scrollTop: 0
                }, speed * steps);
            }
            else 
                if (percentile > 0.85 && percentile < 1) {
                    steps = (this.scrollHeight - this.clientHeight - this.scrollTop) / 15;
                    $(this).animate({
                        scrollTop: this.scrollHeight - this.clientHeight
                    }, speed * steps);
                }
                else {
                    $(this).stop(true, false);
                }
        }
    });
    
    
    $('#fave-list ul li').live('hover', function(event){
        if (event.type == 'mouseover') {
            $(this).children('a.remove-star,a.last-read').fadeIn('fast');
        }
        else {
            $(this).children('a.remove-star,a.last-read').hide();
        }
    });
    
    $('#fave-list ul li a.remove-star').live('click', function(ev){
        $.get(this.href, function(data){
            updateFaveList();
        });
        return false;
    });
    
	
	a3d.startUpdating = function(){
		/*
		 * TODO: All very nice but as soon as the first 200 OK, we need to change the HREF, otherwise it's all gonna
		 * be 200 OK even if it's actually a 304 wrt the first 200.
		 */
		var new_content_interval = a3d.personal_settings.new_content_fetch_interval;
		$('.new-content').each(function(i,el) {
			var $this = $(this);
			$this.data('contentUpdateTimer', window.setInterval(function() {
		        if (a3d.stop_updates) {
    		        return;
        			}
				var href = $this.attr('data-source-href');
				$.get(a3d.updateQS(href, 'count='+$this.attr('data-items-left')||''), function(data, status, request){
		            if (status == 'success') {
		                var paginator = $('<div>').append(data).find('.endless-paginator');
						$this.attr('data-items-left', paginator.attr('data-items-left'));
		                var old_paginator = $('.endless-paginator[rel=' + paginator.attr('rel') + ']');
		                if (old_paginator.length) {
		                    old_paginator.replaceWith(paginator);
		                }
		                else {
		                    $this.parent()[paginator.attr('data-attach-method')](paginator);
		                }
		            }
		        });
			}, $this.attr('data-content-update-interval')*1000 || new_content_interval));
		});

		/*
		 * I'm moving these here, even though they need to be somewhere else.
		 */
	    window.setInterval(function(){
	        if ($('#tags-list').is(':visible')) {
	            updateTagsList();
	        }
	    }, a3d.personal_settings.tags_fetch_interval);
	    window.setInterval(function(){
	        if ($('#fave-list').is(':visible')) {
	            updateFaveList();
	        }
	    }, a3d.personal_settings.favorites_fetch_interval);
	    window.setInterval(updateMentionsList, a3d.personal_settings.mentions_fetch_interval);
		return this; //TODO: Make this return a more sensible value?
	};
	
	
    //Content updating
    updateContent = function(){
		/*
		 * TODO: Update this to work for ALL .new-content elements with the correct tags.
		 */
        var href = $('.new-content').attr('data-source-href');
        $.get(a3d.updateQS(href, 'count=true'), function(data, status, request){
            if (status == 'success') {
                var paginator = $('<div>').append(data).find('.endless-paginator');
                var old_paginator = $('.endless-paginator[rel=' + paginator.attr('rel') + ']');
                
                if (old_paginator.length) {
                    old_paginator.replaceWith(paginator);
                }
                else {
                    $('#new-content').before(paginator);
                }
            }
        });
    };
    
    $('input#stop-updates').click(function(){
        a3d.stop_updates = this.checked;
		if(!a3d.stop_updates) {
			a3d.startUpdating();
		}
    });
	a3d.startUpdating();
});
