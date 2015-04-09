<h1>Formatting Syntax</h1>
A3 supports some simple markup language, which tries to make the datafiles to be as readable as possible. This page contains all possible syntax you may use when editing the pages.
<h2>Basic Text Formatting</h2>
A3 supports <strong>bold</strong>, <em>italic</em>, <u>underlined</u> and <s>strikedout</s> texts. Of course you can <u><strong><em><s>combine</s></em></strong></u> all these.

```
A3 supports *bold*, _italic_, __underlined__ and --strikedout-- texts. Of course you can 
__*_--combine--_*__ all these. 
```

You can also <p align='center'>center</p> the text.

Or make it `monospaced` (WARNING: no markup or html allowed in monospaced text `*see*?`

`<span style="font-size=50pt;">SEE?!</span>`).


You can even make it <span>censored</span>!

```
You can also ->center<- the text. 

Or make it {{{monospaced}}} (WARNING: no markup or html allowed in monospaced
text {{{*see*? <span style="font-size=50pt;">SEE?!</span>}}}). 

You can even make it ^censored^! 
```


<h2>Links</h2>
A3 supports multiple ways of creating links.

<h3>External</h3>
External links are recognized automatically: <a href='http://www.google.com'><a href='http://www.google.com'>http://www.google.com</a></a> but not www.google.com - You can set the link text as well: <a href='http://www.google.com'>This Link points to google</a>. Email addresses like this one: spam\_me@asphalto.org are not recognized.

```
A3 supports multiple ways of creating links. External links are recognized automatically:
http://www.google.com but not www.google.com - You can set the link text as well:
[[http://www.google.com This Link points to google]].
Email addresses like this one: spam_me@asphalto.org are not recognized.
```

<h3>Internal</h3>
You can link directly a <a>@username</a> (for <a>@a username with spaces in it</a> enclose it in square brackets) or a post by its number, like this: <a>#1000</a>.

You can also assign tags to your post like this: <a>#a_tag</a> <a>#another-tag</a> <a>#<code>[</code>a tag with spaces in it<code>]</code></a> but not like #`[69]`: the latter will link the post number 69 and not a numeric tag.

```
You can link directly a @username (for @[a username with spaces in it]
enclose it in square brackets) or a post by its number, like this: #1000. 

You can also assign tags to your post like this: #a_tag #another-tag #[a tag with spaces in it]
but not like #[69]: the latter will link the post number 69 and not a numeric tag.
```

<h2>Sectioning</h2>
You can use up to three different levels of headlines to structure your content.
<h1>Headline Level 1</h1><h2>Headline Level 2</h2><h3>Headline Level 3</h3>


```
****Headline Level 1**** 
***Headline Level 2*** 
**Headline Level 3** 
```


<h2>Images</h2>
You can include images with curly brackets. Optionally you can specify the alt / title of them.

<img src='http://bit.ly/fr0cPF' alt='blabla' title='blabla' />

you can also create a linked image

<a href='http://www.google.com'><img src='http://bit.ly/fr0cPF' alt='blabla' title='blabla' /></a>

```
You can include images with curly brackets. Optionally you can specify the alt / title of them.

[http://bit.ly/fr0cPF blabla]

you can also create a linked image

[http://www.google.com {http://bit.ly/fr0cPF blabla}]
```


<h2>Lists</h2>
A3 supports ordered and unordered lists. To create a list item use a `*` for unordered lists or a # for ordered ones. Those symbols must be at the start of the line and followed by a space.

> <ul>
<blockquote><li>This is a list</li>
<li>The second item</li>
<li>Another item</li></ul></blockquote>

> <ol>
<blockquote><li>The same list but ordered</li>
<li>Another item</li>
<li>That's it</li></ol></blockquote>


```

* This is a list 
* The second item 
* Another item 

# The same list but ordered 
# Another item 
# That's it 

```


<h2>Quoting</h2>

Highlight some text and click on the blue quotes button that will appear. Alternatively you can start a line with > followed by a space and the text you want to quote.

<blockquote>nulla opprime le italiche genti quanto un papa (Radetzky)</blockquote>


```
Highlight some text and click on the blue quotes button that will appear.
Alternatively you can start a line with > followed by a space
and the text you want to quote. 

> nulla opprime le italiche genti quanto un papa (Radetzky) 
```

<h2>No Formatting</h2>
If you need to display text exactly like it is typed (without any formatting), enclose the area with double equal signs.

`This is some text which contains addresses like this: http://www.google.com and *formatting*, but nothing is done with it.`

```
If you need to display text exactly like it is typed (without any formatting), enclose the area with double equal signs.

==This is some text which contains addresses like this: http://www.google.com and *formatting*, but nothing is done with it.==
```


<h2>Embedding HTML</h2>
You can embed raw HTML into your post simply by typing it.

HTML example:
This is some <span>inline HTML</span>
<p>And this is some block HTML</p>

```
This is some <span style="color:red;font-size:150%;">inline HTML</span>
<p style="border:2px dashed red;">And this is some block HTML
```

<h2>Macros</h2>
Macros are a way to quickly build complex formatting codes.

```
Macros are a way to quickly build complex formatting codes.
{%yt:http://www.youtube.com/watch?v=qItugh-fFgg%} 
{%wp:All your base are belong to us%} 
```