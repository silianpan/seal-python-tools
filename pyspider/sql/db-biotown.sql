/*
 Navicat Premium Data Transfer

 Source Server         : mysql-local
 Source Server Type    : MySQL
 Source Server Version : 50733
 Source Host           : localhost:3306
 Source Schema         : db-biotown-others

 Target Server Type    : MySQL
 Target Server Version : 50733
 File Encoding         : 65001

 Date: 31/01/2021 21:46:01
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for spider_bioasis
-- ----------------------------
DROP TABLE IF EXISTS `spider_bioasis`;
CREATE TABLE `spider_bioasis` (
  `id` varchar(64) NOT NULL COMMENT 'ID',
  `title` varchar(255) DEFAULT NULL COMMENT '标题',
  `content` longtext COMMENT '内容',
  `others` json DEFAULT NULL COMMENT '文章地址',
  `json_url` varchar(255) NOT NULL COMMENT '本地json路径',
  `classify_name` varchar(255) DEFAULT NULL COMMENT '分类名称',
  `classify` varchar(255) NOT NULL COMMENT '分类',
  `crt_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '爬取时间',
  `url` varchar(255) NOT NULL COMMENT '爬取url',
  `pub_date` date DEFAULT NULL COMMENT '发布时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for spider_biobay
-- ----------------------------
DROP TABLE IF EXISTS `spider_biobay`;
CREATE TABLE `spider_biobay` (
  `id` varchar(64) NOT NULL COMMENT 'ID',
  `title` varchar(255) DEFAULT NULL COMMENT '标题',
  `content` longtext COMMENT '内容',
  `others` json DEFAULT NULL COMMENT '文章地址',
  `json_url` varchar(255) NOT NULL COMMENT '本地json路径',
  `classify_name` varchar(255) DEFAULT NULL COMMENT '分类名称',
  `classify` varchar(255) NOT NULL COMMENT '分类',
  `crt_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '爬取时间',
  `url` varchar(255) NOT NULL COMMENT '爬取url',
  `pub_date` date DEFAULT NULL COMMENT '发布时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for spider_bybp
-- ----------------------------
DROP TABLE IF EXISTS `spider_bybp`;
CREATE TABLE `spider_bybp` (
  `id` varchar(64) NOT NULL COMMENT 'ID',
  `title` varchar(255) DEFAULT NULL COMMENT '标题',
  `content` longtext COMMENT '内容',
  `others` json DEFAULT NULL COMMENT '文章地址',
  `json_url` varchar(255) NOT NULL COMMENT '本地json路径',
  `classify_name` varchar(255) DEFAULT NULL COMMENT '分类名称',
  `classify` varchar(255) NOT NULL COMMENT '分类',
  `crt_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '爬取时间',
  `url` varchar(255) NOT NULL COMMENT '爬取url',
  `pub_date` date DEFAULT NULL COMMENT '发布时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for spider_cqbiocity
-- ----------------------------
DROP TABLE IF EXISTS `spider_cqbiocity`;
CREATE TABLE `spider_cqbiocity` (
  `id` varchar(64) NOT NULL COMMENT 'ID',
  `title` varchar(255) DEFAULT NULL COMMENT '标题',
  `content` longtext COMMENT '内容',
  `others` json DEFAULT NULL COMMENT '文章地址',
  `json_url` varchar(255) NOT NULL COMMENT '本地json路径',
  `classify_name` varchar(255) DEFAULT NULL COMMENT '分类名称',
  `classify` varchar(255) NOT NULL COMMENT '分类',
  `crt_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '爬取时间',
  `url` varchar(255) NOT NULL COMMENT '爬取url',
  `pub_date` date DEFAULT NULL COMMENT '发布时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for spider_shimsp
-- ----------------------------
DROP TABLE IF EXISTS `spider_shimsp`;
CREATE TABLE `spider_shimsp` (
  `id` varchar(64) NOT NULL COMMENT 'ID',
  `title` varchar(255) DEFAULT NULL COMMENT '标题',
  `content` longtext COMMENT '内容',
  `others` json DEFAULT NULL COMMENT '文章地址',
  `json_url` varchar(255) NOT NULL COMMENT '本地json路径',
  `classify_name` varchar(255) DEFAULT NULL COMMENT '分类名称',
  `classify` varchar(255) NOT NULL COMMENT '分类',
  `crt_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '爬取时间',
  `url` varchar(255) NOT NULL COMMENT '爬取url',
  `pub_date` date DEFAULT NULL COMMENT '发布时间',
  `thumbnail` varchar(255) DEFAULT NULL COMMENT '缩略图',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
