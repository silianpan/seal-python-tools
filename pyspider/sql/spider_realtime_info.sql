/*
 Navicat Premium Data Transfer

 Source Server         : 马鹿113.62.127.198
 Source Server Type    : MySQL
 Source Server Version : 80016
 Source Host           : 113.62.127.198:3306
 Source Schema         : db-biotown-realtime-info

 Target Server Type    : MySQL
 Target Server Version : 80016
 File Encoding         : 65001

 Date: 31/01/2021 21:50:32
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for spider_realtime_info
-- ----------------------------
DROP TABLE IF EXISTS `spider_realtime_info`;
CREATE TABLE `spider_realtime_info` (
  `url` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT 'url',
  `title` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '标题',
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '内容',
  `pub_date` varchar(32) DEFAULT NULL COMMENT '发布日期',
  `source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '来源',
  `crt_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '爬取时间',
  `local_url` varchar(255) DEFAULT NULL COMMENT '本地存放文件路径',
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `thumbnail` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '缩略图',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=40350 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='爬虫-前沿咨询-https://med.sina.com/';

SET FOREIGN_KEY_CHECKS = 1;
