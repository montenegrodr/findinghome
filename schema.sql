-- MySQL dump 10.13  Distrib 5.7.20, for Linux (x86_64)
--
-- Host: localhost    Database: findinghome
-- ------------------------------------------------------
-- Server version	5.7.20

CREATE SCHEMA `findinghome`;

use `findinghome`;

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `dwelling`
--

DROP TABLE IF EXISTS `dwelling`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dwelling` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `address_line_1` varchar(255) DEFAULT NULL,
  `address_line_2` varchar(255) DEFAULT NULL,
  `area_size` varchar(10) DEFAULT NULL,
  `contact_number` varchar(30) DEFAULT NULL,
  `county` varchar(30) DEFAULT NULL,
  `daft_link` varchar(1024) DEFAULT NULL,
  `dwelling_type` varchar(45) DEFAULT NULL,
  `facilities` tinytext,
  `formalised_address` tinytext,
  `listing_image` varchar(2083) DEFAULT NULL,
  `num_bathrooms` int(11) DEFAULT NULL,
  `num_bedrooms` int(11) DEFAULT NULL,
  `price` varchar(45) DEFAULT NULL,
  `price_change` varchar(45) DEFAULT NULL,
  `price_number` int(11) DEFAULT NULL,
  `price_month` int(11) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  `town` varchar(255) DEFAULT NULL,
  `viewings` varchar(45) DEFAULT NULL,
  `features` varchar(45) DEFAULT NULL,
  `agent` varchar(255) DEFAULT NULL,
  `agent_url` varchar(255) DEFAULT NULL,
  `posted_since` varchar(45) DEFAULT NULL,
  `lat` double DEFAULT NULL,
  `long` double DEFAULT NULL,
  `hash` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `hash_UNIQUE` (`hash`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-03-18 17:04:53
