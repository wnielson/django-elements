// -------------------------------------------------------------------
// markItUp!
// -------------------------------------------------------------------
// Copyright (C) 2008 Jay Salvat
// http://markitup.jaysalvat.com/
// -------------------------------------------------------------------
// MarkDown tags example
// http://en.wikipedia.org/wiki/Markdown
// http://daringfireball.net/projects/markdown/
// -------------------------------------------------------------------
// Feel free to add more tags
// -------------------------------------------------------------------

// TODO: DO NOT HARD CODE THIS!
var ELEMENTS_URL = '/admin/elements/elementtype/get_types/';

mySettings = {
	previewParserPath:	'',
	onShiftEnter:		{keepDefault:false, openWith:'\n\n'},
	markupSet: [
		{name:'Heading 1', key:'1', openWith:'# ', placeHolder:'Your title here...' },
		{name:'Heading 2', key:'2', openWith:'## ', placeHolder:'Your title here...' },
		{name:'Heading 3', key:'3', openWith:'### ', placeHolder:'Your title here...' },
		{name:'Heading 4', key:'4', openWith:'#### ', placeHolder:'Your title here...' },
		{name:'Heading 5', key:'5', openWith:'##### ', placeHolder:'Your title here...' },
		{name:'Heading 6', key:'6', openWith:'###### ', placeHolder:'Your title here...' },
		{separator:'---------------' },		
		{name:'Bold', key:'B', openWith:'**', closeWith:'**'},
		{name:'Italic', key:'I', openWith:'_', closeWith:'_'},
		{separator:'---------------' },
		{name:'Bulleted List', openWith:'- ' },
		{name:'Numeric List', openWith:function(markItUp) {
			return markItUp.line+'. ';
		}},
		{separator:'---------------' },
		{name:'Picture', key:'P', replaceWith:'![[![Alternative text]!]]([![Url:!:http://]!] "[![Title]!]")'},
		{name:'Link', key:'L', openWith:'[', closeWith:']([![Url:!:http://]!] "[![Title]!]")', placeHolder:'Your text to link here...' },
		{separator:'---------------'},	
		{name:'Quotes', openWith:'> '},
		{name:'Code Block / Code', openWith:'(!(\t|!|`)!)', closeWith:'(!(`)!)'},
		{separator:'---------------'},
		{name:'Preview', call:'preview', className:"preview"},
		{name:'Element', className: 'element', openWith: function(h) {
		    // Load the plugin the first time the button is pressed
		    if (!h.textarea.elements) {
		        h.textarea.elements = new ElementsPlugin(h.textarea);
		    }
		}}
	]
}

function ElementsPlugin(textarea) {
    this.textarea = textarea;
    this.elementTypes = {};
    
    // Insert the HTML element into the DOM
    $(textarea).prev('.markItUpHeader').find('ul').after(this.buildEl());
}

ElementsPlugin.prototype.buildEl = function() {
    var id = this.textarea.id,
        me = this,
        div = $('<div>').addClass('markItUpElementsPlugin'),
        p = $('<p>').addClass('aligned'),
        select = $('<select style="margin-right: 10px;">').attr('id', 'id_element_content_type-'+id).change(function(evt) {
            value = me.elementTypes[this.value];
            url = value.content_type__app_label+'/'+value.content_type__model;
            url = '../../../'+url+'/';
            
            // Add any filters that are defined for this element type
            if (value.default_filters) {
                url += '?'+value.default_filters;
            }
            
            document.getElementById('lookup_id_inline-'+id).href = url;
        }),
        a = $('<a>').attr('id', 'lookup_id_inline-'+id).addClass('related-lookup').click(function() {
            if (document.getElementById('id_element_content_type-'+id).value != '----------') {
                return showRelatedObjectLookupPopup(this);
            }
            return false;
        }),
        input = $('<input type="button" value="Add" style="margin-left:10px;" />').click(function() {
            me.createElement();
        });
    
    p.append('<strong style="margin-right: 10px;">Type:</strong>');
    
    select.append('<option>----------</option>');
    $.getJSON(ELEMENTS_URL, function(data) {
        $.each(data, function(key, val) {
            me.elementTypes[val.id] = val;
            select.append('<option value="'+val.id+'">'+val.title+' ('+val.content_type__app_label+': '+val.content_type__model+')</option>');
          });
    });
    
    p.append(select);
    p.append('<strong style="margin-right: 10px;">Object:</strong>');
    p.append('<input type="text" class="vIntegerField" id="id_inline-'+id+'" size="10" style="margin-right: 10px;" />');
    a.append('<img src="'+__admin_media_prefix__+'img/selector-search.gif" width="16" height="16" alt="Loopup" />');
    p.append(a);
    p.append(input);
    
    div.append(p);
    
    return div;
}

ElementsPlugin.prototype.createElement = function() {
    var element,
        app_label,
        model_name,
        title,
        object_id = $('#id_inline-'+this.textarea.id).val(),
        val = $('#id_element_content_type-'+this.textarea.id).val();
    
    if (val) {
        bits = val.split('/');
        app_label = bits[0];
        model_name = bits[1].split(':')[0];
        title = bits[1].split(':')[1];
        type = val.replace('/', '.');
    }
    
    if (app_label && model_name && object_id) {
        element = "[[El('"+title+"', id='"+object_id+"')]]";
        this.insert(element);
    }
}

ElementsPlugin.prototype.insert = function(value) {
    this.textarea.focus();
    
    if (document.selection) {
        // IE
        sel = document.selection.createRange();
        sel.text = value;
    } else if (this.textarea.selectionStart || this.textarea.selectionStart == '0') {
        //Mozilla/Firefox/Netscape 7+
        var startPos = this.textarea.selectionStart,
            endPos = this.textarea.selectionEnd;
        
        this.textarea.value = this.textarea.value.substring(0, startPos) + value + this.textarea.value.substring(endPos, this.textarea.value.length);
        this.textarea.setSelectionRange(endPos+value.length, endPos+value.length);
    } else {
        this.textarea.value += value;
    }
}
