/*
 Navicat Premium Data Transfer

 Source Server         : 马鹿113.62.127.198
 Source Server Type    : MySQL
 Source Server Version : 80016
 Source Host           : 113.62.127.198:3306
 Source Schema         : db-biotown-others

 Target Server Type    : MySQL
 Target Server Version : 80016
 File Encoding         : 65001

 Date: 02/02/2021 15:28:47
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for spider_bio_ibiolake
-- ----------------------------
DROP TABLE IF EXISTS `spider_bio_ibiolake`;
CREATE TABLE `spider_bio_ibiolake` (
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '标题',
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '内容',
  `others` json DEFAULT NULL COMMENT '文章地址',
  `json_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '本地json路径',
  `classify_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '分类名称',
  `classify` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '分类',
  `crt_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '爬取时间',
  `url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '爬取url',
  `pub_date` date DEFAULT NULL COMMENT '发布时间',
  `id` varchar(64) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `url` (`url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='光谷生物城政策法规';

SET FOREIGN_KEY_CHECKS = 1;
