# Introduction #

You need to have:
  * Django, of course - I'm mostly tracking SVN, so that'd be a reasonable choice. Ubuntu's distro is also fine. Please note this also means I'm using Python 2.6 - we'll jump to 3 when Django does. Furthermore, this kinda implies running Apache and MySQL, but you can probably make do with other server software as long as Django runs.

  * Several python packages, starting with `setuptools` and `python-mysqldb`, and the following:
```
  sudo easy_install south
  sudo easy_install django-profiles
  sudo easy_install django-registration
  sudo easy_install django-debug-toolbar
  sudo easy_install django-sphinx
  sudo easy_install django-piston
  sudo easy_install feedparser
  sudo easy_install template-utils
  sudo easy_install django_extensions
```
I'm not entirely sure they will all be required but so far I'm using them, so there.

**IMPORTANT:** Make sure feedparser is v5.0 - v4.1 won't work with googlecode feed.


  * An IDE - Eclipse/Aptana/PyDEV is a sensible choice (mine) but not necessarily the only one.

  * Mercurial (although SVN can still be used to checkout)