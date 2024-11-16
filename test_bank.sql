/*
 Navicat Premium Data Transfer

 Source Server         : host
 Source Server Type    : MySQL
 Source Server Version : 80035
 Source Host           : localhost:3306
 Source Schema         : test_bank

 Target Server Type    : MySQL
 Target Server Version : 80035
 File Encoding         : 65001

 Date: 15/11/2024 14:53:04
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for bank_transactions
-- ----------------------------
DROP TABLE IF EXISTS `bank_transactions`;
CREATE TABLE `bank_transactions`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '交易标识',
  `user_id` int NULL DEFAULT NULL COMMENT '交易用户的id',
  `money` double NOT NULL COMMENT '交易的金额',
  `time` datetime NOT NULL COMMENT '交易日期',
  `note` varchar(255) CHARACTER SET gbk COLLATE gbk_chinese_ci NULL DEFAULT NULL COMMENT '交易备注',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE SET NULL ON UPDATE SET NULL
) ENGINE = InnoDB AUTO_INCREMENT = 27 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of bank_transactions
-- ----------------------------
INSERT INTO `bank_transactions` VALUES (14, 1, 1000, '2024-09-30 19:57:10', NULL);
INSERT INTO `bank_transactions` VALUES (15, 1, 1000, '2024-09-30 19:59:11', NULL);
INSERT INTO `bank_transactions` VALUES (16, 1, 5000, '2024-09-30 20:45:45', NULL);
INSERT INTO `bank_transactions` VALUES (17, 1, -100, '2024-09-30 21:08:15', NULL);
INSERT INTO `bank_transactions` VALUES (18, 1, -4000, '2024-09-30 21:08:27', NULL);
INSERT INTO `bank_transactions` VALUES (19, 8, 100, '2024-10-12 17:20:15', NULL);
INSERT INTO `bank_transactions` VALUES (20, 8, 1000, '2024-10-12 17:24:15', NULL);
INSERT INTO `bank_transactions` VALUES (21, 8, 1000, '2024-10-12 17:24:44', NULL);
INSERT INTO `bank_transactions` VALUES (22, 8, -500, '2024-10-12 17:25:13', NULL);
INSERT INTO `bank_transactions` VALUES (23, 8, -10000, '2024-10-12 17:29:27', NULL);
INSERT INTO `bank_transactions` VALUES (24, 8, 100, '2024-10-14 14:31:03', NULL);
INSERT INTO `bank_transactions` VALUES (25, 8, 100, '2024-10-18 14:16:09', NULL);
INSERT INTO `bank_transactions` VALUES (26, 8, -100, '2024-10-18 14:16:15', NULL);

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '用户id',
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '用户名',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '用户密码',
  `permission` tinyint NOT NULL COMMENT '用户权限，1为超级用户，2为普通用户',
  `yue` double NOT NULL DEFAULT 0 COMMENT '用户余额',
  INDEX `id`(`id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 18 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (1, 'root', '123', 1, 1800);
INSERT INTO `user` VALUES (3, '测试1', '1', 2, 500000);
INSERT INTO `user` VALUES (8, 'root2', '123', 2, 110);
INSERT INTO `user` VALUES (9, '15083700341', '113', 1, 11111);
INSERT INTO `user` VALUES (13, '测试4', '111', 2, 10000);

SET FOREIGN_KEY_CHECKS = 1;
