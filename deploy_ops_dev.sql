/*
 Navicat Premium Data Transfer

 Source Server         : Local Docker MySQL
 Source Server Type    : MySQL
 Source Server Version : 50717
 Source Host           : 127.0.0.1:3306
 Source Schema         : deploy_ops_dev

 Target Server Type    : MySQL
 Target Server Version : 50717
 File Encoding         : 65001

 Date: 21/12/2017 17:05:15
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for hosts
-- ----------------------------
DROP TABLE IF EXISTS `hosts`;
CREATE TABLE `hosts`  (
  `id` int(8) UNSIGNED NOT NULL AUTO_INCREMENT,
  `ip_addr` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `env` int(2) NOT NULL COMMENT 'prod:0, test:1',
  `created_at` datetime(0) NULL DEFAULT NULL,
  `updated_at` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 12 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of hosts
-- ----------------------------
INSERT INTO `hosts` VALUES (1, '192.168.28.12', 0, '2017-12-19 03:29:57', '2017-12-19 03:29:57');
INSERT INTO `hosts` VALUES (2, '172.19.3.24', 1, '2017-12-19 06:19:36', '2017-12-19 06:19:36');
INSERT INTO `hosts` VALUES (3, '192.168.28.13', 0, '2017-12-19 06:21:07', '2017-12-19 06:21:07');
INSERT INTO `hosts` VALUES (4, '172.19.3.25', 1, '2017-12-19 06:23:36', '2017-12-19 06:23:36');
INSERT INTO `hosts` VALUES (5, '172.19.3.28', 1, '2017-12-20 08:26:20', '2017-12-20 08:26:20');
INSERT INTO `hosts` VALUES (6, '172.19.3.29', 1, '2017-12-20 08:26:38', '2017-12-20 08:26:38');
INSERT INTO `hosts` VALUES (7, '192.168.26.1', 0, '2017-12-20 08:30:31', '2017-12-20 08:30:31');
INSERT INTO `hosts` VALUES (8, '192.168.26.2', 0, '2017-12-20 08:30:53', '2017-12-20 08:30:53');
INSERT INTO `hosts` VALUES (9, '192.168.28.14', 0, '2017-12-20 08:31:32', '2017-12-20 08:31:32');
INSERT INTO `hosts` VALUES (10, '192.168.28.15', 0, '2017-12-20 08:31:43', '2017-12-20 08:31:43');
INSERT INTO `hosts` VALUES (11, '192.168.28.23', 0, '2017-12-20 08:31:54', '2017-12-20 08:31:54');

-- ----------------------------
-- Table structure for projects
-- ----------------------------
DROP TABLE IF EXISTS `projects`;
CREATE TABLE `projects`  (
  `id` int(8) UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `before_checkout` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `after_checkout` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `before_deploy` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `after_deploy` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `project_id` int(4) NULL DEFAULT NULL,
  `created_at` datetime(0) NULL DEFAULT NULL,
  `updated_at` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of projects
-- ----------------------------
INSERT INTO `projects` VALUES (1, '主机监控', 'mkdir /data/www/monitor', 'chown www.www -R /data/www/monitor', 'ansible -m ping', 'ansible -m service -a \'name=nginx state=restarted\'', 136, '2017-12-20 08:16:18', '2017-12-20 08:16:18');
INSERT INTO `projects` VALUES (2, '自动提测（gitlab webhook）', '1', '2', '3', '4', 121, '2017-12-20 08:43:31', '2017-12-20 08:43:31');
INSERT INTO `projects` VALUES (3, '运维系统', '6', '6', '6', '6', 116, '2017-12-20 08:49:34', '2017-12-20 08:49:34');

-- ----------------------------
-- Table structure for rel_project_host
-- ----------------------------
DROP TABLE IF EXISTS `rel_project_host`;
CREATE TABLE `rel_project_host`  (
  `id` int(8) UNSIGNED NOT NULL AUTO_INCREMENT,
  `project_id` int(4) NULL DEFAULT NULL,
  `host_id` int(4) NULL DEFAULT NULL,
  `created_at` datetime(0) NULL DEFAULT NULL,
  `updated_at` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of rel_project_host
-- ----------------------------
INSERT INTO `rel_project_host` VALUES (1, 1, 1, '2017-12-20 08:16:18', '2017-12-20 08:16:18');
INSERT INTO `rel_project_host` VALUES (2, 1, 4, '2017-12-20 08:16:18', '2017-12-20 08:16:18');
INSERT INTO `rel_project_host` VALUES (3, 2, 11, '2017-12-20 08:43:31', '2017-12-20 08:43:31');
INSERT INTO `rel_project_host` VALUES (4, 2, 2, '2017-12-20 08:43:32', '2017-12-20 08:43:32');
INSERT INTO `rel_project_host` VALUES (5, 2, 4, '2017-12-20 08:43:32', '2017-12-20 08:43:32');
INSERT INTO `rel_project_host` VALUES (6, 2, 5, '2017-12-20 08:43:32', '2017-12-20 08:43:32');
INSERT INTO `rel_project_host` VALUES (7, 2, 6, '2017-12-20 08:43:32', '2017-12-20 08:43:32');
INSERT INTO `rel_project_host` VALUES (8, 3, 11, '2017-12-20 08:49:34', '2017-12-20 08:49:34');
INSERT INTO `rel_project_host` VALUES (9, 3, 2, '2017-12-20 08:49:34', '2017-12-20 08:49:34');
INSERT INTO `rel_project_host` VALUES (10, 3, 4, '2017-12-20 08:49:34', '2017-12-20 08:49:34');

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `id` int(16) UNSIGNED NOT NULL AUTO_INCREMENT,
  `gitlab_id` int(16) NULL DEFAULT NULL,
  `gitlab_name` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `gitlab_username` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `gitlab_email` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `gitlab_avatar` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `created_at` datetime(0) NULL DEFAULT NULL,
  `updated_at` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (2, 59, '陈波', 'chenbo', '150339480@qq.com', 'http://www.gravatar.com/avatar/8c81ec298bdd3aae42c93eee97934c93?s=80&d=identicon', '2017-10-13 07:48:06', '2017-10-13 07:48:06');
INSERT INTO `users` VALUES (3, 60, '魏振东', 'weizhendong', 'wzdxx1314@163.com', 'http://www.gravatar.com/avatar/a8e426bb4a423ebb9d69b8f139dcdae2?s=80&d=identicon', '2017-10-13 08:47:53', '2017-10-13 08:47:53');
INSERT INTO `users` VALUES (4, 58, '杰远飞', 'jieyuanfei', 'jie746635835@163.com', 'http://gitlab.onenet.com/uploads/-/system/user/avatar/58/%E5%A4%B4%E5%83%8F.jpg', '2017-10-13 08:52:33', '2017-10-13 08:52:33');
INSERT INTO `users` VALUES (5, 43, '谭江', 'tanjiang', '289801415@qq.com', 'http://www.gravatar.com/avatar/f003a376e1f129edf8b3110d003ddb02?s=80&d=identicon', '2017-12-06 03:22:02', '2017-12-06 03:22:02');
INSERT INTO `users` VALUES (6, 16, '高宇', 'gaoyu', '13996147982@163.com', 'http://gitlab.onenet.com/uploads/-/system/user/avatar/16/u_2407149380_2620804321_fm_21_gp_0.jpg', '2017-12-07 03:33:08', '2017-12-07 03:33:08');
INSERT INTO `users` VALUES (7, 2, '张海博', 'zhanghaibo', 'boer0924@qq.com', 'http://gitlab.onenet.com/uploads/-/system/user/avatar/2/top.jpg', '2017-12-18 09:23:58', '2017-12-18 09:23:58');
INSERT INTO `users` VALUES (8, 55, '谭泽', 'tanze', '284974796@qq.com', 'http://www.gravatar.com/avatar/5ed5c8091845d06687b5e1010bb20a1d?s=80&d=identicon', '2017-12-20 08:13:46', '2017-12-20 08:13:46');

SET FOREIGN_KEY_CHECKS = 1;
