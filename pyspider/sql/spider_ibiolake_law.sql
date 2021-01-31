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

 Date: 31/01/2021 21:49:22
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for spider_ibiolake_law
-- ----------------------------
DROP TABLE IF EXISTS `spider_ibiolake_law`;
CREATE TABLE `spider_ibiolake_law` (
  `url` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'url',
  `title` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '标题',
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '内容',
  `pub_date` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '发布日期',
  `source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '来源',
  `click_num` varchar(8) DEFAULT NULL COMMENT '点击次数',
  `category1` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '分类1',
  `category2` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '分类2',
  `crt_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `thumbnail` varchar(255) DEFAULT NULL COMMENT '缩略图',
  PRIMARY KEY (`url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='爬虫-光谷生物城政策法规-http://www.ibiolake.com/';

SET FOREIGN_KEY_CHECKS = 1;
