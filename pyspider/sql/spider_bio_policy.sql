/*
 Navicat Premium Data Transfer

 Source Server         : 马鹿113.62.127.198
 Source Server Type    : MySQL
 Source Server Version : 80016
 Source Host           : 113.62.127.198:3306
 Source Schema         : db-biotown-policy

 Target Server Type    : MySQL
 Target Server Version : 80016
 File Encoding         : 65001

 Date: 31/01/2021 21:50:15
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for spider_bio_policy
-- ----------------------------
DROP TABLE IF EXISTS `spider_bio_policy`;
CREATE TABLE `spider_bio_policy` (
  `url` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'url',
  `title` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '标题',
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '内容',
  `pub_dept` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '发布部门',
  `pub_no` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '发文字号',
  `pub_date` varchar(32) DEFAULT NULL COMMENT '发布日期',
  `impl_date` varchar(32) DEFAULT NULL COMMENT '实施日期',
  `force_level` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '效力级别',
  `time_valid` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '时效性',
  `crt_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '爬取时间',
  `local_url` varchar(255) DEFAULT NULL COMMENT '本地文件路径',
  PRIMARY KEY (`url`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='爬虫-政策法规数据-https://db.yaozh.com/';

SET FOREIGN_KEY_CHECKS = 1;
