-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: May 17, 2010 at 08:58 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `a3d`
--

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL auto_increment,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_group_id` (`group_id`),
  KEY `auth_group_permissions_permission_id` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `auth_message`
--

CREATE TABLE `auth_message` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` int(11) NOT NULL,
  `message` longtext NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `auth_message_user_id` (`user_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=77 ;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_content_type_id` (`content_type_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=92 ;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL auto_increment,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `last_login` datetime NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3668 ;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_user_id` (`user_id`),
  KEY `auth_user_groups_group_id` (`group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_user_id` (`user_id`),
  KEY `auth_user_user_permissions_permission_id` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `board_extendedattribute`
--

CREATE TABLE `board_extendedattribute` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(32) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=5 ;

-- --------------------------------------------------------

--
-- Table structure for table `board_extendedattributevalue`
--

CREATE TABLE `board_extendedattributevalue` (
  `id` int(11) NOT NULL auto_increment,
  `key_id` int(11) NOT NULL,
  `value` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `object_id` int(10) unsigned NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `board_extendedattributevalue_key_id` (`key_id`),
  KEY `board_extendedattributevalue_content_type_id` (`content_type_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=26240 ;

-- --------------------------------------------------------

--
-- Table structure for table `board_ignore`
--

CREATE TABLE `board_ignore` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `object_id` int(10) unsigned NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `board_ignore_user_id` (`user_id`),
  KEY `board_ignore_content_type_id` (`content_type_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

-- --------------------------------------------------------

--
-- Table structure for table `board_interaction`
--

CREATE TABLE `board_interaction` (
  `id` int(11) NOT NULL auto_increment,
  `created` datetime NOT NULL,
  `updated` datetime NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `user_id` int(11) NOT NULL,
  `interaction_type_id` int(11) NOT NULL,
  `value` longtext NOT NULL,
  `object_id` int(10) unsigned NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `user_id` (`user_id`,`interaction_type_id`,`object_id`),
  KEY `board_interaction_403f60f` (`user_id`),
  KEY `board_interaction_28a5169f` (`interaction_type_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=6 ;

-- --------------------------------------------------------

--
-- Table structure for table `board_interactiontype`
--

CREATE TABLE `board_interactiontype` (
  `id` int(11) NOT NULL auto_increment,
  `created` datetime NOT NULL,
  `updated` datetime NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `name` varchar(30) NOT NULL,
  `info` longtext NOT NULL,
  `content_type_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `name_2` (`name`,`content_type_id`),
  KEY `board_interactiontype_1bb8f392` (`content_type_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=11 ;

-- --------------------------------------------------------

--
-- Table structure for table `board_mention`
--

CREATE TABLE `board_mention` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` int(11) NOT NULL,
  `post_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `board_mention_403f60f` (`user_id`),
  KEY `board_mention_699ae8ca` (`post_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `board_post`
--

CREATE TABLE `board_post` (
  `id` int(11) NOT NULL auto_increment,
  `created` datetime NOT NULL,
  `updated` datetime NOT NULL,
  `is_active` tinyint(1) NOT NULL default '1',
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) default NULL,
  `object_id` int(10) unsigned default NULL,
  `rating` int(11) NOT NULL,
  `views_count` int(11) NOT NULL,
  `replies_count` int(11) NOT NULL,
  `status` smallint(6) NOT NULL,
  `versions_count` int(11) NOT NULL,
  `ip` char(15) NOT NULL,
  `userdata` varchar(255) NOT NULL,
  `username` varchar(32) NOT NULL,
  `last_poster_id` int(11) default NULL,
  `reverse_timestamp` int(10) unsigned NOT NULL,
  `title` varchar(255) NOT NULL,
  `read_only` tinyint(1) NOT NULL,
  `no_replies` tinyint(1) NOT NULL,
  `template_override_id` int(11) default NULL,
  `_last_reply_id` int(10) unsigned NOT NULL default '0',
  PRIMARY KEY  (`id`),
  KEY `board_post_content_type_id` (`content_type_id`),
  KEY `board_post_last_poster_id` (`last_poster_id`),
  KEY `board_post_template_override_id` (`template_override_id`),
  KEY `object_id` (`object_id`),
  KEY `is_active` (`is_active`,`status`),
  KEY `last_reply` (`reverse_timestamp`,`object_id`,`replies_count`),
  KEY `board_post_user_id` (`user_id`,`updated`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1318640 ;

-- --------------------------------------------------------

--
-- Table structure for table `board_postdata`
--

CREATE TABLE `board_postdata` (
  `post_ptr_id` int(11) NOT NULL,
  `body` longtext NOT NULL,
  `summary` longtext NOT NULL,
  `body_markdown` longtext NOT NULL,
  `signature` longtext NOT NULL,
  `tagset` longtext NOT NULL,
  PRIMARY KEY  (`post_ptr_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `board_shorty`
--

CREATE TABLE `board_shorty` (
  `id` int(11) NOT NULL auto_increment,
  `created` datetime NOT NULL,
  `updated` datetime NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `sender_id` int(11) NOT NULL,
  `body` varchar(255) NOT NULL,
  `receiver_id` int(11) default NULL,
  PRIMARY KEY  (`id`),
  KEY `board_shorty_sender_id` (`sender_id`),
  KEY `board_shorty_receiver_id` (`receiver_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `board_tag`
--

CREATE TABLE `board_tag` (
  `id` int(11) NOT NULL auto_increment,
  `created` datetime NOT NULL,
  `updated` datetime NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `title` varchar(50) NOT NULL,
  `icon` varchar(100) NOT NULL,
  `attach_count` int(10) unsigned NOT NULL,
  `last_object` datetime default NULL,
  `template_id` int(11) default NULL,
  `description` text NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `board_tag_title` (`title`),
  KEY `board_tag_template_id` (`template_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=45 ;

-- --------------------------------------------------------

--
-- Table structure for table `board_tagattach`
--

CREATE TABLE `board_tagattach` (
  `id` int(11) NOT NULL auto_increment,
  `tag_id` int(11) NOT NULL,
  `post_id` int(11) NOT NULL,
  `obj_update` int(10) unsigned NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `tag_id` (`tag_id`,`post_id`),
  KEY `board_tagattach_post_id` (`post_id`),
  KEY `board_tagattach_tag_id` (`tag_id`,`obj_update`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=49523 ;

-- --------------------------------------------------------

--
-- Table structure for table `board_template`
--

CREATE TABLE `board_template` (
  `id` int(11) NOT NULL auto_increment,
  `created` datetime NOT NULL,
  `updated` datetime NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `name` varchar(255) NOT NULL,
  `body` longtext NOT NULL,
  `parent_id` int(11) default NULL,
  PRIMARY KEY  (`id`),
  KEY `parent_id_refs_id_15fd1303` (`parent_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

-- --------------------------------------------------------

--
-- Table structure for table `board_thread`
--

CREATE TABLE `board_thread` (
  `id` int(11) NOT NULL auto_increment,
  `created` datetime NOT NULL,
  `updated` datetime NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `first_post_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `last_poster_id` int(11) NOT NULL,
  `last_reply` datetime NOT NULL,
  `title` varchar(255) NOT NULL,
  `top_lock` tinyint(1) NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `user_id_refs_id_2bc5ba97` (`user_id`),
  KEY `last_poster_id_refs_id_2bc5ba97` (`last_poster_id`),
  KEY `first_post_id_refs_id_73000293` (`first_post_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `board_userprofile`
--

CREATE TABLE `board_userprofile` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` int(11) NOT NULL,
  `hidden_status` tinyint(1) NOT NULL,
  `hidden_email` tinyint(1) NOT NULL,
  `rating_total` int(11) NOT NULL,
  `signature` longtext NOT NULL,
  `secret_question` longtext NOT NULL,
  `secret_answer` longtext NOT NULL,
  `short_desc` varchar(255) NOT NULL,
  `long_desc` longtext NOT NULL,
  `custom_nick_display` longtext NOT NULL,
  `mod_denied` tinyint(1) NOT NULL,
  `auto_login` tinyint(1) NOT NULL,
  `back_to_topic` tinyint(1) NOT NULL,
  `auto_quote` tinyint(1) NOT NULL,
  `link_source_post` tinyint(1) NOT NULL,
  `always_preview` tinyint(1) NOT NULL,
  `can_modify_profile_own` tinyint(1) NOT NULL,
  `can_set_nick_color` tinyint(1) NOT NULL,
  `can_change_short_desc` tinyint(1) NOT NULL,
  `show_ruler` tinyint(1) NOT NULL,
  `save_password` tinyint(1) NOT NULL,
  `contributor` tinyint(1) NOT NULL,
  `is_alias` tinyint(1) NOT NULL,
  `post_per_page` smallint(6) NOT NULL,
  `min_rating` smallint(6) NOT NULL,
  `mana` int(11) NOT NULL,
  `last_post_id` int(11) default NULL,
  `posts_count` int(11) NOT NULL,
  `_last_reply_id` int(10) unsigned NOT NULL default '0',
  PRIMARY KEY  (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `board_userprofile_11738784` (`last_post_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3624 ;

-- --------------------------------------------------------

--
-- Table structure for table `denorm_dirtyinstance`
--

CREATE TABLE `denorm_dirtyinstance` (
  `id` int(11) NOT NULL auto_increment,
  `content_type_id` int(11) NOT NULL,
  `object_id` int(10) unsigned default NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `object_id` (`object_id`,`content_type_id`),
  KEY `denorm_dirtyinstance_content_type_id` (`content_type_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=182 ;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL auto_increment,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) default NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `django_admin_log_user_id` (`user_id`),
  KEY `django_admin_log_content_type_id` (`content_type_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=82 ;

-- --------------------------------------------------------

--
-- Table structure for table `django_comment_flags`
--

CREATE TABLE `django_comment_flags` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` int(11) NOT NULL,
  `comment_id` int(11) NOT NULL,
  `flag` varchar(30) NOT NULL,
  `flag_date` datetime NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `user_id` (`user_id`,`comment_id`,`flag`),
  KEY `django_comment_flags_user_id` (`user_id`),
  KEY `django_comment_flags_comment_id` (`comment_id`),
  KEY `django_comment_flags_flag` (`flag`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=31 ;

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY  (`session_key`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `django_site`
--

CREATE TABLE `django_site` (
  `id` int(11) NOT NULL auto_increment,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

-- --------------------------------------------------------

--
-- Table structure for table `faves_fave`
--

CREATE TABLE `faves_fave` (
  `id` int(11) NOT NULL auto_increment,
  `type_id` int(11) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `object_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `withdrawn` tinyint(1) NOT NULL,
  `date_created` datetime NOT NULL,
  `date_updated` datetime default NULL,
  PRIMARY KEY  (`id`),
  KEY `faves_fave_type_id` (`type_id`),
  KEY `faves_fave_content_type_id` (`content_type_id`),
  KEY `faves_fave_user_id` (`user_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

-- --------------------------------------------------------

--
-- Table structure for table `faves_favetype`
--

CREATE TABLE `faves_favetype` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(255) NOT NULL,
  `slug` varchar(50) NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `faves_favetype_slug` (`slug`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

-- --------------------------------------------------------

--
-- Table structure for table `registration_registrationprofile`
--

CREATE TABLE `registration_registrationprofile` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` int(11) NOT NULL,
  `activation_key` varchar(40) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `user_id` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `temp`
--

CREATE TABLE `temp` (
  `id` int(11) NOT NULL,
  `value` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
