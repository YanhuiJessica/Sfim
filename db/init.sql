
-- Dumping database structure for sfim
DROP DATABASE IF EXISTS `sfim`;
CREATE DATABASE `sfim` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */;
USE `sfim`;

-- Dumping structure for table sfim.users
CREATE TABLE `users` (
  `usrid` int(11) NOT NULL AUTO_INCREMENT,
  `usrname` varchar(255) NOT NULL DEFAULT '',
  `hashword` varchar(255) NOT NULL DEFAULT '',
  `mail` varchar(255) NOT NULL DEFAULT '',
  `token` varchar(50) NOT NULL DEFAULT '',
  `authcode` varchar(50) NOT NULL DEFAULT '',
  `verification_status` tinyint(1) NOT NULL DEFAULT '0',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '用户创建时间',
  `generate_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '链接生成时间',
  `pubkey` varbinary(255) NOT NULL DEFAULT '',
  `privkey` varbinary(1023) NOT NULL DEFAULT '',
  `symkey` varbinary(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`usrid`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping structure for table sfim.online_users
CREATE TABLE `online_users` (
  `usrid` int(11) NOT NULL AUTO_INCREMENT,
  `token` varchar(50) NOT NULL DEFAULT '',
  `last_used` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `Pk` varbinary(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`usrid`),
  CONSTRAINT `usrid` FOREIGN KEY (`usrid`) REFERENCES `users` (`usrid`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping structure for table sfim.files
CREATE TABLE `files` (
  `fileid` int(11) NOT NULL AUTO_INCREMENT,
  `filename` varchar(255) DEFAULT NULL,
  `size` varchar(255) NOT NULL DEFAULT '',
  `sha256` varchar(255) NOT NULL DEFAULT '',
  `uid` int(11) NOT NULL DEFAULT '0',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`fileid`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;