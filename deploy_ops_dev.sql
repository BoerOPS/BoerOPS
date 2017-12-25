ALTER TABLE users DROP COLUMN id;
ALTER TABLE users CHANGE COLUMN gitlab_id id INTEGER;
ALTER TABLE users ADD PRIMARY KEY (id);
ALTER TABLE projects DROP COLUMN id;
UPDATE rel_project_host SET project_id=121 WHERE id > 2 AND id <= 7;
ALTER TABLE projects CHANGE COLUMN project_id id INTEGER;

a001cb353c1ef12bf3e6ed3dd9767a53df2041ef30f34b726b2b5eee889245be

DROP TABLE IF EXISTS `deploys`;
CREATE TABLE `deploys`  (
  `id` int(16) UNSIGNED NOT NULL AUTO_INCREMENT,
  `status` int(1) NULL DEFAULT NULL COMMENT '0: deploy recode created; \r\n1: prepare code;\r\n2: exec before commands;\r\n3: deploy code;\r\n4: exec after commands;',
  `project_id` int(8) NULL DEFAULT NULL,
  `branch_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `commit_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `user_id` int(8) NULL DEFAULT NULL,
  `introduce` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '版本概述',
  `created_at` datetime(0) NULL DEFAULT NULL,
  `updated_at` datetime(0) NULL DEFAULT NULL,
  `env` int(1) NULL DEFAULT NULL COMMENT '0: prod;1: test',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;