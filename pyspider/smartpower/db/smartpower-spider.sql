/*
 Navicat Premium Data Transfer

 Source Server         : smartpower-8.137.8.225
 Source Server Type    : MySQL
 Source Server Version : 50741
 Source Host           : 8.137.8.225:33306
 Source Schema         : smartpower-spider

 Target Server Type    : MySQL
 Target Server Version : 50741
 File Encoding         : 65001

 Date: 06/07/2024 14:28:41
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for bjx_hy
-- ----------------------------
DROP TABLE IF EXISTS `bjx_hy`;
CREATE TABLE `bjx_hy` (
  `id` varchar(255) NOT NULL COMMENT 'ID',
  `title` varchar(255) DEFAULT NULL COMMENT '标题',
  `classify` varchar(255) DEFAULT NULL COMMENT '类型',
  `classify_name` varchar(255) DEFAULT NULL COMMENT '类型名称',
  `industry` varchar(255) DEFAULT NULL COMMENT '行业',
  `pub_date` varchar(255) DEFAULT NULL COMMENT '发布日期',
  `url` varchar(255) NOT NULL COMMENT 'url',
  `content` longtext COMMENT '文本内容',
  `json` longtext NOT NULL COMMENT 'json内容base64',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='北极星-行业';

-- ----------------------------
-- Table structure for bjx_zx
-- ----------------------------
DROP TABLE IF EXISTS `bjx_zx`;
CREATE TABLE `bjx_zx` (
  `id` varchar(255) NOT NULL COMMENT 'ID',
  `title` varchar(255) DEFAULT NULL COMMENT '标题',
  `classify` varchar(255) DEFAULT NULL COMMENT '类型',
  `classify_name` varchar(255) DEFAULT NULL COMMENT '类型名称',
  `pub_date` varchar(255) DEFAULT NULL COMMENT '发布日期',
  `url` varchar(255) NOT NULL COMMENT 'url',
  `content` longtext COMMENT '文本内容',
  `json` longtext NOT NULL COMMENT 'json内容base64',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='北极星-资讯';

-- ----------------------------
-- Table structure for dlzstp_dzw_sx
-- ----------------------------
DROP TABLE IF EXISTS `dlzstp_dzw_sx`;
CREATE TABLE `dlzstp_dzw_sx` (
  `id` varchar(255) NOT NULL COMMENT 'ID',
  `title` varchar(255) DEFAULT NULL COMMENT '标题',
  `classify` varchar(255) DEFAULT NULL COMMENT '类型',
  `classify_name` varchar(255) DEFAULT NULL COMMENT '类型名称',
  `industry` varchar(255) DEFAULT NULL COMMENT '行业',
  `pub_date` varchar(255) DEFAULT NULL COMMENT '发布日期',
  `media_name` varchar(255) DEFAULT NULL COMMENT '媒体名称',
  `url` varchar(255) NOT NULL COMMENT 'url',
  `content` longtext COMMENT '文本内容',
  `json` longtext NOT NULL COMMENT 'json内容base64',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='电力知识图谱-电知网-时讯';

-- ----------------------------
-- Table structure for dlzstp_dzw_wj
-- ----------------------------
DROP TABLE IF EXISTS `dlzstp_dzw_wj`;
CREATE TABLE `dlzstp_dzw_wj` (
  `id` varchar(255) NOT NULL COMMENT 'ID',
  `title` varchar(255) DEFAULT NULL COMMENT '标题',
  `first` varchar(255) DEFAULT NULL COMMENT '一级分类',
  `pub_date` varchar(255) DEFAULT NULL COMMENT '发布日期',
  `url` varchar(255) DEFAULT NULL COMMENT 'url',
  `content` longtext COMMENT '文本内容',
  `json` longtext NOT NULL COMMENT 'json内容base64',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='电力知识图谱-电知网-文件';

-- ----------------------------
-- Table structure for dlzstp_dzw_zs
-- ----------------------------
DROP TABLE IF EXISTS `dlzstp_dzw_zs`;
CREATE TABLE `dlzstp_dzw_zs` (
  `id` varchar(255) NOT NULL COMMENT 'ID',
  `title` varchar(255) DEFAULT NULL COMMENT '标题',
  `classify` varchar(255) DEFAULT NULL COMMENT '类型',
  `classify_name` varchar(255) DEFAULT NULL COMMENT '类型名称',
  `industry` varchar(255) DEFAULT NULL COMMENT '行业',
  `pub_date` varchar(255) DEFAULT NULL COMMENT '发布日期',
  `url` varchar(255) NOT NULL COMMENT 'url',
  `content` longtext COMMENT '文本内容',
  `json` longtext NOT NULL COMMENT 'json内容base64',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='电力知识图谱-电知网-知识';

-- ----------------------------
-- Table structure for scdl_jyzx
-- ----------------------------
DROP TABLE IF EXISTS `scdl_jyzx`;
CREATE TABLE `scdl_jyzx` (
  `id` varchar(255) NOT NULL COMMENT 'ID',
  `title` varchar(255) DEFAULT NULL COMMENT '标题',
  `url` varchar(255) NOT NULL COMMENT 'url',
  `first` varchar(255) DEFAULT NULL COMMENT '分类一级',
  `second` varchar(255) DEFAULT NULL COMMENT '分类二级',
  `content` longtext COMMENT '文本内容',
  `json` longtext NOT NULL COMMENT 'json内容base64',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='四川电力交易中心文件';

-- ----------------------------
-- Table structure for scdl_xwdt
-- ----------------------------
DROP TABLE IF EXISTS `scdl_xwdt`;
CREATE TABLE `scdl_xwdt` (
  `id` varchar(255) NOT NULL COMMENT 'ID',
  `title` varchar(255) DEFAULT NULL COMMENT '标题',
  `classify` varchar(255) DEFAULT NULL COMMENT '类型',
  `classify_name` varchar(255) DEFAULT NULL COMMENT '类型名称',
  `pub_date` varchar(255) DEFAULT NULL COMMENT '发布日期',
  `url` varchar(255) NOT NULL COMMENT 'url',
  `content` longtext COMMENT '文本内容',
  `json` longtext NOT NULL COMMENT 'json内容base64',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='四川电力-新闻动态';

-- ----------------------------
-- Table structure for scdl_xxgk
-- ----------------------------
DROP TABLE IF EXISTS `scdl_xxgk`;
CREATE TABLE `scdl_xxgk` (
  `id` varchar(255) NOT NULL COMMENT 'ID',
  `title` varchar(255) DEFAULT NULL COMMENT '标题',
  `classify` varchar(255) DEFAULT NULL COMMENT '类型',
  `classify_name` varchar(255) DEFAULT NULL COMMENT '类型名称',
  `pub_date` varchar(255) DEFAULT NULL COMMENT '发布日期',
  `url` varchar(255) NOT NULL COMMENT 'url',
  `content` longtext COMMENT '文本内容',
  `json` longtext NOT NULL COMMENT 'json内容base64',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='四川电力-信息公开';

SET FOREIGN_KEY_CHECKS = 1;
