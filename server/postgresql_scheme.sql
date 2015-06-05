--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: blunder_comments; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE blunder_comments (
    id integer NOT NULL,
    user_id integer NOT NULL,
    blunder_id character varying(255) NOT NULL,
    date timestamp without time zone DEFAULT now() NOT NULL,
    parent_id integer,
    comment text NOT NULL
);


ALTER TABLE blunder_comments OWNER TO postgres;

--
-- Name: blunder_comments_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE blunder_comments_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE blunder_comments_id_seq OWNER TO postgres;

--
-- Name: blunder_comments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE blunder_comments_id_seq OWNED BY blunder_comments.id;


--
-- Name: blunder_comments_votes; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE blunder_comments_votes (
    id integer NOT NULL,
    user_id integer NOT NULL,
    comment_id integer NOT NULL,
    assign_date timestamp without time zone DEFAULT now() NOT NULL,
    vote integer NOT NULL,
    CONSTRAINT blunder_comments_votes_vote_check CHECK ((vote = ANY (ARRAY[(-1), 1])))
);


ALTER TABLE blunder_comments_votes OWNER TO postgres;

--
-- Name: blunder_comments_votes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE blunder_comments_votes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE blunder_comments_votes_id_seq OWNER TO postgres;

--
-- Name: blunder_comments_votes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE blunder_comments_votes_id_seq OWNED BY blunder_comments_votes.id;


--
-- Name: blunder_favorites; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE blunder_favorites (
    id integer NOT NULL,
    user_id integer NOT NULL,
    blunder_id character varying(255) NOT NULL,
    assign_date timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE blunder_favorites OWNER TO postgres;

--
-- Name: blunder_favorites_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE blunder_favorites_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE blunder_favorites_id_seq OWNER TO postgres;

--
-- Name: blunder_favorites_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE blunder_favorites_id_seq OWNED BY blunder_favorites.id;


--
-- Name: blunder_history; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE blunder_history (
    id integer NOT NULL,
    user_id integer NOT NULL,
    blunder_id character varying(255) NOT NULL,
    result integer NOT NULL,
    user_elo integer NOT NULL,
    blunder_elo integer NOT NULL,
    user_line character varying(255) NOT NULL,
    date_start timestamp without time zone NOT NULL,
    date_finish timestamp without time zone DEFAULT now() NOT NULL,
    CONSTRAINT blunder_history_result_check CHECK ((result = ANY (ARRAY[0, 1])))
);


ALTER TABLE blunder_history OWNER TO postgres;

--
-- Name: blunder_history_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE blunder_history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE blunder_history_id_seq OWNER TO postgres;

--
-- Name: blunder_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE blunder_history_id_seq OWNED BY blunder_history.id;


--
-- Name: blunder_tasks; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE blunder_tasks (
    id integer NOT NULL,
    user_id integer NOT NULL,
    blunder_id character varying(255) NOT NULL,
    assign_date timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE blunder_tasks OWNER TO postgres;

--
-- Name: blunder_tasks_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE blunder_tasks_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE blunder_tasks_id_seq OWNER TO postgres;

--
-- Name: blunder_tasks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE blunder_tasks_id_seq OWNED BY blunder_tasks.id;


--
-- Name: blunder_votes; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE blunder_votes (
    id integer NOT NULL,
    blunder_id character varying(255) NOT NULL,
    assign_date timestamp without time zone DEFAULT now() NOT NULL,
    vote integer NOT NULL,
    user_id integer NOT NULL,
    CONSTRAINT blunder_votes_vote_check CHECK ((vote = ANY (ARRAY[(-1), 1])))
);


ALTER TABLE blunder_votes OWNER TO postgres;

--
-- Name: blunder_votes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE blunder_votes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE blunder_votes_id_seq OWNER TO postgres;

--
-- Name: blunder_votes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE blunder_votes_id_seq OWNED BY blunder_votes.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE users (
    id integer NOT NULL,
    username character varying(255) NOT NULL,
    password character varying(255) NOT NULL,
    role integer NOT NULL,
    registration timestamp without time zone NOT NULL,
    last_login timestamp without time zone NOT NULL,
    elo integer DEFAULT 1500 NOT NULL,
    email character varying(255) DEFAULT ''::character varying NOT NULL,
    salt character varying(255) NOT NULL
);


ALTER TABLE users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE users_id_seq OWNED BY users.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY blunder_comments ALTER COLUMN id SET DEFAULT nextval('blunder_comments_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY blunder_comments_votes ALTER COLUMN id SET DEFAULT nextval('blunder_comments_votes_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY blunder_favorites ALTER COLUMN id SET DEFAULT nextval('blunder_favorites_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY blunder_history ALTER COLUMN id SET DEFAULT nextval('blunder_history_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY blunder_tasks ALTER COLUMN id SET DEFAULT nextval('blunder_tasks_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY blunder_votes ALTER COLUMN id SET DEFAULT nextval('blunder_votes_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY users ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);


--
-- Data for Name: blunder_comments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY blunder_comments (id, user_id, blunder_id, date, parent_id, comment) FROM stdin;
23	120	556b4381e13823404953bbc9	2015-06-05 15:52:51.109154	\N	fghfghf
\.


--
-- Name: blunder_comments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('blunder_comments_id_seq', 23, true);


--
-- Data for Name: blunder_comments_votes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY blunder_comments_votes (id, user_id, comment_id, assign_date, vote) FROM stdin;
\.


--
-- Name: blunder_comments_votes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('blunder_comments_votes_id_seq', 14, true);


--
-- Data for Name: blunder_favorites; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY blunder_favorites (id, user_id, blunder_id, assign_date) FROM stdin;
39	120	556b4381e13823404953bbc9	2015-06-05 15:52:47.44741
\.


--
-- Name: blunder_favorites_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('blunder_favorites_id_seq', 39, true);


--
-- Data for Name: blunder_history; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY blunder_history (id, user_id, blunder_id, result, user_elo, blunder_elo, user_line, date_start, date_finish) FROM stdin;
140	120	556b43a7e13823404953bbce	0	1237	1300	{Rxf5,e4}	2015-06-05 16:37:12.51485	2015-06-05 16:37:12.51485
141	120	556b434ce13823404953bbc4	0	1224	2500	{Nxe6,Bf4}	2015-06-05 16:45:01.95433	2015-06-05 16:45:50.285175
142	120	556b3a4be1382331efae3f4a	0	1224	1700	{Be3,Rxe3,Rxe3,Bxe3}	2015-06-05 16:46:05.931595	2015-06-05 16:46:12.425337
143	120	556b42f9e13823404953bbba	0	1222	1509	{Kxg4,Rg2+}	2015-06-05 16:46:15.312264	2015-06-05 16:46:22.537519
144	120	556b3bcce1382331efae3f70	0	1217	1500	{Kxg4,Rf5}	2015-06-05 16:51:57.0931	2015-06-05 16:52:11.833162
145	120	556b3a57e1382331efae3f4b	0	1212	1702	{Be2,Rxf2,Qxf2,Nf4,Qf3,Nxe2}	2015-06-05 16:52:34.473762	2015-06-05 16:53:07.722489
146	120	556b3af0e1382331efae3f5b	1	1210	1313		2015-06-05 16:53:18.021846	2015-06-05 16:53:26.226707
\.


--
-- Name: blunder_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('blunder_history_id_seq', 146, true);


--
-- Data for Name: blunder_tasks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY blunder_tasks (id, user_id, blunder_id, assign_date) FROM stdin;
\.


--
-- Name: blunder_tasks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('blunder_tasks_id_seq', 171, true);


--
-- Data for Name: blunder_votes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY blunder_votes (id, blunder_id, assign_date, vote, user_id) FROM stdin;
13	556b43b0e13823404953bbcf	2015-06-03 16:33:32.357754	-1	120
14	556b42f2e13823404953bbb9	2015-06-03 16:40:43.12862	1	122
15	556b3b1ce1382331efae3f60	2015-06-03 16:46:16.41893	1	122
16	556b4265e13823404953bbab	2015-06-04 08:50:28.866158	1	120
17	556b3acbe1382331efae3f57	2015-06-04 08:50:38.353441	-1	120
18	556b4381e13823404953bbc9	2015-06-05 15:52:46.060383	1	120
19	556b3bcce1382331efae3f70	2015-06-05 16:52:32.200985	1	120
\.


--
-- Name: blunder_votes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('blunder_votes_id_seq', 19, true);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY users (id, username, password, role, registration, last_login, elo, email, salt) FROM stdin;
121	Failuref	$2a$12$pXj7c8krKAGjM2dGLO6UoubtDLHKVNy4eQL/R9FvawhimxaVwwRsa	0	2015-05-28 03:25:05.64194	2015-06-01 19:37:10.166601	1671	chezstov@gmail.com	$2a$12$pXj7c8krKAGjM2dGLO6Uou
122	demo	$2a$12$cqwAprmH0bZYi/J2pWnVSeiGZcvA4u9KKbuK40EN30I//zNPZA6.a	3	2015-06-03 16:38:04.173926	2015-06-03 16:38:04.569265	1314		$2a$12$cqwAprmH0bZYi/J2pWnVSe
120	JackalSh	$2a$12$2lOJlAl0eLr8DqyId6236.1ZGbFhTgIel79qUoAxbj0.nLQoiOwmC	0	2015-05-28 03:24:31.500694	2015-06-04 09:26:17.445983	1231	jackalsh@gmail.com	$2a$12$2lOJlAl0eLr8DqyId6236.
\.


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('users_id_seq', 122, true);


--
-- Name: blunder_comments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY blunder_comments
    ADD CONSTRAINT blunder_comments_pkey PRIMARY KEY (id);


--
-- Name: blunder_comments_votes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY blunder_comments_votes
    ADD CONSTRAINT blunder_comments_votes_pkey PRIMARY KEY (id);


--
-- Name: blunder_comments_votes_user_id_comment_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY blunder_comments_votes
    ADD CONSTRAINT blunder_comments_votes_user_id_comment_id_key UNIQUE (user_id, comment_id);


--
-- Name: blunder_favorites_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY blunder_favorites
    ADD CONSTRAINT blunder_favorites_pkey PRIMARY KEY (id);


--
-- Name: blunder_favorites_user_id_blunder_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY blunder_favorites
    ADD CONSTRAINT blunder_favorites_user_id_blunder_id_key UNIQUE (user_id, blunder_id);


--
-- Name: blunder_history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY blunder_history
    ADD CONSTRAINT blunder_history_pkey PRIMARY KEY (id);


--
-- Name: blunder_tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY blunder_tasks
    ADD CONSTRAINT blunder_tasks_pkey PRIMARY KEY (id);


--
-- Name: blunder_tasks_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY blunder_tasks
    ADD CONSTRAINT blunder_tasks_user_id_key UNIQUE (user_id);


--
-- Name: blunder_votes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY blunder_votes
    ADD CONSTRAINT blunder_votes_pkey PRIMARY KEY (id);


--
-- Name: blunder_votes_user_id_blunder_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY blunder_votes
    ADD CONSTRAINT blunder_votes_user_id_blunder_id_key UNIQUE (user_id, blunder_id);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: blunder_comments_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY blunder_comments
    ADD CONSTRAINT blunder_comments_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES blunder_comments(id);


--
-- Name: blunder_comments_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY blunder_comments
    ADD CONSTRAINT blunder_comments_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id);


--
-- Name: blunder_comments_votes_comment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY blunder_comments_votes
    ADD CONSTRAINT blunder_comments_votes_comment_id_fkey FOREIGN KEY (comment_id) REFERENCES blunder_comments(id);


--
-- Name: blunder_comments_votes_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY blunder_comments_votes
    ADD CONSTRAINT blunder_comments_votes_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id);


--
-- Name: blunder_favorites_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY blunder_favorites
    ADD CONSTRAINT blunder_favorites_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id);


--
-- Name: blunder_history_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY blunder_history
    ADD CONSTRAINT blunder_history_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id);


--
-- Name: blunder_tasks_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY blunder_tasks
    ADD CONSTRAINT blunder_tasks_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id);


--
-- Name: blunder_votes_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY blunder_votes
    ADD CONSTRAINT blunder_votes_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

