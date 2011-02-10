'''
Created on 29/mag/2010

@author: pgcd
'''
import re
from django.utils.html import escape
from almparse.signals import parsing_done
#import urllib
#def escape(string):
#        subst=r'([\'"<>]|[\x7f-\xff])'
#        entities={'"':'&quot;', "'":'&#39;', ">":'&gt;', "<":'&lt;'}
#        repl=lambda x: '%s'%entities[x.group(0)] if x.group(0) in entities else ord(x.group(0))
#        return re.sub(subst, repl, string)


class Node(object):
    defaults = {'_start':r'(?<![a-zA-Z0-9])',
                '_end':r'(?![a-zA-Z0-9|])',
                '_startline':r'(?<=^)\s*',
                '_endline':r'\s*(?=\n|$)',
                '_escape':r'\|?'
                }

    def __init__(self, regex = '', tag = '', children = False, attrs = None, allowed_attributes = None, regex_priority = 100):
        self.regex = regex % self.defaults if regex else '^.+$'
        self.tag = tag
        self.attrs = attrs or {}
        self.allowed_attributes = allowed_attributes or []
        self.children = children
        self.regex_priority = regex_priority

    
    def update_attributes(self, body, basedict = None):
        at = True
        basedict = basedict or {}
        while at:
            at = re.search(r'^(\((?P<key>\w+):(?P<quote>[\'"]?)(?P<val>.*?)(?P=quote)\))(?!\s)', body)
            if at:
                basedict.update({at.group('key'):at.group('val')})
                body = body[at.end():]
        attrs = self.attrs.copy()
        attrs.update(basedict)
        return (body, attrs)
        
    def safe_attributes(self, basedict = None):
        safedict = {}
        basedict = basedict or {}
        for d in basedict:
            if d in self.allowed_attributes:        
                safedict[d] = basedict[d]
        return safedict
        
    def build_regex(self):
        prlst = []
        for x in self.children.items():
            if x[1].regex_priority not in prlst:
                prlst.append(x[1].regex_priority)
        prlst.sort()
        regexlst = [[] for x in prlst]
        for x in self.children.items():
            for i, p in enumerate(prlst):
                if x[1].regex_priority == p:
                    regexlst[i].append(x[1].regex)
                    break;
            else:
                pass # uh? if parsing reaches this point there's a bug

        r = r"%s" % '|'.join([r"%s" % '|'.join([x for x in xl]) for xl in regexlst])
        rx = re.compile(r, re.S)
        return rx
    
    def build(self, body, attrs):
        #This method should be somehow overridden in subclasses
#        body, attrs = self.update_attributes(body)
        attrs = self.safe_attributes(attrs)
        if self.tag:
            result = "<%(tag)s%(attrs)s />" if self.children == False else "<%(tag)s%(attrs)s>%(content)s</%(tag)s>"
            attrs = (" " + " ".join(['%s="%s"' % (x[0], escape(x[1])) for x in attrs.items()])) if attrs else ''
            result = result % {'tag':self.tag, 'content':body, 'attrs': attrs}
        else:
            result = body
        return result
    
    def parse(self, text, groupdict = ''):
        def xlate(t):
            rx = self.build_regex()
            m = rx.search(t)
            if not m:
                return t
            head, tail = m.span()
            if m.lastgroup:
                try:
                    content_node = m.group(m.lastgroup + '_content')
                except IndexError:
                    content_node = m.group(m.lastindex + 1)
                text = self.children[m.lastgroup].parse(content_node, m.groupdict())
            else:
                text = m.group()
            return t[:head] + text + xlate(t[tail:])

        text, attrs = self.update_attributes(text) # Text gets cleaned here.
        if not self.children:
            return self.build(text, attrs)
        return self.build(xlate(text), attrs)

class RawHtmlNode(Node):
    def parse(self, body, *args, **kwargs):
        return escape(body)

class CodeNode(Node):
    def parse(self, body, *args, **kwargs):
        return super(CodeNode, self).parse(re.sub('\n', '<br />', escape(body)), *args, **kwargs)


class LineBreakNode(Node):
    def parse(self, body, *args, **kwargs):
        return '<br />'

    
class LinkNode(Node):
    def update_attributes(self, body):
        attrs = self.attrs.copy()
        match = re.search(r'^\s*(?P<href>\S+)\s*((?P<q>[\'"]?)(?P<content>(.+)?)(?P=q))?\s*$', body)
        if match: #TODO: fix regex do that this check is unnecessary
            attrs.update(match.groupdict())
        else:
            attrs.update({'href':'', 'content':''})
        body = attrs.get('content') or attrs['href']
        attrs['href'] = re.sub("^(?!/|http://|ftp://|https://)", "http://", attrs['href'], 1)
        return (body, attrs)

class QuoteNode(Node):
    def update_attributes(self, body):
        attrs = self.attrs.copy()
        body = re.sub(r'(?P<st>^|\n)>\s?', '\g<st>', body)
        try:
            at = re.search(r'^\s?@(?P<user>\[?.*[^~]\]\s*(?=#)|[^[][^\s#]+)\s?(?P<post>\#\d+(?=\s|$))?', body)
            attrs.update(at.groupdict())
            trim = at.end('user')
            if attrs['post']:
                attrs['data-related-post'] = attrs['post'][1:]
                trim = at.end('post')
            attrs['data-related-user'] = attrs['user'].lstrip('[').rstrip('] ')
            if self.tag == 'q':
                body = body[trim:].lstrip()
            else:
                body = body[:trim] + '\n' + body[trim:].lstrip()
        except AttributeError:
            pass
        return (body, attrs)
    
#    def parse(self, text, groupdict):
#        text = re.sub(r'(?P<st>^|\n)>\s?', '\g<st>', text)
#        return super(QuoteNode, self).parse(text, groupdict)
        



class ImgNode(Node):
    def update_attributes(self, body):
        body, attrs = super(ImgNode, self).update_attributes(body)
        match = re.search(r'(?m)^\s*(?P<src>\S+)\s*((?P<q>[\'"]?)(?P<title>(.+?)?)(?P=q)?)?\s*$', body)
        if match: #TODO: fix regex do that this check is unnecessary
            attrs.update(match.groupdict())
        else:
            attrs.update({'src':''})
        attrs['alt'] = attrs.get('title', attrs['src'])
        return ('', attrs)

class AutoImgNode(Node):
    def update_attributes(self, body):
        attrs = self.attrs.copy()
        attrs['src'] = attrs['alt'] = body
        return ('', attrs)

class AutoLinkNode(Node):
    def update_attributes(self, body):
        attrs = self.attrs.copy()
        attrs['href'] = body
        return (body, attrs)
   
class ListNode(Node):
    def parse(self, text, groupdict):
        list_marker = groupdict.get('list_marker') or groupdict.get('ol_marker') or groupdict.get('ul_marker')
        tabs = ' ' * (len(list_marker))
        regex = r'''(?x)(?s)
            (?P<li>[ \t]*
                (?P<list_marker>%(list_marker)s)
                (?P<li_content>.+?)
                (?=
                    \n[ \t]*%(list_marker)s(?![*#])
                    |
                   $(?# The LI ends before the end of the string )
                )
            )''' % {'list_marker':re.escape(list_marker)}
        def xlate(t):
            rx = re.compile(regex, re.S)
            m = rx.search(t)
            if not m:
                return t
            head, tail = m.span()
            if m.lastgroup:
                try:
                    content_node = m.group(m.lastgroup + '_content')
                except IndexError:
                    content_node = m.group(m.lastindex + 1)
                text = self.children[m.lastgroup].parse(content_node, m.groupdict())
            else:
                text = m.group()
            return t[:head].rstrip('\n') + '\n' + tabs + text + xlate(t[tail:])
        return '\n' + tabs + self.build(xlate(text), {}) + '\n'

class MacroNode(Node):
    def parse(self, text, groupdict):
        from almparse.models import Macro
        try:
            m = Macro.objects.get(name = groupdict['macro_name']) #TODO: Filter by user/group/perm
        except Macro.DoesNotExist: #@UndefinedVariable
            return groupdict['macro'].replace('%}', " -- macro not available%}" + groupdict['macro_name']) #TODO: Something prettier
        if m.regex_match:
            if groupdict.get('macro_content'):
                return re.sub(m.regex_match, m.regex_replace, groupdict['macro_content'])
            else:
                return groupdict['macro'].replace('%}', " -- content required%}") #TODO: Something prettier
        else: 
            return m.regex_replace
        
class PluginNode(Node):
    pass

BlockNodes = {
    'macro':MacroNode(regex = r'(?P<macro>\{%%\s*(?P<macro_name>[^:]+?)\s*(?:%%\}|:(?P<macro_content>[^<].+?[^~])?\s*%%\}))'),
    'plugin':PluginNode(regex = r'(?P<plugin><<<(.+?)>>>)'), #TODO:
    'blockquote':QuoteNode(tag = 'blockquote', allowed_attributes = "cite data-related-user data-related-post".split(), regex = r'(?s)(?P<blockquote>(?:^|\n)(>.*?))(?:$|\n(?!>))'),
    'center':Node(tag = 'div', attrs = {'class':"text-center"}, regex = r'(?P<center>->(.*?[^~])<-)', allowed_attributes = ['class']),
    'left':Node(tag = 'div', attrs = {'class':"text-left"}, regex = r'(?P<left><-(.*?[^~])<-)', allowed_attributes = ['class']),
    'right':Node(tag = 'div', attrs = {'class':"text-right"}, regex = r'(?P<right>->((?:[^<]|<[^-])*?[^~])->)', allowed_attributes = ['class']),
    'force':Node(regex = r'(?P<force>\|(.*?[^~])\|)', regex_priority = 50), #force must come after forcein (see below)
    'code':CodeNode(tag = 'code', regex = r'(?P<code>\{\{\{(.*?[^~])\}\}\})', allowed_attributes = ['lang']),
    }

EmptyNodes = {
    'raw': RawHtmlNode(regex = r'(?P<raw>==(.*?[^~])==)'),
    'img':ImgNode(tag = 'img', regex = r'(?P<img>(?<!{)\{\{([^{].+?[^~}])\}\})', allowed_attributes = "src title alt width height border".split()),
    #'img':ImgNode(tag = 'img', regex = r'(?<!{)(?P<img>\{\{(\s*[^{\s]\S*\s*((?P<auximgquote>[\'"]?)(.*?[^~}])?(?P=auximgquote)?)?\s*)\}\})', allowed_attributes = "src title alt width height border".split()),
    'br':LineBreakNode(regex = r'(?P<br>(?<=\n))', tag = 'br', regex_priority = 10),
    'autoimg': AutoImgNode(tag = 'img',
           regex = r'%(_start)s(?P<autoimg>(http://\S+(?:jpg|jpeg|gif|png)))%(_end)s', allowed_attributes = "src title alt".split()),
}

InlineNodes = {
    'forcein':Node(regex = r'(?P<forcein>\|((?P<aux1>[=-_]{2}|[*_^])(\|(?P<aux2>[=-_]{2}|[*_^]).*?(?P=aux2)\||.)*?(?P=aux1))\|)', regex_priority = 20),
    'spoiler':Node(regex = r'%(_start)s(?P<spoiler>\^(.*?[^~])\^)%(_end)s', tag = 'span', attrs = {'class':'spoiler'}, allowed_attributes = ['class']),
    'strong':Node(regex = r'%(_start)s(?P<strong>\*([^~*]|[^* ].*?[^~])\*)%(_end)s', tag = 'strong'),
#    'em':Node(regex = r'%(_start)s(?P<em>_([^_ ].*?[^~])\_)%(_end)s', tag = 'em'),
    'del':Node(regex = r'%(_start)s(?P<del>--(.*?[^~])--)%(_end)s', tag = 'del'),
    'ins':Node(regex = r'%(_start)s(?P<ins>__(.*?[^~])__)%(_end)s', tag = 'ins'),
    'em':Node(regex = r'%(_start)s(?P<em>_([^~_]|[^_].*?[^~_])_(?!_))%(_end)s', tag = 'em'),
    'q':QuoteNode(tag = 'q', allowed_attributes = "data-related-user data-related-post".split(), regex = r'(?P<q>(?<!")""([^"].*?[^~])"")'),
    'a': LinkNode(tag = 'a', regex = r'(?P<a>\[\[(.*?[^~])\]\])', allowed_attributes = "href title".split(" ")),
    #'a': LinkNode(tag = 'a', regex = r'(?P<a>\[\[(\s*\S+\s*((?P<auxaquote>[\'"]?)(.*?[^~])(?P=auxaquote)\s*)|[^~])\]\])', allowed_attributes = "href title".split(" ")),
    'escape':Node(regex = r'(?P<escape>~(.))', tag = 'span', attrs = {'class':'escaped'}, allowed_attributes = ['class']),
    'autolink': AutoLinkNode(tag = 'a',
#           regex = r'(?P<autolink>((?=^|(?<=\s))(?:ftp|https?)://\S+[^.,;:!?]))(?<!\.jpg|\.gif|\.png)(?<!\.jpeg)(?=\s|$|[.,;:!?])', allowed_attributes = ["href"]),
            regex = r'(?P<autolink>(\b(?:(?:https?|ftp)://)((\S+?)(?!\.jpg|\.gif|\.png|jpeg)\S{4})(?=[.,;:!?]\W|\s|$)))', allowed_attributes = ["href"]),
    
    }

TitleNodes = {
    'h1':Node(regex = r'%(_startline)s(?P<h1>\*{4}\s?(.*?[^~])\s?\*{4})%(_endline)s', tag = 'h1'),
    'h2':Node(regex = r'%(_startline)s(?P<h2>\*{3}\s?([^ *].*?[^~])\s?\*{3})%(_endline)s', tag = 'h2'),
    'h3':Node(regex = r'%(_startline)s(?P<h3>\*\*\s?([^ *].*?[^~])\s?\*\*)%(_endline)s', tag = 'h3'),
    }

ListNodes = {
    'ol':ListNode(tag = 'ol', regex = r'''(?x)(?s)
        (?:^|\n)
        [ \t]*
        (?P<ol>(
            (?P<ol_marker>(?:[*#]\s)*(?:\#\s))
            [^*#].*?
        ))
        (?=\n\n|\n[ \t]*(?!(?P=ol_marker))|$)
        '''),
#    'ul':Node(tag='ul', regex=r'(?:^|\n)(?P<ul>([ \t]*\*[^*#].*(\n|$)([ \t]*[^\s*#].*(\n|$))*([ \t]*[*#]{2}.*(\n|$))*)+)'),
    'ul':ListNode(tag = 'ul', regex = r'''(?x)(?s)
        (?:^|\n)
        [ \t]*
        (?P<ul>(
            (?P<ul_marker>(?:[*#]\s)*(?:\*\s))
            [^*#].*?
        ))
        (?=\n(?=\n)|\n[ \t]*(?!(?P=ul_marker))|$)
        '''),
}

li_node = Node(tag = 'li')

li_node.children = ListNodes
li_node.children.update(InlineNodes)
li_node.children['force'] = BlockNodes['force']
ListNodes['ul'].children = {'li':li_node}
ListNodes['ol'].children = {'li':li_node}





Nodes = {}
Nodes.update(InlineNodes)
Nodes.update(BlockNodes)
Nodes.update(EmptyNodes)
Nodes.update(ListNodes)
Nodes.update(TitleNodes)

for n in BlockNodes:
    BlockNodes[n].children = Nodes #They should have all the possible children

for n, v in TitleNodes.items():
    v.children = InlineNodes # node: this actually imports all the EmptyNodes as InlineNodes's children (see below)
    #v.children = InlineNodes.copy() # use this instead of the previous one to remove images and br from titles!
    v.children['raw'] = EmptyNodes['raw']

for n, v in InlineNodes.items():
    v.children = InlineNodes
    v.children.update(EmptyNodes)
    #v.children['autoimg'] = Nodes['autoimg']
    #v.children['br'] = Nodes['br']
    #v.children['forcein'] = Nodes['forcein']
    #v.children['autolink'] = Nodes['autolink']

Nodes['a'].children = {'autoimg':Nodes['autoimg'], 'img':Nodes['img']}

Nodes['autolink'].children = {}
Nodes['code'].children = {} #{'br': Nodes['br']}

def transform(input):
    """
    This is actually the main function.
    """
    root = Node(children = Nodes)
    r = root.parse(input)
    parsing_done.send(root.__class__, text = r)
    return unicode(r)
