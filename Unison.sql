DROP DATABASE IF EXISTS `unison`;
CREATE DATABASE IF NOT EXISTS `unison`;
USE `unison`;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
-- On research I found repeated references to the fact that first/last isn't ideal
--   `firstName` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
--   `lastName` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `username` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `mobile` varchar(15) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `passwordHash` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `registeredAt` datetime NOT NULL,
  `lastLogin` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_username` (`username`),
  UNIQUE KEY `uq_mobile` (`mobile`),
  UNIQUE KEY `uq_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Table structure for table `user_post`
--

DROP TABLE IF EXISTS `user_post`;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `user_post` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `userId` bigint NOT NULL,
  `senderId` bigint DEFAULT NULL,
  `message` tinytext COLLATE utf8mb4_unicode_ci NOT NULL,
  `attachment` blob NOT NULL,
  `createdAt` datetime NOT NULL,
  `updatedAt` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_upost_user` (`userId`),
  KEY `idx_upost_sender` (`senderId`),
  CONSTRAINT `fk_upost_sender` FOREIGN KEY (`senderId`) REFERENCES `user` (`id`),
  CONSTRAINT `fk_upost_user` FOREIGN KEY (`userId`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Table structure for table `user_endorsements`
--

DROP TABLE IF EXISTS `user_endorsements`;
CREATE TABLE `user_endorsements` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `sourceId` bigint NOT NULL,
  `targetId` bigint NOT NULL,
--  Do we want a type of endorsement, or simply that the user has been endorsed?
--  `type` smallint(6) NOT NULL DEFAULT '0',
  `endorsement_post` bigint NOT NULL,
  `createdAt` datetime NOT NULL,
  `updatedAt` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_ufollower` (`sourceId`,`targetId`,`endorsement_post`),
  KEY `idx_ufollower_source` (`sourceId`),
  KEY `idx_ufollower_target` (`targetId`),
  CONSTRAINT `fk_uendorse_source` FOREIGN KEY (`sourceId`) REFERENCES `user` (`id`),
  CONSTRAINT `fk_uendorse_target` FOREIGN KEY (`targetId`) REFERENCES `user` (`id`),
  CONSTRAINT `fk_uendorse_post` FOREIGN KEY (`endorsement_post`) REFERENCES `user_post` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Table structure for table `skills`
--

DROP TABLE IF EXISTS `skills`;
CREATE TABLE `skills` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `userId` bigint NOT NULL,
  `skillName` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `endorsed` boolean NOT NULL,
  `endorsedBy` bigint DEFAULT NULL,
  `createdAt` datetime NOT NULL,
  `updatedAt` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_suser_id` FOREIGN KEY (`userId`) REFERENCES `user` (`id`),
  CONSTRAINT `fk_endorsing_user` FOREIGN KEY (`endorsedBy`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Table structure for table `profile`
--

DROP TABLE IF EXISTS `profile`;
CREATE TABLE `profile` (
  `userId` bigint NOT NULL,
  `fullName` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `preferredName` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `badges` smallint NOT NULL DEFAULT '0',
  `skills` smallint NOT NULL DEFAULT '0',
  `createdAt` datetime NOT NULL,
  `updatedAt` datetime DEFAULT NULL,
  `profileBody` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`userId`),
  CONSTRAINT `fk_puser_id` FOREIGN KEY (`userId`) REFERENCES `user` (`id`)
-- Had thought to make badges and skills arrays that reference the id's in a seperate table, 
-- but that seems like it wouldn't be an easy design to implement and maintain
--   CONSTRAINT `fk_skills` FOREIGN KEY (`skills`) REFERENCES `skills` (`id`)
--   CONSTRAINT `fk_badges` FOREIGN KEY (`badges`) REFERENCES `badges` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Table structure for table `notifications`
--

DROP TABLE IF EXISTS `notifications`;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `notifications` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `notifiedUserId` bigint NOT NULL,
  `message` tinytext COLLATE utf8mb4_unicode_ci NOT NULL,
  `createdAt` datetime NOT NULL,
  `acknowledgedAt` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_notified_user` FOREIGN KEY (`notifiedUserId`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;