CREATE SCHEMA `test_db` DEFAULT CHARACTER SET utf8 ;

CREATE TABLE `test_db`.`table_one` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '编号',
  `name` VARCHAR(45) NOT NULL COMMENT '名称',
  `text` VARCHAR(45) NULL COMMENT '文本',
  `status` TINYINT NULL DEFAULT 0 COMMENT '状态',
  PRIMARY KEY (`id`));

CREATE TABLE `test_db`.`table_two` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '编号',
  `title` VARCHAR(45) NOT NULL COMMENT '标题',
  `text` VARCHAR(45) NULL COMMENT '文本',
  `status` TINYINT NULL DEFAULT 0 COMMENT '状态',
  PRIMARY KEY (`id`));
  
  CREATE TABLE `test_db`.`table_user` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '编号',
  `name` VARCHAR(45) NOT NULL COMMENT '姓名',
  `passwd` VARCHAR(45) NULL COMMENT '密码',
  PRIMARY KEY (`id`));
