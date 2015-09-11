-- MySQL dump 10.13  Distrib 5.1.73, for redhat-linux-gnu (x86_64)
--
-- Host: localhost    Database: report
-- ------------------------------------------------------
-- Server version	5.1.73-log

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
-- Temporary table structure for view `Usuario_ativos`
--

DROP TABLE IF EXISTS `Usuario_ativos`;
/*!50001 DROP VIEW IF EXISTS `Usuario_ativos`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `Usuario_ativos` (
 `tuid` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `acct_auth`
--

DROP TABLE IF EXISTS `acct_auth`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `acct_auth` (
  `user_name` char(45) NOT NULL,
  `user_passwd` char(20) NOT NULL,
  `user_descr` varchar(100) NOT NULL,
  PRIMARY KEY (`user_name`),
  UNIQUE KEY `user_name_UNIQUE` (`user_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `acct_cmd`
--

DROP TABLE IF EXISTS `acct_cmd`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `acct_cmd` (
  `host` varchar(15) NOT NULL,
  `comando` varchar(255) NOT NULL,
  `uid` int(10) NOT NULL,
  `time_effect` decimal(12,2) NOT NULL,
  `time_user` decimal(12,2) DEFAULT NULL,
  `time_system` decimal(12,2) DEFAULT NULL,
  `data_pross` date NOT NULL,
  PRIMARY KEY (`host`,`comando`,`uid`,`time_effect`,`data_pross`),
  KEY `acct_cmd_idx` (`host`,`comando`,`uid`,`data_pross`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `acct_uid`
--

DROP TABLE IF EXISTS `acct_uid`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `acct_uid` (
  `host` varchar(15) NOT NULL,
  `uid` int(11) NOT NULL,
  `time_effect` decimal(12,2) NOT NULL,
  `time_user` decimal(12,2) DEFAULT NULL,
  `time_system` decimal(12,2) DEFAULT NULL,
  `data_pross` date NOT NULL,
  PRIMARY KEY (`host`,`uid`,`time_effect`,`data_pross`),
  KEY `acct_uid_idx` (`host`,`uid`,`data_pross`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `host_desc`
--

DROP TABLE IF EXISTS `host_desc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `host_desc` (
  `host` varchar(15) NOT NULL,
  `descricao` varchar(200) DEFAULT NULL,
  `usuario` varchar(45) DEFAULT NULL,
  `ativo` binary(1) DEFAULT '0',
  `data_insc` datetime DEFAULT NULL,
  PRIMARY KEY (`host`),
  UNIQUE KEY `host_UNIQUE` (`host`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `uid` int(11) NOT NULL,
  `gid` int(11) DEFAULT '0',
  `username` varchar(45) DEFAULT NULL,
  `groupname` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Base de uid e gid como no ldap.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Final view structure for view `Usuario_ativos`
--

/*!50001 DROP TABLE IF EXISTS `Usuario_ativos`*/;
/*!50001 DROP VIEW IF EXISTS `Usuario_ativos`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = latin1 */;
/*!50001 SET character_set_results     = latin1 */;
/*!50001 SET collation_connection      = latin1_swedish_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `Usuario_ativos` AS (select `acct_uid`.`uid` AS `tuid` from (`acct_uid` join `users`) group by `acct_uid`.`uid`) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-07-09 13:01:42
