'''
Created on 19/mag/2010

@author: pgcd
'''
from django import template
register=template.Library()


def parsingTag(node, name, required=0):
    r"""
    Decorator to replace the standard tag mini-parser. 
    Will pass all the parameters to the node, in the order given, after filtering out "for" and "as".
    Sample tag:
        @parsingTag("a_tag")
        class ANode(template.Node):
            def __init__(self, someval, retval):
                self.someval=someval
                self.retval=retval
            def render(self, context):
                context[self.retval]=self.someval
                print self.someval
                return ''
    
    Sample template usage:
        {% a_tag for "example" as retval %}
    """
    #@ register.tag(name=name)
    def do_parsing(parser, token):
        args=token.split_contents()
        args=filter(lambda x: x not in ['for', 'as'], args)
        if required<len(args):
            return node(*args[1:])
        else:
            raise template.TemplateSyntaxError, "Tag %s requires at least %s arguments"%(args[0], required)
    register.tag(name, do_parsing)

