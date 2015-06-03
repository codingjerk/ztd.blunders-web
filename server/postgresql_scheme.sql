--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
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
    parent_id integer DEFAULT 0 NOT NULL,
    comment text NOT NULL
);


ALTER TABLE public.blunder_comments OWNER TO postgres;

--
-- Name: blunder_comments_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE blunder_comments_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.blunder_comments_id_seq OWNER TO postgres;

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


ALTER TABLE public.blunder_comments_votes OWNER TO postgres;

--
-- Name: blunder_comments_votes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE blunder_comments_votes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.blunder_comments_votes_id_seq OWNER TO postgres;

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


ALTER TABLE public.blunder_favorites OWNER TO postgres;

--
-- Name: blunder_favorites_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE blunder_favorites_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.blunder_favorites_id_seq OWNER TO postgres;

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
    date timestamp without time zone DEFAULT now() NOT NULL,
    user_line character varying(255) NOT NULL,
    CONSTRAINT blunder_history_result_check CHECK ((result = ANY (ARRAY[0, 1])))
);


ALTER TABLE public.blunder_history OWNER TO postgres;

--
-- Name: blunder_history_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE blunder_history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.blunder_history_id_seq OWNER TO postgres;

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


ALTER TABLE public.blunder_tasks OWNER TO postgres;

--
-- Name: blunder_tasks_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE blunder_tasks_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.blunder_tasks_id_seq OWNER TO postgres;

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


ALTER TABLE public.blunder_votes OWNER TO postgres;

--
-- Name: blunder_votes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE blunder_votes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.blunder_votes_id_seq OWNER TO postgres;

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


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO postgres;

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
1	120	556b3b9be1382331efae3f6b	2015-06-02 14:10:01.156	0	fgfg
2	120	556b336ee138232acf525080	2015-06-02 14:52:39.45111	0	sdfdsfdsf
3	120	556b43b0e13823404953bbcf	2015-06-02 15:01:21.187979	0	hjkjhkjhk
4	120	556b43b0e13823404953bbcf	2015-06-03 16:33:11.447524	3	Hi\n
5	120	556b42f2e13823404953bbb9	2015-06-03 16:37:33.308303	0	Hi
6	122	556b42f2e13823404953bbb9	2015-06-03 16:40:31.124313	5	Hi you too
7	122	556b3b1ce1382331efae3f60	2015-06-03 16:46:14.176086	0	retretret
8	122	556b3bdae1382331efae3f71	2015-06-03 16:46:40.037297	0	dfg
\.


--
-- Name: blunder_comments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('blunder_comments_id_seq', 8, true);


--
-- Data for Name: blunder_comments_votes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY blunder_comments_votes (id, user_id, comment_id, assign_date, vote) FROM stdin;
12	121	1	2015-06-03 15:25:31.203489	1
14	122	5	2015-06-03 16:40:20.916752	1
\.


--
-- Name: blunder_comments_votes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('blunder_comments_votes_id_seq', 14, true);


--
-- Data for Name: blunder_favorites; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY blunder_favorites (id, user_id, blunder_id, assign_date) FROM stdin;
22	120	556b4292e13823404953bbaf	2015-06-01 20:57:44.605283
23	120	556b43f5e13823404953bbd6	2015-06-01 20:57:54.842294
25	120	556b43fce13823404953bbd7	2015-06-01 21:49:19.905517
26	120	556b3aa7e1382331efae3f53	2015-06-01 21:49:31.639267
27	120	556b3ae4e1382331efae3f59	2015-06-01 21:50:13.73623
28	120	556b3b9be1382331efae3f6b	2015-06-01 21:50:45.421789
29	120	556b4274e13823404953bbad	2015-06-01 21:50:48.663275
30	120	556b432be13823404953bbc0	2015-06-01 21:50:52.583251
31	120	556b3acbe1382331efae3f57	2015-06-01 21:50:56.237807
33	120	556b3ab8e1382331efae3f55	2015-06-03 16:33:48.194497
34	122	556b42f2e13823404953bbb9	2015-06-03 16:40:41.606013
35	122	556b3bdae1382331efae3f71	2015-06-03 16:46:41.238796
\.


--
-- Name: blunder_favorites_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('blunder_favorites_id_seq', 35, true);


--
-- Data for Name: blunder_history; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY blunder_history (id, user_id, blunder_id, result, user_elo, blunder_elo, date, user_line) FROM stdin;
124	122	556b42f2e13823404953bbb9	0	1387	1472	2015-06-03 16:40:45.2554	{Qg6+}
126	122	556b3be3e1382331efae3f72	0	1375	1700	2015-06-03 16:40:49.833206	{Rc2}
128	122	556b3b91e1382331efae3f6a	0	1371	1300	2015-06-03 16:40:52.957282	{Kg5}
130	122	556b3b1ce1382331efae3f60	0	1349	1300	2015-06-03 16:46:25.286887	{Qe2}
125	122	556b3b16e1382331efae3f5f	0	1375	2100	2015-06-03 16:40:47.288974	{b4}
127	122	556b3b34e1382331efae3f62	0	1371	2700	2015-06-03 16:40:51.85562	{Ne4}
129	122	556b3a2de1382331efae3f46	0	1352	1722	2015-06-03 16:46:09.060735	{Kd8,f6}
131	122	556b3bdae1382331efae3f71	0	1331	1300	2015-06-03 16:46:35.2008	{Qe3+,Rf2}
121	122	556b3ae4e1382331efae3f59	0	1429	1530	2015-06-03 16:40:04.939738	{Qg4,Bf3}
122	122	556b43fce13823404953bbd7	0	1418	1553	2015-06-03 16:40:10.682445	{Ke1,Nc2+}
123	122	556b3380e138232acf525083	0	1408	1300	2015-06-03 16:40:15.589286	{Kb6,Nc4+}
\.


--
-- Name: blunder_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('blunder_history_id_seq', 131, true);


--
-- Data for Name: blunder_tasks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY blunder_tasks (id, user_id, blunder_id, assign_date) FROM stdin;
154	120	556b433fe13823404953bbc3	2015-06-03 16:46:59.429778
\.


--
-- Name: blunder_tasks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('blunder_tasks_id_seq', 154, true);


--
-- Data for Name: blunder_votes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY blunder_votes (id, blunder_id, assign_date, vote, user_id) FROM stdin;
13	556b43b0e13823404953bbcf	2015-06-03 16:33:32.357754	-1	120
14	556b42f2e13823404953bbb9	2015-06-03 16:40:43.12862	1	122
15	556b3b1ce1382331efae3f60	2015-06-03 16:46:16.41893	1	122
\.


--
-- Name: blunder_votes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('blunder_votes_id_seq', 15, true);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY users (id, username, password, role, registration, last_login, elo, email, salt) FROM stdin;
121	Failuref	$2a$12$pXj7c8krKAGjM2dGLO6UoubtDLHKVNy4eQL/R9FvawhimxaVwwRsa	0	2015-05-28 03:25:05.64194	2015-06-01 19:37:10.166601	1671	chezstov@gmail.com	$2a$12$pXj7c8krKAGjM2dGLO6Uou
122	demo	$2a$12$cqwAprmH0bZYi/J2pWnVSeiGZcvA4u9KKbuK40EN30I//zNPZA6.a	3	2015-06-03 16:38:04.173926	2015-06-03 16:38:04.569265	1314		$2a$12$cqwAprmH0bZYi/J2pWnVSe
120	JackalSh	$2a$12$2lOJlAl0eLr8DqyId6236.1ZGbFhTgIel79qUoAxbj0.nLQoiOwmC	0	2015-05-28 03:24:31.500694	2015-06-03 16:46:58.842631	1239	jackalsh@gmail.com	$2a$12$2lOJlAl0eLr8DqyId6236.
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

