// ----------------------------------------------------------------------------
// markItUp!
// ----------------------------------------------------------------------------
// Copyright (C) 2008 Jay Salvat
// http://markitup.jaysalvat.com/
// ----------------------------------------------------------------------------
// Html tags
// http://en.wikipedia.org/wiki/html
// ----------------------------------------------------------------------------
// Basic set. Feel free to add more tags
// ----------------------------------------------------------------------------
mySettings = {	
	onShiftEnter:  	{keepDefault:false, replaceWith:'<br />\n'},
	onCtrlEnter:  	{keepDefault:false, openWith:'\n<p>', closeWith:'</p>'},
	onTab:    		{keepDefault:false, replaceWith:'    '},
	markupSet:  [ 	
		{name:'Bold', key:'B', openWith:'(!(<strong>|!|<b>)!)', closeWith:'(!(</strong>|!|</b>)!)' },
		{name:'Italic', key:'I', openWith:'(!(<em>|!|<i>)!)', closeWith:'(!(</em>|!|</i>)!)'  },
		{name:'Stroke through', key:'S', openWith:'<del>', closeWith:'</del>' },
		{separator:'---------------' },
		{name:'Picture', key:'P', replaceWith:'<img src="[![Source:!:http://]!]" alt="[![Alternative text]!]" />' },
		{name:'Link', key:'L', openWith:'<a href="[![Link:!:http://]!]"(!( title="[![Title]!]")!)>', closeWith:'</a>', placeHolder:'Your text to link...' },
		{separator:'---------------' },
		{name:'Clean', className:'clean', replaceWith:function(markitup) { return markitup.selection.replace(/<(.*?)>/g, "") } },		
		{name:'Preview', className:'preview',  call:'altPreview'}
	]
}

function checkIfMidWord(h) {
		var c = h.caretPosition,
			t = h.textarea,
			before = t.value.substr(c-1,1), //we need two chars
			after = t.value.substr(c+h.selection.length,1),
			// check if a break is required before the word
			hasBreakBefore = before.match(/[^a-zA-Z0-9]/),
			hasBreakAfter = after.match(/[^a-zA-Z0-9]/)
		
		if (!h.oldOpenWith) {
			h.oldOpenWith = h.openWith
		}
		if (!h.oldCloseWith) {
			h.oldCloseWith = h.closeWith
		}
		if (hasBreakBefore && hasBreakAfter) {
			h.openWith = h.oldOpenWith;
			h.closeWith = h.oldCloseWith;
		} else {
			h.openWith = '|'+h.oldOpenWith;
			h.closeWith = h.oldCloseWith+'|';
		}
		
	}

almSettings = {
	previewParserPath: '/p/preview',
    nameSpace:          "alm", // Useful to prevent multi-instances CSS conflict
    //previewParserPath:  "~/sets/wiki/preview.php",
    onShiftEnter:       {keepDefault:false, replaceWith:'\n\n'},
	onTab:    		{keepDefault:false, replaceWith:'    '},
    markupSet:  [
        {name:'Bold', className:'buttonBold', key:'B', openWith:"*", closeWith:"*", beforeInsert: checkIfMidWord}, 
        {name:'Italic', className:'buttonItalic', key:'I', openWith:"_", closeWith:"_", beforeInsert: checkIfMidWord}, 
        {name:'Stroke', className:'buttonStroke', key:'S', openWith:'--', closeWith:'--', beforeInsert: checkIfMidWord}, 
		{name:'Underline', className:'buttonUnderline', key:'U', openWith:'__', closeWith:'__', beforeInsert: checkIfMidWord},
		{name:'Spoiler', className:'buttonSpoiler', key:'P', openWith:'^', closeWith:'^', beforeInsert: checkIfMidWord},
        {separator:'---------------' },
        {name:'Image', className:'buttonImage', key:'I', openWith:'{{[![Url:!:http://]!](!( [![Title]!])!)',closeWith:'}}'}, 
        {name:'Link', className:'buttonLink', key:'L', openWith:'[[[![Url:!:http://]!] ', closeWith:']]', placeHolder:'Your text to link here...' },
        {separator:'---------------' },
        {name:'Blockquote', className:'buttonBlockquote', key:'Q', openWith:'> '},
        {name:'Code', className:'buttonCode', openWith:'(!({{{|!|{{{([![Language:!:php]!]))!)', closeWith:'}}}'}, 
		{name:'Escaped HTML', className:'buttonEscapedHTML', key:'H', openWith:'==', closeWith:'=='},
		{name:'Center', className:'buttonCenter', key:'N', openWith:'->', closeWith:'<-'},

        {separator:'---------------' },
        {name:'Heading 1', className:'buttonHeading1', key:'1', openWith:'**** ', closeWith:' ****', placeHolder:'Your title here...' },
        {name:'Heading 2', className:'buttonHeading2', key:'2', openWith:'*** ', closeWith:' ***', placeHolder:'Your title here...' },
        {name:'Heading 3', className:'buttonHeading3', key:'3', openWith:'** ', closeWith:' **', placeHolder:'Your title here...' },
        {separator:'---------------' },        
        {name:'Bulleted list', className:'buttonBulletedList', openWith:'* '}, 
        {name:'Numeric list', className:'buttonNumericList', openWith:'# '}, 
		
        {separator:'---------------' },
        {name:'Preview', call:'preview', className:'preview'}
    ]
}