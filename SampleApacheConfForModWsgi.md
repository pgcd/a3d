# Introduction #

My apache config is as follow; I'm assuming `mod_wsgi` is enabled, and there's an entry in `/etc/hosts` to have `a3d` point to 127.0.0.1


```
<VirtualHost *:80>
    Alias /media/ /home/pgcd/workspace/django-svn/django/contrib/admin/media/
    Alias /a3dmedia/ /home/pgcd/workspace/a3d/media/
    ServerName a3d
    <Directory /home/pgcd/workspace/a3d/apache/>
        Order allow,deny
        Allow from all
    </Directory>
    <Directory /home/pgcd/workspace/a3d/media/>
        Order allow,deny
        Allow from all
    </Directory>
    <Directory /home/pgcd/workspace/django-svn/django/contrib/admin/media/>
        Order allow,deny
        Allow from all
    </Directory>

    WSGIScriptAlias / /home/pgcd/workspace/a3d/apache/django.wsgi
    DocumentRoot /var/www/
</VirtualHost>

```