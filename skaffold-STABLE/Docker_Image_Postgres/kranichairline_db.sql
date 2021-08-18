--
-- PostgreSQL database dump
--

-- Dumped from database version 13.1
-- Dumped by pg_dump version 13.1

-- Started on 2021-06-25 17:55:08

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 3 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres

--
-- TOC entry 2987 (class 0 OID 0)
-- Dependencies: 3
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: post


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 200 (class 1259 OID 17421)
-- Name: Flights; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."flights" (
    flight_no integer NOT NULL,
    origin character(20),
    destination character(20),
    seats integer,
    booked_seats integer,
    price numeric
);


ALTER TABLE public."flights" OWNER TO postgres;

--
-- TOC entry 2981 (class 0 OID 17421)
-- Dependencies: 200
-- Data for Name: Flights; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."flights" (flight_no, origin, destination, seats, booked_seats, price) FROM stdin;
815	FRA                 	IAD                 	350	15	755.25
89	MCH\n                	EDTE                	25	2	1500
25	KJYO                	DFW\n                	60	10	269
1337	EDFM\n               	OMDB                	33	29	400
\.


--
-- TOC entry 2850 (class 2606 OID 17428)
-- Name: Flights Flights_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."flights"
    ADD CONSTRAINT "Flights_pkey" PRIMARY KEY (flight_no);


-- Completed on 2021-06-25 17:55:08

--
-- PostgreSQL database dump complete
--

