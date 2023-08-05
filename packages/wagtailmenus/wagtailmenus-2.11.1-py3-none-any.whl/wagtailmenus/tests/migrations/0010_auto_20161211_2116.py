# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-11 21:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtailmenus.models.menuitems
import wagtailmenus.models.menus


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailmenus', '0020_auto_20161210_0004'),
        ('tests', '0009_typicalpage'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomFlatMenu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='For internal reference only.', max_length=255, verbose_name='title')),
                ('handle', models.SlugField(help_text='Used to reference this menu in templates etc. Must be unique for the selected site.', max_length=100, verbose_name='handle')),
                ('heading', models.CharField(blank=True, help_text='If supplied, appears above the menu when rendered.', max_length=255, verbose_name='heading')),
                ('max_levels', models.PositiveSmallIntegerField(choices=[(1, '1: No sub-navigation (flat)'), (2, '2: Allow 1 level of sub-navigation'), (3, '3: Allow 2 levels of sub-navigation'), (4, '4: Allow 3 levels of sub-navigation')], default=1, help_text='The maximum number of levels to display when rendering this menu. The value can be overidden by supplying a different <code>max_levels</code> value to the <code>{% flat_menu %}</code> tag in your templates.', verbose_name='maximum levels')),
                ('use_specific', models.PositiveSmallIntegerField(choices=[(0, 'Off (most efficient)'), (1, 'Auto'), (2, 'Top level'), (3, 'Always (least efficient)')], default=1, help_text="Controls how 'specific' pages objects are fetched and used when rendering this menu. This value can be overidden by supplying a different <code>use_specific</code> value to the <code>{% flat_menu %}</code> tag in your templates.", verbose_name='specific page usage')),
                ('heading_de', models.CharField(blank=True, max_length=255, verbose_name='heading (de)')),
                ('heading_fr', models.CharField(blank=True, max_length=255, verbose_name='heading (fr)')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailcore.Site', verbose_name='site')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'flat menu',
                'verbose_name_plural': 'flat menus',
            },
            bases=(models.Model, wagtailmenus.models.menus.Menu),
        ),
        migrations.CreateModel(
            name='CustomFlatMenuItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('link_url', models.CharField(blank=True, max_length=255, null=True, verbose_name='link to a custom URL')),
                ('link_text', models.CharField(blank=True, help_text="Provide the text to use for a custom URL, or set on an internal page link to use instead of the page's title.", max_length=255, verbose_name='link text')),
                ('handle', models.CharField(blank=True, help_text='Use this field to optionally specify an additional value for each menu item, which you can then reference in custom menu templates.', max_length=100, verbose_name='handle')),
                ('url_append', models.CharField(blank=True, help_text="Use this to optionally append a #hash or querystring to the above page's URL.", max_length=255, verbose_name='append to URL')),
                ('allow_subnav', models.BooleanField(default=False, help_text="NOTE: The sub-menu might not be displayed, even if checked. It depends on how the menu is used in this project's templates.", verbose_name='allow sub-menu for this item')),
                ('link_text_de', models.CharField(blank=True, max_length=255, verbose_name='link text (de)')),
                ('link_text_fr', models.CharField(blank=True, max_length=255, verbose_name='link text (fr)')),
                ('link_page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.Page', verbose_name='link to an internal page')),
                ('menu', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu_items', to='tests.CustomFlatMenu')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, wagtailmenus.models.menuitems.MenuItem),
        ),
        migrations.CreateModel(
            name='CustomMainMenu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_levels', models.PositiveSmallIntegerField(choices=[(1, '1: No sub-navigation (flat)'), (2, '2: Allow 1 level of sub-navigation'), (3, '3: Allow 2 levels of sub-navigation'), (4, '4: Allow 3 levels of sub-navigation')], default=2, help_text='The maximum number of levels to display when rendering this menu. The value can be overidden by supplying a different <code>max_levels</code> value to the <code>{% main_menu %}</code> tag in your templates.', verbose_name='maximum levels')),
                ('use_specific', models.PositiveSmallIntegerField(choices=[(0, 'Off (most efficient)'), (1, 'Auto'), (2, 'Top level'), (3, 'Always (least efficient)')], default=1, help_text="Controls how 'specific' pages objects are fetched and used when rendering this menu. This value can be overidden by supplying a different <code>use_specific</code> value to the <code>{% main_menu %}</code> tag in your templates.", verbose_name='specific page usage')),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailcore.Site', verbose_name='site')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'main menu',
                'verbose_name_plural': 'main menu',
            },
            bases=(models.Model, wagtailmenus.models.menus.Menu),
        ),
        migrations.CreateModel(
            name='CustomMainMenuItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('link_url', models.CharField(blank=True, max_length=255, null=True, verbose_name='link to a custom URL')),
                ('link_text', models.CharField(blank=True, help_text="Provide the text to use for a custom URL, or set on an internal page link to use instead of the page's title.", max_length=255, verbose_name='link text')),
                ('handle', models.CharField(blank=True, help_text='Use this field to optionally specify an additional value for each menu item, which you can then reference in custom menu templates.', max_length=100, verbose_name='handle')),
                ('url_append', models.CharField(blank=True, help_text="Use this to optionally append a #hash or querystring to the above page's URL.", max_length=255, verbose_name='append to URL')),
                ('allow_subnav', models.BooleanField(default=True, help_text="NOTE: The sub-menu might not be displayed, even if checked. It depends on how the menu is used in this project's templates.", verbose_name='allow sub-menu for this item')),
                ('link_text_de', models.CharField(blank=True, max_length=255, verbose_name='link text (de)')),
                ('link_text_fr', models.CharField(blank=True, max_length=255, verbose_name='link text (fr)')),
                ('link_page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.Page', verbose_name='link to an internal page')),
                ('menu', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu_items', to='tests.CustomMainMenu')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, wagtailmenus.models.menuitems.MenuItem),
        ),
        migrations.CreateModel(
            name='FlatMenuCustomMenuItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('link_url', models.CharField(blank=True, max_length=255, null=True, verbose_name='link to a custom URL')),
                ('link_text', models.CharField(blank=True, help_text="Provide the text to use for a custom URL, or set on an internal page link to use instead of the page's title.", max_length=255, verbose_name='link text')),
                ('handle', models.CharField(blank=True, help_text='Use this field to optionally specify an additional value for each menu item, which you can then reference in custom menu templates.', max_length=100, verbose_name='handle')),
                ('url_append', models.CharField(blank=True, help_text="Use this to optionally append a #hash or querystring to the above page's URL.", max_length=255, verbose_name='append to URL')),
                ('allow_subnav', models.BooleanField(default=False, help_text="NOTE: The sub-menu might not be displayed, even if checked. It depends on how the menu is used in this project's templates.", verbose_name='allow sub-menu for this item')),
                ('link_text_de', models.CharField(blank=True, max_length=255, verbose_name='link text (de)')),
                ('link_text_fr', models.CharField(blank=True, max_length=255, verbose_name='link text (fr)')),
                ('link_page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.Page', verbose_name='link to an internal page')),
                ('menu', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='custom_menu_items', to='wagtailmenus.FlatMenu')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, wagtailmenus.models.menuitems.MenuItem),
        ),
        migrations.CreateModel(
            name='MainMenuCustomMenuItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('link_url', models.CharField(blank=True, max_length=255, null=True, verbose_name='link to a custom URL')),
                ('link_text', models.CharField(blank=True, help_text="Provide the text to use for a custom URL, or set on an internal page link to use instead of the page's title.", max_length=255, verbose_name='link text')),
                ('handle', models.CharField(blank=True, help_text='Use this field to optionally specify an additional value for each menu item, which you can then reference in custom menu templates.', max_length=100, verbose_name='handle')),
                ('url_append', models.CharField(blank=True, help_text="Use this to optionally append a #hash or querystring to the above page's URL.", max_length=255, verbose_name='append to URL')),
                ('allow_subnav', models.BooleanField(default=True, help_text="NOTE: The sub-menu might not be displayed, even if checked. It depends on how the menu is used in this project's templates.", verbose_name='allow sub-menu for this item')),
                ('link_text_de', models.CharField(blank=True, max_length=255, verbose_name='link text (de)')),
                ('link_text_fr', models.CharField(blank=True, max_length=255, verbose_name='link text (fr)')),
                ('link_page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.Page', verbose_name='link to an internal page')),
                ('menu', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='custom_menu_items', to='wagtailmenus.MainMenu')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, wagtailmenus.models.menuitems.MenuItem),
        ),
        migrations.AddField(
            model_name='toplevelpage',
            name='repeated_item_text_de',
            field=models.CharField(blank=True, max_length=255, verbose_name='repeated item link text (de)'),
        ),
        migrations.AddField(
            model_name='toplevelpage',
            name='repeated_item_text_fr',
            field=models.CharField(blank=True, max_length=255, verbose_name='repeated item link text (fr)'),
        ),
        migrations.AddField(
            model_name='toplevelpage',
            name='title_de',
            field=models.CharField(blank=True, max_length=255, verbose_name='title (de)'),
        ),
        migrations.AddField(
            model_name='toplevelpage',
            name='title_fr',
            field=models.CharField(blank=True, max_length=255, verbose_name='title (fr)'),
        ),
        migrations.AlterUniqueTogether(
            name='customflatmenu',
            unique_together=set([('site', 'handle')]),
        ),
    ]
