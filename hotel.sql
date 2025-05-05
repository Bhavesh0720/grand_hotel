-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 13, 2024 at 08:43 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `hotel`
--

-- --------------------------------------------------------

--
-- Table structure for table `contact_form`
--

CREATE TABLE `contact_form` (
  `contact_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `email` varchar(255) NOT NULL,
  `message` text NOT NULL,
  `submitted_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `contact_form`
--

INSERT INTO `contact_form` (`contact_id`, `name`, `phone`, `email`, `message`, `submitted_at`) VALUES
(1, 'dhaval', '3245678390', 'dhaval123@gmail.com', 'xrdftgyuijsdmc', '2024-09-11 10:00:45'),
(2, 'montu', '8576467890', 'montu123@gmail.com', 'montu mithhhhoooo', '2024-09-11 10:03:53'),
(3, 'sunil', '34768', 'sunil123@gmail.com', 'hin aechbb je', '2024-09-11 10:05:44'),
(4, 'ravi', '757329812', 'ravi123@gmail.com', 'vbhncmkd', '2024-09-12 04:34:34'),
(5, 'tufel ', '01987652', 'ml123@gmail.com', 'dxchj', '2024-09-12 04:49:46'),
(6, 'prashant', '827654873', 'prashant12@gmail.com', 'xrctvykjhvv', '2024-09-12 09:59:54');

-- --------------------------------------------------------

--
-- Table structure for table `reservations`
--

CREATE TABLE `reservations` (
  `reservation_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `room_id` varchar(30) DEFAULT NULL,
  `reservation_date` date DEFAULT NULL,
  `room_type` varchar(100) DEFAULT NULL,
  `check_in_date` date DEFAULT NULL,
  `check_out_date` date DEFAULT NULL,
  `notes` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `reservations`
--

INSERT INTO `reservations` (`reservation_id`, `user_id`, `room_id`, `reservation_date`, `room_type`, `check_in_date`, `check_out_date`, `notes`) VALUES
(1, 5, 'SR_NAC_1', '2024-09-12', 'Single Room (No AC)', '2024-09-12', '2024-09-13', 'erdtfyg'),
(2, 5, 'DS_1', '2024-09-12', 'Deluxe Suite', '2024-09-12', '2024-09-13', 'ertyguhijb'),
(5, 7, 'PS_5', '2024-09-13', 'Presidential Suite', '2024-09-13', '2024-09-14', 'dfkjhb');

-- --------------------------------------------------------

--
-- Table structure for table `room`
--

CREATE TABLE `room` (
  `room_id` varchar(30) NOT NULL,
  `room_type` varchar(100) DEFAULT NULL,
  `rate` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `room`
--

INSERT INTO `room` (`room_id`, `room_type`, `rate`) VALUES
('BC_1', 'Business Class', 155.00),
('BC_2', 'Business Class', 150.00),
('BC_3', 'Business Class', 150.00),
('BC_4', 'Business Class', 1111.00),
('DS_1', 'Deluxe Suite', 200.00),
('DS_2', 'Deluxe Suite', 200.00),
('DS_3', 'Deluxe Suite', 200.00),
('FR_1', 'Family Room', 120.00),
('FR_2', 'Family Room', 120.00),
('FR_3', 'Family Room', 120.00),
('JS_1', 'Junior Suite', 300.00),
('JS_2', 'Junior Suite', 300.00),
('JS_3', 'Junior Suite', 300.00),
('JS_4', 'Junior Suite', 1826.00),
('PS_1', 'Presidential Suite', 400.00),
('PS_2', 'Presidential Suite', 400.00),
('PS_3', 'Presidential Suite', 400.00),
('PS_5', 'Presidential Suite', 10000.00),
('SDS_1', 'Super Deluxe Suite', 250.00),
('SDS_2', 'Super Deluxe Suite', 250.00),
('SDS_3', 'Super Deluxe Suite', 250.00),
('SR_AC_1', 'Single Room (AC)', 70.00),
('SR_AC_2', 'Single Room (AC)', 70.00),
('SR_AC_3', 'Single Room (AC)', 70.00),
('SR_NAC_1', 'Single Room (No AC)', 50.00),
('SR_NAC_2', 'Single Room (No AC)', 50.00),
('SR_NAC_3', 'Single Room (No AC)', 50.00);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone_number` varchar(15) NOT NULL,
  `address` varchar(255) NOT NULL,
  `terms` tinyint(1) NOT NULL,
  `is_admin` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `first_name`, `last_name`, `password`, `email`, `phone_number`, `address`, `terms`, `is_admin`) VALUES
(5, 'prashant', '', 'prashant', 'prashant123@gmail.com', '463283722', 'rfghjbvcrtyhjn', 0, 0),
(6, 'Bhavesh', 'Parmar', 'bhavesh0720', 'bhavesh0720@gmail.com', '1234567890', 'gdvcbdjbhvj', 0, 1),
(7, 'dhaval', 'Parmar', 'dhaval', 'dhaval123@gmail.com', '4632883722', 'rfghjbvcrtyhjn6774edf', 0, 0),
(8, 'tufel', '', 'tufel', 'tufel123@gmail.com', '6354613412', 'kalyanpur,tankar,morbi, 363650', 0, 0),
(9, 'ravi', 'bhatasana', 'ravi', 'ravi123@gmail.com', '01101001001', '01276372-1e36r278eev', 0, 0),
(10, 'prashant123', '', 'prashant123', 'aaaaaa@ggg.com', '123456', 'sdddd', 0, 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `contact_form`
--
ALTER TABLE `contact_form`
  ADD PRIMARY KEY (`contact_id`);

--
-- Indexes for table `reservations`
--
ALTER TABLE `reservations`
  ADD PRIMARY KEY (`reservation_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `room_id` (`room_id`);

--
-- Indexes for table `room`
--
ALTER TABLE `room`
  ADD PRIMARY KEY (`room_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `contact_form`
--
ALTER TABLE `contact_form`
  MODIFY `contact_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `reservations`
--
ALTER TABLE `reservations`
  MODIFY `reservation_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `reservations`
--
ALTER TABLE `reservations`
  ADD CONSTRAINT `reservations_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  ADD CONSTRAINT `reservations_ibfk_2` FOREIGN KEY (`room_id`) REFERENCES `room` (`room_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
