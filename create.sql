SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for positions
-- ----------------------------
DROP TABLE IF EXISTS `positions`;
CREATE TABLE `positions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `keywords` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `spiderUrl` varchar(1000) COLLATE utf8mb4_bin DEFAULT NULL,
  `jobId` varchar(255) COLLATE utf8mb4_bin NOT NULL,
  `jobTitle` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `jobType` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `jobUrl` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `salary` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `position` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `qualification` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `description` longtext COLLATE utf8mb4_bin,
  `industry` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `jobFunction` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `companyName` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `employmentType` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `companyUrl` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `companyAddress` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `seniorityLevel` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `pubTime` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `createdTime` datetime DEFAULT NULL,
  `updatedTime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `jobId` (`jobId`) USING HASH
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

SET FOREIGN_KEY_CHECKS = 1;


SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for title
-- ----------------------------
DROP TABLE IF EXISTS `title`;
CREATE TABLE `title` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `updateTime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;