CREATE TABLE IF NOT EXISTS `itrago` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `username` varchar(250) NOT NULL,
  `password` varchar(250) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

INSERT INTO `itrago` (`id`, `username`, `password`) VALUES
(1, 'itrago', '0d1e46a9bc407c2601969ac20b7a9d0f8da1a8b0'),
(2, 'administrator', '504e73cf0aede565e54e1e9957960e3f0451ca9c'),
(3, 'support', '5d4c23967dbb4f75e6fe42dffd45489fb46ab9ce'),
(4, 'praktikant', '40a2eb7c7f7300014012420c39e6fbedc75eeab2');
