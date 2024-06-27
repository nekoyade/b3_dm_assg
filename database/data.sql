/*  PROJECT NAME:   b3_dm_assg
 *  FILE NAME:      data.sql
 *
 *  2024 Keitaro Kamo (@nekoyade)
 *
 */

PRAGMA foreign_keys = true;


/* Tables */

INSERT INTO persons VALUES ('PS000000', 'Sample Taro', '2003-08-23', 'Somewhere');
-- INSERT INTO persons VALUES ('PS', '', '--', '');

-- INSERT INTO phones VALUES ('PS', '');

-- INSERT INTO emails VALUES ('PS', '');

-- INSERT INTO roles VALUES ('PS', '');

-- INSERT INTO instruments VALUES ('PS', '');

INSERT INTO groups VALUES ('GP001', '山谷連', 'A 県 X 市', null, 'regular', null, 'PS000000');
INSERT INTO groups VALUES ('GP002', '海原連', 'A 県 X 市 XC 地区', null, 'regular', null, 'PS000000');
INSERT INTO groups VALUES ('GP003', '清風連', 'A 県 Y 町 YB 郡', 'gp003@example.com', 'regular', null, 'PS000000');
INSERT INTO groups VALUES ('GP004', '工業連', 'A 県 X 市 XA 地区', null, 'corporate', 'XA 工業', 'PS000000');
INSERT INTO groups VALUES ('GP005', '電子連', 'A 県 Y 町 YA 郡', 'gp005@example.com', 'corporate', 'Y エレクトロニクス', 'PS000000');
INSERT INTO groups VALUES ('GP006', '不動連', 'A 県 X 市 XB 地区', 'gp006@example.com', 'corporate', 'XB エステート', 'PS000000');
INSERT INTO groups VALUES ('GP007', '阿学連', 'A 県 X 市', null, 'student', 'X 大学 阿波踊り研究会', 'PS000000');
INSERT INTO groups VALUES ('GP008', '文大連', 'A 県 X 市 XA 地区', 'gp008@example.com', 'student', 'X 文化学院大学', 'PS000000');
-- INSERT INTO groups VALUES ('GP', '', '', null, '', null, 'PS');

INSERT INTO venues VALUES ('VN001', '屋外', 'A 県 X 市');
INSERT INTO venues VALUES ('VN002', 'X 市文化センター', 'A 県 X 市本町');
INSERT INTO venues VALUES ('VN003', 'XB 劇場', 'A 県 X 市 XB 地区');
INSERT INTO venues VALUES ('VN004', 'XB 東演芸ホール', 'A 県 X 市 XB 地区');
-- INSERT INTO venues VALUES ('VN', '', '');

INSERT INTO sections VALUES ('SC001', 'XX 電鉄 X 駅前広場', 5000, 'VN001');
INSERT INTO sections VALUES ('SC002', '市役所通り', 2000, 'VN001');
INSERT INTO sections VALUES ('SC003', '目抜き通り', 3000, 'VN001');
INSERT INTO sections VALUES ('SC004', 'X 市立自然公園', 8000, 'VN001');
INSERT INTO sections VALUES ('SC005', 'A ホール', 700, 'VN002');
INSERT INTO sections VALUES ('SC006', 'B ホール', 500, 'VN002');
INSERT INTO sections VALUES ('SC007', 'C ホール', 250, 'VN002');
INSERT INTO sections VALUES ('SC008', '大ホール', 800, 'VN003');
INSERT INTO sections VALUES ('SC009', '小ホール', 300, 'VN003');
INSERT INTO sections VALUES ('SC010', 'ホール 1', 550, 'VN004');
INSERT INTO sections VALUES ('SC011', 'ホール 2', 250, 'VN004');
-- INSERT INTO sections VALUES ('SC', '', , 'VN');

-- INSERT INTO performances VALUES ('PF', '', '', 'GP', 'SC');

-- INSERT INTO reservations VALUES ('PS', 'PF', '', '');


/* Join tables */

-- INSERT INTO households VALUES ('PS', 'PS');

-- INSERT INTO persons_groups VALUES ('PS', 'GP');
