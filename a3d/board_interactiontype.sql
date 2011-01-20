-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jul 06, 2010 at 02:29 PM
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
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=12 ;

--
-- Dumping data for table `board_interactiontype`
--

INSERT INTO `board_interactiontype` (`id`, `created`, `updated`, `is_active`, `name`, `info`, `content_type_id`) VALUES
(1, '2010-05-03 09:34:53', '2010-05-03 09:34:53', 1, 'create', '', 10),
(2, '2010-05-03 09:36:46', '2010-05-03 09:36:46', 1, 'update', '', 10),
(3, '2010-05-03 09:37:23', '2010-05-03 09:37:23', 1, 'read', '', 10),
(4, '2010-05-03 09:37:33', '2010-05-03 09:37:33', 1, 'delete', '', 10),
(5, '2010-05-03 09:37:48', '2010-05-03 09:37:48', 1, 'rate', '', 10),
(6, '2010-05-03 09:38:03', '2010-05-03 09:38:03', 1, 'timeshift', '', 10),
(7, '2010-05-03 09:38:31', '2010-05-03 09:38:31', 1, 'flag', '', 10),
(8, '2010-05-13 18:44:14', '2010-05-13 18:44:14', 1, 'read', '', 12),
(9, '2010-05-13 18:44:34', '2010-05-13 18:44:34', 1, 'read', '', 11),
(10, '2010-05-03 09:34:53', '2010-05-03 09:34:53', 1, 'replied', '', 10),
(11, '2010-05-03 09:37:23', '2010-05-03 09:37:23', 1, 'read', 'Read post by user.', 3);
