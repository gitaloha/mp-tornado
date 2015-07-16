CREATE DATABASE IF NOT EXISTS `db_test`;
use `db_test`;

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` INT(10) NOT NULL AUTO_INCREMENT,
  `nickname` VARCHAR(50),
  `headimg` VARCHAR(300),
  `create_time` DATETIME NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

