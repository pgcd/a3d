"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from almparse.parser import transform

class ParserTest(TestCase):
    def test_inlines(self):
        self.assertEqual(transform("""This __sentence__ will _have_ several *tags*."""),
        u'''This <ins>sentence</ins> will <em>have</em> several <strong>tags</strong>.''')

        self.assertEqual(transform("This_one_won't__have__any. This|^one^|will|_have_|two."),
        """This_one_won't__have__any. This<span class="spoiler">one</span>will<em>have</em>two.""")

    def test_headings(self):
        self.assertEqual(transform("**** This is the _H1_ heading ****"),
                         u'<h1>This is the <em>H1</em> heading</h1>')
        self.assertEqual(transform("*** This is the __H2__ heading ***"),
                         u'<h2>This is the <ins>H2</ins> heading</h2>')
        self.assertEqual(transform("** This is the H3 heading **"),
                        u'<h3>This is the H3 heading</h3>')

    def test_blocks(self):
        self.assertEqual(transform("""->This sentence is centered with some {{{(lang:python)code thrown in}}}<-"""),
                        u'<div class="text-center">This sentence is centered with some <code lang="python">code thrown in</code></div>')
        
        self.assertEqual(transform('''==This is <'"> escaped=='''),
                        u'This is &lt;&#39;&quot;&gt; escaped')
        
    def test_implicit(self):
        self.assertEqual(transform("http://www.google.com"),
                         u'<a href="http://www.google.com">http://www.google.com</a>')
        self.assertEqual(transform("http://www.google.com/test.jpg"),
                         u'<img src="http://www.google.com/test.jpg" alt="http://www.google.com/test.jpg" />')

    def test_links(self):
        self.assertEqual(transform("[[http://www.google.com Google]]"),
                         u'<a href="http://www.google.com">Google</a>')    
        self.assertEqual(transform("[[http://www.google.com {{http://www.google.com/test.jpg Test.jpg}}]]"),
                         u'<a href="http://www.google.com"><img src="http://www.google.com/test.jpg" alt="Test.jpg" title="Test.jpg" /></a>')
        self.assertEqual(transform('{{http://www.google.com/test.jpg "Test.jpg"}}'),
                         u'<img src="http://www.google.com/test.jpg" alt="&quot;Test.jpg&quot;" title="&quot;Test.jpg&quot;" />')
        
    def test_quoted(self):  
        self.assertEqual(transform("> @[username] #123\n> first quoted line\n>> Nested quote\> end quote\n\n"),
                         u'<blockquote data-related-post="123" data-related-user="username">@[username] #123\n<br />first quoted line<blockquote>Nested quote\\> end quote</blockquote></blockquote>\n<br />')
        
        
    def test_nested(self):
        import re
        rx = re.compile('\s')
        r = transform('''
* This should be the first line.
* # Second Line _indented_
* # Third line http://a.link.to
* fourth line back
# A different list
# With four lines
# * And an indented ul
# * With two lines''')
        e = u'''<ul><li>This should be the first line.
<ol>
<li>Second Line <em>indented</em></li>
<li>Third line <a href="http://a.link.to">http://a.link.to</a></li>
</ol>
</li>
<li>fourth line back</li></ul>
<ol>
<li>A different list</li>
<li>With four lines
<ul>
<li>And an indented ul</li>
<li>With two lines</li></ul>
</li></ol>'''
        stripped_r = rx.sub('', r)
        stripped_e = rx.sub('', e)
        self.assertEqual(stripped_r, stripped_e)
