CREATE DATABASE IF NOT EXISTS `box_data` DEFAULT CHARSET utf8 COLLATE utf8_general_ci;

use box_data;

set names 'utf8';

CREATE TABLE IF NOT EXISTS `box_comment`(
`id` INT(10) NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT '主键id',
`content_id` INT(10) NOT NULL COMMENT '内容id',
`nickname` VARCHAR(50) NOT NULL COMMENT '用户评论名称',
`cover` VARCHAR(255) NOT NULL COMMENT '头像地址',
`comment` VARCHAR(255) NOT NULL COMMENT '评论信息',
`comment_time` INT(10) NOT NULL COMMENT '评论时间',
`pid` INT(10)  COMMENT '上级',
`source_id` BIGINT(11) NOT NULL COMMENT '源id')
;