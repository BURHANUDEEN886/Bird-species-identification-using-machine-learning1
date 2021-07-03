-- phpMyAdmin SQL Dump
-- version 4.3.11
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Jun 12, 2021 at 06:49 PM
-- Server version: 5.6.24
-- PHP Version: 5.5.24

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `customersatisfaction`
--

-- --------------------------------------------------------

--
-- Table structure for table `registration`
--

CREATE TABLE IF NOT EXISTS `registration` (
  `first_nm` varchar(50) NOT NULL,
  `last_nm` varchar(50) NOT NULL,
  `dob` varchar(50) NOT NULL,
  `age` int(11) NOT NULL,
  `email` varchar(50) NOT NULL,
  `phno` varchar(50) NOT NULL,
  `gender` varchar(50) NOT NULL,
  `addr` varchar(50) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `approve` int(11) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `registration`
--

INSERT INTO `registration` (`first_nm`, `last_nm`, `dob`, `age`, `email`, `phno`, `gender`, `addr`, `username`, `password`, `approve`) VALUES
('Arjun', 'A', '2020-12-02', 23, 'arjun@gmail.com', '9856362145', 'male', 'xsdvxsdf\n', 'arjun', 'arjun', 1),
('Vishal', 'S', '1994-10-03', 26, 'unni@gmail.com', '9874563211', 'male', 'Eloor North	\n', 'vis', 'vis', 1),
('Vaisakh', 'S', '2019-07-17', 27, 'vaiss@gmail.com', '9856321111', 'male', 'nnnbnbbn\n', 'vaiss', 'vaiss', 1),
('Awwe', 'A', '2021-05-05', 30, 'xxc@gghghng.cmm', '9652147830', 'male', 'ik\n', 'ik', 'ik', 0);

-- --------------------------------------------------------

--
-- Table structure for table `results`
--

CREATE TABLE IF NOT EXISTS `results` (
  `dates` datetime NOT NULL,
  `angry` varchar(100) NOT NULL,
  `happy` varchar(100) NOT NULL,
  `sad` varchar(100) NOT NULL,
  `fear` varchar(100) NOT NULL,
  `disgust` varchar(100) NOT NULL,
  `neutral` varchar(100) NOT NULL,
  `surprise` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `results`
--

INSERT INTO `results` (`dates`, `angry`, `happy`, `sad`, `fear`, `disgust`, `neutral`, `surprise`) VALUES
('2020-11-03 00:00:00', '10', '15', '45', '2', '1', '143', '2'),
('2020-12-21 00:00:00', '0', '0', '67', '0', '0', '3', '0'),
('2020-12-24 00:00:00', '0', '0', '12', '0', '0', '0', '0'),
('2021-05-08 00:00:00', '0', '0', '44', '0', '0', '4', '0');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `registration`
--
ALTER TABLE `registration`
  ADD UNIQUE KEY `email` (`email`), ADD UNIQUE KEY `username` (`username`), ADD UNIQUE KEY `phno` (`phno`), ADD UNIQUE KEY `phno_2` (`phno`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
