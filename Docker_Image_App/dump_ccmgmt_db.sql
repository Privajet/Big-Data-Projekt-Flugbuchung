--
-- PostgreSQL database dump
--

-- Dumped from database version 13.1
-- Dumped by pg_dump version 13.1

-- Started on 2021-05-31 22:45:09

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
-- TOC entry 212 (class 1255 OID 17230)
-- Name: test_audit(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.test_audit() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin
	if (TG_OP = 'DELETE') THEN
		insert into corona_tests_audit values( 'D',now(), user, OLD.*);
	ELSIF(TG_OP = 'UPDATE') THEN
		insert into corona_tests_audit values( 'U',now(), user, OLD.*);
	ELSIF(TG_OP = 'INSERT') THEN
		insert into corona_tests_audit values( 'I',now(), user, NEW.*);
end if;
return null;
end;
$$;


ALTER FUNCTION public.test_audit() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 204 (class 1259 OID 16600)
-- Name: branches; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.branches (
    branch_number integer NOT NULL,
    supervisor_no integer,
    "Location" character(30) NOT NULL
);


ALTER TABLE public.branches OWNER TO postgres;

--
-- TOC entry 203 (class 1259 OID 16597)
-- Name: corona_tests; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.corona_tests (
    pers_no integer NOT NULL,
    test_date date NOT NULL,
    id integer NOT NULL,
    positive boolean NOT NULL
);


ALTER TABLE public.corona_tests OWNER TO postgres;

--
-- TOC entry 200 (class 1259 OID 16582)
-- Name: employees; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.employees (
    age integer NOT NULL,
    chip_number integer NOT NULL,
    personal_number integer NOT NULL,
    department_number integer,
    first_name character(30) NOT NULL,
    last_name character(30) NOT NULL
);


ALTER TABLE public.employees OWNER TO postgres;

--
-- TOC entry 208 (class 1259 OID 16747)
-- Name: presence; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.presence (
    room_no integer NOT NULL,
    chip_no integer NOT NULL,
    time_checkin time without time zone,
    time_checkout time without time zone,
    "ID" integer NOT NULL,
    date date NOT NULL
);


ALTER TABLE public.presence OWNER TO postgres;

--
-- TOC entry 209 (class 1259 OID 16757)
-- Name: infected_areas; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.infected_areas AS
 SELECT presence.room_no,
    presence.date
   FROM ((public.corona_tests
     JOIN public.employees ON (((corona_tests.pers_no = employees.personal_number) AND (corona_tests.positive = true))))
     LEFT JOIN public.presence ON ((employees.chip_number = presence.chip_no)));


ALTER TABLE public.infected_areas OWNER TO postgres;

--
-- TOC entry 211 (class 1259 OID 17233)
-- Name: contactpersons; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.contactpersons AS
 SELECT employees.first_name,
    employees.last_name,
    employees.department_number
   FROM ((public.employees
     RIGHT JOIN ( SELECT presence.room_no,
            presence.chip_no,
            presence.time_checkin,
            presence.time_checkout,
            presence."ID",
            presence.date,
            infected_areas.room_no,
            infected_areas.date
           FROM (public.presence
             JOIN public.infected_areas ON (((presence.room_no = infected_areas.room_no) AND (presence.date = infected_areas.date))))) infctd(room_no, chip_no, time_checkin, time_checkout, "ID", date, room_no_1, date_1) ON ((employees.chip_number = infctd.chip_no)))
     LEFT JOIN public.corona_tests ON ((employees.personal_number = corona_tests.pers_no)))
  WHERE (corona_tests.positive IS NOT TRUE);


ALTER TABLE public.contactpersons OWNER TO postgres;

--
-- TOC entry 210 (class 1259 OID 17227)
-- Name: corona_tests_audit; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.corona_tests_audit (
    operation character(1) NOT NULL,
    timelog timestamp without time zone NOT NULL,
    user_id character(45) NOT NULL,
    pers_no integer,
    test_date date,
    id integer,
    positive boolean
);


ALTER TABLE public.corona_tests_audit OWNER TO postgres;

--
-- TOC entry 206 (class 1259 OID 16722)
-- Name: corona_tests_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.corona_tests ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.corona_tests_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 201 (class 1259 OID 16585)
-- Name: department; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.department (
    department_number integer NOT NULL,
    supervisors_pers_no integer
);


ALTER TABLE public.department OWNER TO postgres;

--
-- TOC entry 207 (class 1259 OID 16745)
-- Name: presence_ID_seq1; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.presence ALTER COLUMN "ID" ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."presence_ID_seq1"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 202 (class 1259 OID 16591)
-- Name: rooms; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rooms (
    room_no integer NOT NULL,
    unique_id integer NOT NULL,
    capacity integer,
    branch_no integer NOT NULL,
    department_no integer
);


ALTER TABLE public.rooms OWNER TO postgres;

--
-- TOC entry 205 (class 1259 OID 16603)
-- Name: vaccinations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.vaccinations (
    pers_no integer NOT NULL,
    vacc_completed boolean NOT NULL
);


ALTER TABLE public.vaccinations OWNER TO postgres;

--
-- TOC entry 3051 (class 0 OID 16600)
-- Dependencies: 204
-- Data for Name: branches; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.branches VALUES (1, 11344279, 'London
                       ');
INSERT INTO public.branches VALUES (2, 57893811, 'Mannheim                      ');
INSERT INTO public.branches VALUES (3, 65468481, 'Berlin
                       ');


--
-- TOC entry 3050 (class 0 OID 16597)
-- Dependencies: 203
-- Data for Name: corona_tests; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.corona_tests OVERRIDING SYSTEM VALUE VALUES (14572648, '2021-05-19', 7, false);
INSERT INTO public.corona_tests OVERRIDING SYSTEM VALUE VALUES (99999999, '2021-05-14', 8, false);
INSERT INTO public.corona_tests OVERRIDING SYSTEM VALUE VALUES (11344279, '2021-05-16', 3, true);


--
-- TOC entry 3056 (class 0 OID 17227)
-- Dependencies: 210
-- Data for Name: corona_tests_audit; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.corona_tests_audit VALUES ('I', '2021-05-27 21:06:46.4502', 'postgres                                     ', 14572648, '2021-05-19', 7, NULL);
INSERT INTO public.corona_tests_audit VALUES ('U', '2021-05-27 21:07:00.665456', 'postgres                                     ', 14572648, '2021-05-19', 7, NULL);
INSERT INTO public.corona_tests_audit VALUES ('D', '2021-05-31 19:10:53.177179', 'postgres                                     ', 11344279, '2021-05-13', 4, false);
INSERT INTO public.corona_tests_audit VALUES ('I', '2021-05-31 19:12:09.94634', 'postgres                                     ', 99999999, '2021-05-14', 8, false);
INSERT INTO public.corona_tests_audit VALUES ('U', '2021-05-31 19:13:02.510588', 'postgres                                     ', 11344279, '2021-05-15', 3, true);


--
-- TOC entry 3048 (class 0 OID 16585)
-- Dependencies: 201
-- Data for Name: department; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.department VALUES (2002, 11344279);
INSERT INTO public.department VALUES (4002, 11344279);
INSERT INTO public.department VALUES (1001, 12245881);
INSERT INTO public.department VALUES (1002, 57893811);
INSERT INTO public.department VALUES (2001, 56465841);
INSERT INTO public.department VALUES (3001, 56465841);
INSERT INTO public.department VALUES (9003, 65468481);


--
-- TOC entry 3047 (class 0 OID 16582)
-- Dependencies: 200
-- Data for Name: employees; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.employees VALUES (31, 112359, 12245881, 1002, 'Clarin

                      ', 'Edte                          ');
INSERT INTO public.employees VALUES (31, 136548, 56465841, 2002, 'John                          ', 'Doe                           ');
INSERT INTO public.employees VALUES (20, 123456, 11344279, 4002, 'Patient
                      ', 'Zero                          ');
INSERT INTO public.employees VALUES (25, 876543, 57893811, 9003, 'Mr. 
                         ', 'T
                            ');
INSERT INTO public.employees VALUES (28, 848356, 65468481, 3001, 'Max                           ', 'Mustermann
                   ');
INSERT INTO public.employees VALUES (29, 158347, 86493572, 1002, 'Maria                         ', 'Ployee
                       ');
INSERT INTO public.employees VALUES (40, 111111, 99999999, 9003, 'Chuck                         ', 'Neris
                        ');
INSERT INTO public.employees VALUES (35, 156486, 15687635, 4002, 'Hugh                          ', 'Jass
                         ');
INSERT INTO public.employees VALUES (38, 154725, 14572648, 3001, 'Amanda                        ', 'Hugginkiss                    ');
INSERT INTO public.employees VALUES (27, 154476, 15763985, 2002, 'Mike                          ', 'Rotch

                       ');
INSERT INTO public.employees VALUES (30, 444444, 888888, NULL, 'Chuck                         ', 'Testa                         ');


--
-- TOC entry 3055 (class 0 OID 16747)
-- Dependencies: 208
-- Data for Name: presence; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.presence OVERRIDING SYSTEM VALUE VALUES (12, 112359, '12:30:00', '13:30:00', 5, '2021-05-15');
INSERT INTO public.presence OVERRIDING SYSTEM VALUE VALUES (12, 123456, '08:30:00', '16:00:00', 6, '2021-05-15');
INSERT INTO public.presence OVERRIDING SYSTEM VALUE VALUES (13, 123456, '09:00:00', '18:00:00', 7, '2021-05-15');
INSERT INTO public.presence OVERRIDING SYSTEM VALUE VALUES (15, 123456, '08:50:00', '18:00:00', 8, '2021-05-13');
INSERT INTO public.presence OVERRIDING SYSTEM VALUE VALUES (18, 136548, '09:20:00', '13:00:00', 9, '2021-05-15');
INSERT INTO public.presence OVERRIDING SYSTEM VALUE VALUES (12, 136548, '07:55:00', '16:00:00', 10, '2021-04-01');
INSERT INTO public.presence OVERRIDING SYSTEM VALUE VALUES (15, 136548, '08:55:00', '18:00:00', 11, '2021-05-13');


--
-- TOC entry 3049 (class 0 OID 16591)
-- Dependencies: 202
-- Data for Name: rooms; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.rooms VALUES (10, 110, 8, 1, 1001);
INSERT INTO public.rooms VALUES (11, 111, 4, 1, 2001);
INSERT INTO public.rooms VALUES (12, 112, 10, 1, 3001);
INSERT INTO public.rooms VALUES (1, 201, 5, 2, 1002);
INSERT INTO public.rooms VALUES (2, 202, 10, 2, 2002);
INSERT INTO public.rooms VALUES (3, 203, 4, 2, 4002);
INSERT INTO public.rooms VALUES (50, 350, 15, 3, 9003);


--
-- TOC entry 3052 (class 0 OID 16603)
-- Dependencies: 205
-- Data for Name: vaccinations; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.vaccinations VALUES (99999999, true);
INSERT INTO public.vaccinations VALUES (11344279, false);
INSERT INTO public.vaccinations VALUES (15763985, false);
INSERT INTO public.vaccinations VALUES (57893811, false);
INSERT INTO public.vaccinations VALUES (86493572, true);


--
-- TOC entry 3062 (class 0 OID 0)
-- Dependencies: 206
-- Name: corona_tests_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.corona_tests_id_seq', 8, true);


--
-- TOC entry 3063 (class 0 OID 0)
-- Dependencies: 207
-- Name: presence_ID_seq1; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."presence_ID_seq1"', 11, true);


--
-- TOC entry 2902 (class 2606 OID 16696)
-- Name: branches branches_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.branches
    ADD CONSTRAINT branches_pkey PRIMARY KEY (branch_number);


--
-- TOC entry 2892 (class 2606 OID 16712)
-- Name: employees chipnumber; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT chipnumber UNIQUE (chip_number) INCLUDE (chip_number);


--
-- TOC entry 2900 (class 2606 OID 16728)
-- Name: corona_tests corona_tests_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.corona_tests
    ADD CONSTRAINT corona_tests_pkey PRIMARY KEY (id);


--
-- TOC entry 2896 (class 2606 OID 17016)
-- Name: department department_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.department
    ADD CONSTRAINT department_pkey PRIMARY KEY (department_number);


--
-- TOC entry 2894 (class 2606 OID 16698)
-- Name: employees employees_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_pkey PRIMARY KEY (personal_number);


--
-- TOC entry 2906 (class 2606 OID 16751)
-- Name: presence presence_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.presence
    ADD CONSTRAINT presence_pkey PRIMARY KEY ("ID");


--
-- TOC entry 2898 (class 2606 OID 17001)
-- Name: rooms rooms_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms
    ADD CONSTRAINT rooms_pkey PRIMARY KEY (unique_id);


--
-- TOC entry 2904 (class 2606 OID 17037)
-- Name: vaccinations vaccinations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vaccinations
    ADD CONSTRAINT vaccinations_pkey PRIMARY KEY (pers_no);


--
-- TOC entry 2914 (class 2620 OID 17231)
-- Name: corona_tests tests_audit_trigger; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tests_audit_trigger AFTER INSERT OR DELETE OR UPDATE ON public.corona_tests FOR EACH ROW EXECUTE FUNCTION public.test_audit();


--
-- TOC entry 2910 (class 2606 OID 17415)
-- Name: rooms branch; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms
    ADD CONSTRAINT branch FOREIGN KEY (branch_no) REFERENCES public.branches(branch_number) NOT VALID;


--
-- TOC entry 2913 (class 2606 OID 16752)
-- Name: presence chipmatching; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.presence
    ADD CONSTRAINT chipmatching FOREIGN KEY (chip_no) REFERENCES public.employees(chip_number);


--
-- TOC entry 2911 (class 2606 OID 16699)
-- Name: corona_tests corona_tests_pers_no_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.corona_tests
    ADD CONSTRAINT corona_tests_pers_no_fkey FOREIGN KEY (pers_no) REFERENCES public.employees(personal_number) NOT VALID;


--
-- TOC entry 2909 (class 2606 OID 17022)
-- Name: rooms dept_no; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms
    ADD CONSTRAINT dept_no FOREIGN KEY (department_no) REFERENCES public.department(department_number) NOT VALID;


--
-- TOC entry 2907 (class 2606 OID 17031)
-- Name: employees dept_no; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT dept_no FOREIGN KEY (department_number) REFERENCES public.department(department_number) NOT VALID;


--
-- TOC entry 2908 (class 2606 OID 17017)
-- Name: department persno; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.department
    ADD CONSTRAINT persno FOREIGN KEY (supervisors_pers_no) REFERENCES public.employees(personal_number) NOT VALID;


--
-- TOC entry 2912 (class 2606 OID 17038)
-- Name: vaccinations persno; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vaccinations
    ADD CONSTRAINT persno FOREIGN KEY (pers_no) REFERENCES public.employees(personal_number) NOT VALID;


-- Completed on 2021-05-31 22:45:09

--
-- PostgreSQL database dump complete
--

