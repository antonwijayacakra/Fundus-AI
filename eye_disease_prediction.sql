-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 23 Jun 2024 pada 18.08
-- Versi server: 10.4.32-MariaDB
-- Versi PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `eye_disease_prediction`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `prediction`
--

CREATE TABLE `prediction` (
  `id` int(11) NOT NULL,
  `filename` varchar(255) NOT NULL,
  `prediction` varchar(50) NOT NULL,
  `upload_date` datetime DEFAULT NULL,
  `model` char(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `prediction`
--

INSERT INTO `prediction` (`id`, `filename`, `prediction`, `upload_date`, `model`) VALUES
(63, 'DR.jpeg', 'DR', '2024-06-23 22:28:11', ''),
(64, 'DR.jpeg', 'retinopathy', '2024-06-23 22:47:00', 'xception'),
(65, 'DR.jpeg', 'retinopathy', '2024-06-23 22:48:21', 'xception'),
(66, 'DR.jpeg', 'glaucoma', '2024-06-23 22:48:43', 'mobilenet'),
(67, 'DR.jpeg', 'glaucoma', '2024-06-23 22:48:51', 'vgg16'),
(68, 'DR.jpeg', 'glaucoma', '2024-06-23 22:50:08', 'mobilenet'),
(69, 'DR.jpeg', 'glaucoma', '2024-06-23 22:50:08', 'mobilenet'),
(70, 'DR.jpeg', 'glaucoma', '2024-06-23 22:50:15', 'vgg16'),
(71, 'Glaucoma_test.jpg', 'normal', '2024-06-23 22:50:31', 'mobilenet'),
(72, 'Glaucoma_test.jpg', 'normal', '2024-06-23 22:50:42', 'vgg16'),
(73, 'DR.jpg', 'DR', '2024-06-23 22:52:05', 'xception'),
(74, 'DR.jpg', 'DR', '2024-06-23 22:52:16', 'mobilenet'),
(75, 'DR.jpg', 'DR', '2024-06-23 22:52:25', 'vgg16');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `prediction`
--
ALTER TABLE `prediction`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `prediction`
--
ALTER TABLE `prediction`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=76;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
