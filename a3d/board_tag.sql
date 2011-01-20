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
  `reverse_timestamp` int(11) unsigned NOT NULL default '0',
  `template_id` int(11) default NULL,
  `description` text NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `board_tag_title` (`title`),
  KEY `board_tag_template_id` (`template_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=47 ;

--
-- Dumping data for table `board_tag`
--

INSERT INTO `board_tag` (`id`, `created`, `updated`, `is_active`, `title`, `icon`, `attach_count`, `reverse_timestamp`, `template_id`, `description`) VALUES
(1, '2010-03-27 18:24:45', '2010-03-30 13:12:07', 1, 'news', '', 0, 2010, NULL, ''),
(2, '2010-03-27 18:24:45', '2010-03-31 14:39:56', 1, 'user', '', 0, 2010, NULL, 'Gente che ha deciso di asphaltarsi. A volte c''è da chiedersi il perché. Più spesso, però, forse è meglio non farlo.'),
(3, '2010-03-27 18:24:45', '2010-06-11 17:17:01', 1, 'bla-bla', '', 0, 2010, NULL, 'Bla bla bla bla.'),
(4, '2010-03-27 18:24:45', '2010-06-20 14:46:32', 1, 'recensioni', '', 1, 2010, NULL, 'Hai visto un film, letto un libro, provato un nuovo dildo e ci vuoi raccontare le tue impressioni? Fallo pure, ma ricordati di pulire quando hai finito.'),
(5, '2010-03-27 18:24:45', '2010-03-30 13:12:07', 1, 'immagini', '', 0, 2010, NULL, 'Posta qui le tue foto. Le tette sono bene accette.Le foto prese da rotten, invece, hanno un po'' rotto il cazzo.'),
(6, '2010-03-27 18:24:45', '2010-03-30 13:12:07', 1, 'musica', '', 0, 2010, NULL, 'Abbastanza ovvio, no?'),
(7, '2010-03-27 18:24:45', '2010-03-30 13:12:07', 1, 'copula', '', 0, 2010, NULL, 'Una volta si poteva votare, poi mi sono rotto la minchia.'),
(8, '2010-03-27 18:24:45', '2010-03-30 13:12:07', 1, 'deliri', '', 0, 2010, NULL, 'Scrittura creativa e farneticazioni varie. Se possibile, evita lagne sul fidanzato che ti ha appena mollato - a meno che tu non stia cercando di trombare, ovviamente.'),
(9, '2010-03-27 18:24:45', '2010-03-30 13:12:07', 1, 'referrers', '', 0, 2010, NULL, 'Le stringhe di ricerca con cui la gente arriva sull''asphalto. Non per cuori puri e stomaci deboli.'),
(10, '2010-03-27 18:24:45', '2010-03-30 13:12:07', 1, 'links', '', 0, 2010, NULL, 'Link a siti interessanti. Dove per "interessanti" si intende "non blogs".'),
(11, '2010-03-27 18:24:45', '2010-03-30 13:12:07', 1, 'bug_report', '', 0, 2010, NULL, 'Segnalate tutto quello che non va. Nell''asphalto, non nella vostra patetica e inutile vita, ovviamente.'),
(12, '2010-03-27 18:24:45', '2010-04-07 12:40:15', 1, 'anon', '', 0, 2010, 1, 'Anonimato totale.'),
(13, '2010-03-27 18:24:45', '2010-03-30 13:12:07', 1, 'wiki', '', 0, 2010, NULL, 'Letteratura collettiva. Puoi scrivere e editare tutto. Chi ne abusa, però, verrà severamente punito (<i>hint: <u>c''entra</u> Yussuf</i>)'),
(14, '2010-03-27 18:24:45', '2010-03-30 13:12:07', 1, 'csr', '', 0, 2010, NULL, 'Annunci di konzertue (un plurale irregolare) e altre cose csr-related.'),
(15, '2010-03-27 18:24:45', '2010-03-30 13:12:07', 1, 'mercanzia', '', 0, 2010, NULL, 'Potete essere al top dell''eleganza e darmi soldi contemporaneamente. Se non è moderno multitasking questo, non so che cazzo volete di più.'),
(16, '2010-03-27 18:24:45', '2010-03-30 13:12:07', 1, 'gaming', '', 0, 2010, NULL, 'Che cazzo di comunità moderna sarebbe senza una sezione sui videogggggiochi, eh? Ai ggiovani ci piacciono, e quindi ci vogliono.'),
(17, '2010-03-27 18:24:45', '2010-03-30 13:12:07', 1, 'telefilm', '', 0, 2010, NULL, 'Massì, apriamo pure una categoria per i telefilm.'),
(18, '2010-03-27 18:24:45', '2010-03-30 13:12:07', 1, 'a3', '', 0, 2010, NULL, ''),
(19, '2010-03-27 18:24:45', '2010-03-30 13:12:07', 1, 'add-me', '', 0, 2010, NULL, ''),
(20, '2010-03-27 18:24:45', '2010-06-11 17:49:02', 1, 'richiesta', '', 0, 2010, NULL, ''),
(21, '2010-03-27 18:24:45', '2010-03-31 16:25:06', 1, 'blog', '', 0, 2010, NULL, ''),
(22, '2010-03-27 18:24:45', '2010-04-15 11:13:59', 1, 'rotten', 'tag/subcat-rotten_1.gif', 0, 2010, NULL, ''),
(23, '2010-03-27 18:24:45', '2010-06-22 15:02:12', 1, 'tette', '', 0, 2010, NULL, ''),
(24, '2010-03-27 18:24:45', '2010-06-26 11:45:11', 1, 'porno', '', 0, 3017426680, NULL, ''),
(25, '2010-03-27 18:24:45', '2010-03-30 13:12:07', 1, 'link', '', 0, 2010, NULL, ''),
(26, '2010-03-27 18:24:45', '2010-06-12 17:44:59', 1, 'tech', '', 0, 2010, NULL, ''),
(27, '2010-03-27 18:24:45', '2010-03-30 13:12:07', 1, 'meta', '', 0, 2010, NULL, ''),
(28, '2010-03-27 18:24:45', '2010-03-30 13:12:07', 1, 'obs', '', 0, 2010, NULL, ''),
(29, '2010-03-27 18:24:45', '2010-03-30 13:12:07', 1, 'flame', '', 0, 2010, NULL, ''),
(30, '2010-03-27 18:24:45', '2010-03-30 13:12:07', 1, 'bug', '', 0, 2010, NULL, ''),
(31, '2010-03-27 18:24:45', '2010-03-30 13:12:07', 1, 'cut-n-paste', '', 0, 2010, NULL, ''),
(32, '2010-03-27 18:24:45', '2010-03-30 13:12:07', 1, 'politica', '', 0, 2010, NULL, ''),
(33, '2010-03-27 18:24:45', '2010-03-30 13:12:07', 1, 'sport', '', 0, 2010, NULL, ''),
(34, '2010-03-27 18:24:45', '2010-03-30 13:12:07', 1, 'importante', '', 0, 2010, NULL, ''),
(35, '2010-03-27 18:24:45', '2010-03-30 13:12:07', 1, 'rido', '', 0, 2010, NULL, ''),
(36, '2010-03-27 18:24:45', '2010-03-30 13:12:07', 1, 'tedio', '', 0, 2010, NULL, ''),
(37, '2010-03-27 18:24:45', '2010-03-30 13:12:07', 1, 'media', '', 0, 2010, NULL, ''),
(38, '2010-03-27 18:24:45', '2010-03-28 10:45:27', 1, 'presto', '', 0, 2010, NULL, ''),
(39, '2010-03-27 18:24:45', '2010-03-30 13:12:07', 1, 'chat', '', 0, 2010, NULL, ''),
(40, '2010-03-27 18:24:45', '2010-03-30 13:12:07', 1, 'scienza', '', 0, 2010, NULL, ''),
(41, '2010-03-27 18:24:45', '2010-03-30 13:12:07', 1, 'meet', '', 0, 2010, NULL, ''),
(43, '2010-03-27 18:24:45', '2010-03-30 13:12:07', 1, 'attwhore', '', 0, 2010, NULL, ''),
(45, '2010-06-12 17:32:23', '2010-06-12 17:44:45', 1, 'mitico', '', 0, 0, NULL, ''),
(46, '2010-06-16 17:51:11', '2010-06-16 17:51:11', 1, 'subito', '', 0, 0, NULL, '');
