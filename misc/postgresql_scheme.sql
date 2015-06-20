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
    spent_time integer NOT NULL,
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
-- Name: blunder_task_type; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE blunder_task_type (
    id integer NOT NULL,
    name character varying(20) NOT NULL
);


ALTER TABLE blunder_task_type OWNER TO postgres;

--
-- Name: blunder_task_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE blunder_task_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE blunder_task_type_id_seq OWNER TO postgres;

--
-- Name: blunder_task_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE blunder_task_type_id_seq OWNED BY blunder_task_type.id;


--
-- Name: blunder_tasks; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE blunder_tasks (
    id integer NOT NULL,
    user_id integer NOT NULL,
    blunder_id character varying(255) NOT NULL,
    assign_date timestamp without time zone DEFAULT now() NOT NULL,
    type_id integer NOT NULL
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

ALTER TABLE ONLY blunder_task_type ALTER COLUMN id SET DEFAULT nextval('blunder_task_type_id_seq'::regclass);


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
\.


--
-- Name: blunder_comments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('blunder_comments_id_seq', 26, true);


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
44	121	557a18bde13823b8223a01b2	2015-06-20 05:01:58.364809
\.


--
-- Name: blunder_favorites_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('blunder_favorites_id_seq', 44, true);


--
-- Data for Name: blunder_history; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY blunder_history (id, user_id, blunder_id, result, user_elo, blunder_elo, user_line, date_start, date_finish, spent_time) FROM stdin;
209	121	55768f0283878c17d7ab5a5a	0	1607	1726	{Kg8}	2015-06-18 01:09:57.410498	2015-06-18 01:09:58.516172	1
210	121	5576923683878c17d7ab5aa3	0	1596	1434	{Kf8}	2015-06-18 01:09:58.787269	2015-06-18 01:10:26.60509	6
211	121	55764e0e83878c17d7ab551a	0	1573	1395	{Kxg5,c3}	2015-06-18 01:10:26.813931	2015-06-18 01:16:03.785586	337
212	120	5576f00883878c2ef4695864	1	1164	1366		2015-06-19 15:29:03.979606	2015-06-19 15:29:31.24835	27
213	120	55772d9c83878c2ef4695d8d	0	1188	1397	{Kc4,b5+}	2015-06-19 15:29:37.066097	2015-06-19 15:29:53.927551	17
214	120	55769d8b83878c17d7ab5ba3	0	1181	1762	{Nf6,Bg5}	2015-06-19 15:30:10.234903	2015-06-19 15:30:23.946638	13
215	120	5576c5e683878c17d7ab5f1b	0	1180	1300	{g4,d7}	2015-06-19 15:30:36.287644	2015-06-19 15:31:23.468829	47
216	120	5576bea183878c17d7ab5e7c	0	1169	1487	{Bc8,Qd4+}	2015-06-19 15:31:33.980912	2015-06-19 15:32:28.286626	54
217	120	5576ba4e83878c17d7ab5e1e	1	1165	1576		2015-06-19 15:32:38.448278	2015-06-19 15:33:08.47908	30
218	120	5577169183878c2ef4695b9c	0	1194	1395	{Ne4,Nxe4}	2015-06-19 15:33:12.034161	2015-06-19 15:33:17.707192	5
219	120	5576625b83878c17d7ab56a1	0	1186	1958	{Nbc5}	2015-06-19 15:33:35.252773	2015-06-19 15:51:10.970604	1056
220	120	5576c55583878c17d7ab5f0c	1	1186	1400		2015-06-19 15:51:11.301601	2015-06-19 15:51:42.936378	31
221	120	5576b8a283878c17d7ab5df7	0	1211	1495	{Rd1,Re1+,Rxe1,Bxf3,g5,Bd4+}	2015-06-19 15:51:47.491429	2015-06-19 15:53:09.826366	46
222	120	5576998983878c17d7ab5b48	0	1206	1590	{h6,Ne8+}	2015-06-19 15:53:34.97023	2015-06-19 15:55:03.210331	88
223	120	55767a3e83878c17d7ab58a0	0	1203	1540	{Bg7,Rxg7+}	2015-06-19 15:55:24.146625	2015-06-19 15:56:17.012246	53
224	120	5576634b83878c17d7ab56b6	0	1199	1533	{Rxd2,Qd3}	2015-06-19 15:56:29.273116	2015-06-19 16:26:21.931093	4
225	121	557893b5e13823b830f5587d	0	1549	1542	{Kg7,Qg5}	2015-06-20 04:18:15.947978	2015-06-20 04:18:19.489947	3
226	121	55792641e13823b83bff78ec	0	1533	1941	{Ne8,Nd7}	2015-06-20 04:18:22.643078	2015-06-20 04:18:25.15424	2
227	121	55793ab8e13823b838fcc76d	0	1530	2261	{Rxe4,Rxe4}	2015-06-20 04:18:26.784488	2015-06-20 04:18:29.942382	3
228	121	5579e87de13823b81d81ea65	0	1530	1408	{Nc6,Qxc6}	2015-06-20 04:18:33.891935	2015-06-20 04:18:36.295999	2
229	121	55797d2ee13823b82239eb93	0	1509	1563	{Rf7,exf6}	2015-06-20 04:18:39.986528	2015-06-20 04:18:42.854373	3
230	121	55798e11e13823b828eb3776	0	1495	1561	{h5,Ra2}	2015-06-20 04:18:45.350302	2015-06-20 04:18:50.384519	5
231	121	5579a6fbe13823b8361c8c89	0	1482	1360	{Bc4,Rd4}	2015-06-20 04:19:06.500131	2015-06-20 04:19:09.090824	2
232	121	55796311e13823b83fd87f7d	0	1461	2095	{Bxe2,Bd2}	2015-06-20 04:19:11.214848	2015-06-20 04:19:13.907312	2
233	121	557a5797e13823b83d9486f5	0	1460	1731	{b6,Qc6+}	2015-06-20 04:19:17.132132	2015-06-20 04:19:20.347551	3
234	121	557ab1cfe13823b838fcfca3	0	1454	1336	{Rae8}	2015-06-20 04:20:49.795319	2015-06-20 04:20:53.321938	3
235	121	5578d6eee13823b829cd9304	0	1433	1621	{Rhh2}	2015-06-20 04:20:53.875247	2015-06-20 04:20:55.02941	1
236	121	5578a7c0e13823b83eab8fd2	0	1425	1670	{Nd7}	2015-06-20 04:20:55.503988	2015-06-20 04:20:56.755875	1
237	121	5579a89ce13823b81d81e147	0	1419	1737	{Ke1}	2015-06-20 04:20:57.40469	2015-06-20 04:20:59.569346	2
238	121	55785d7be13823b834829d15	0	1415	1780	{Rxd3,Nf6+,Kh8,Bg5}	2015-06-20 04:21:26.51556	2015-06-20 04:23:02.410178	94
239	121	5578b4e1e13823b83bff68bf	0	1412	1303	{Kg3,e2}	2015-06-20 04:23:15.18516	2015-06-20 04:23:33.759544	18
240	121	5579d759e13823b830f58682	0	1391	1721	{Ne6}	2015-06-20 04:23:42.027516	2015-06-20 04:23:44.51133	2
241	121	557a5519e13823b8398a2725	0	1387	1201	{c6}	2015-06-20 04:23:45.554221	2015-06-20 04:23:46.243437	0
242	121	5579948ce13823b829cdadf5	0	1363	1688	{Qxf5}	2015-06-20 04:23:46.904766	2015-06-20 04:23:49.081093	2
243	121	5578caf6e13823b82239d23e	0	1359	1719	{Rd6}	2015-06-20 04:23:49.41503	2015-06-20 04:23:50.702948	1
244	121	55799c67e13823b8398a0cd9	0	1355	1865	{Bxe5+}	2015-06-20 04:23:51.253411	2015-06-20 04:23:53.384536	2
245	121	557abe6ce13823b82b9ba72f	0	1353	1333	{Kh2}	2015-06-20 04:23:54.750031	2015-06-20 04:24:04.266426	9
246	121	557872ace13823b833298c3c	0	1336	1323	{Rf1}	2015-06-20 04:24:04.943524	2015-06-20 04:24:27.886455	22
247	121	557aa8b1e13823b825318277	0	1319	1384	{Kf3,Ne5+}	2015-06-20 04:24:29.18951	2015-06-20 04:24:44.110835	15
248	121	5578a494e13823b83eab8f5f	0	1306	1508	{Rc1,Re3}	2015-06-20 04:24:57.196288	2015-06-20 04:25:18.375669	21
249	121	55789ed7e13823b8361c6717	0	1298	3167	{bxa3}	2015-06-20 05:01:40.393395	2015-06-20 05:01:47.612674	7
250	121	55786214e13823b83fd85b00	0	1298	1545	{Rd7}	2015-06-20 05:01:48.145709	2015-06-20 05:01:49.6624	1
251	121	5578d270e13823b82a777707	0	1292	1262	{Re8}	2015-06-20 05:01:50.429044	2015-06-20 05:01:51.363565	1
252	121	557a18bde13823b8223a01b2	0	1275	1500	{Rb4}	2015-06-20 05:01:55.776589	2015-06-20 05:02:06.517562	10
253	121	55794a7fe13823b82239e463	0	1268	1425	{Kd5}	2015-06-20 06:26:43.597452	2015-06-20 06:26:46.448497	2
254	121	557907dde13823b83fd8728e	0	1259	2191	{h4}	2015-06-20 06:26:50.446827	2015-06-20 06:26:51.157634	0
255	121	5578d093e13823b821717c0d	0	1259	1433	{Nc5}	2015-06-20 06:26:53.557241	2015-06-20 06:27:00.189035	6
256	121	557a6267e13823b81c3e0b1e	0	1250	1303	{Bh4}	2015-06-20 06:27:18.439461	2015-06-20 06:27:46.759446	26
257	121	5579cee9e13823b818db4fd1	0	1236	1443	{Qh2+}	2015-06-20 06:27:55.088864	2015-06-20 06:28:02.640116	6
258	121	5578c932e13823b82b9b5ff5	0	1229	1323	{Bxa4}	2015-06-20 06:39:33.168024	2015-06-20 06:39:33.932853	0
\.


--
-- Name: blunder_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('blunder_history_id_seq', 258, true);


--
-- Data for Name: blunder_task_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY blunder_task_type (id, name) FROM stdin;
1	explore
2	rated
\.


--
-- Name: blunder_task_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('blunder_task_type_id_seq', 2, true);


--
-- Data for Name: blunder_tasks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY blunder_tasks (id, user_id, blunder_id, assign_date, type_id) FROM stdin;
297	121	557a86e4e13823b826e6fcf8	2015-06-20 06:39:42.436334	2
298	140	5578c266e13823b81b5aef5c	2015-06-20 07:32:35.329009	2
299	141	5578e9c2e13823b824cbbc6f	2015-06-20 07:36:44.465791	2
300	142	5578fa1ce13823b8361c73f5	2015-06-20 07:49:48.967675	2
301	143	5578b11ae13823b83fd86634	2015-06-20 08:01:55.546512	2
302	144	557963bbe13823b8361c82fd	2015-06-20 08:26:42.953315	2
237	121	557715a883878c2ef4695b89	2015-06-18 01:16:20.888432	2
303	145	557a1d07e13823b825316eb8	2015-06-20 10:33:50.545918	2
251	121	5578bf52e13823b829cd8fa5	2015-06-19 22:21:19.536543	2
252	121	5578ed5fe13823b826e6c2d0	2015-06-19 22:21:35.000096	2
253	121	5579d52be13823b82b9b8616	2015-06-20 03:29:46.228397	2
260	121	5579c53fe13823b824cbdb91	2015-06-20 04:18:53.025934	2
264	121	557a6d88e13823b8223a0dd0	2015-06-20 04:19:25.388217	2
269	121	557a63d8e13823b82b9b9a45	2015-06-20 04:21:00.222456	2
281	121	5579a32ce13823b832e27faf	2015-06-20 04:29:03.099535	2
282	121	557a7452e13823b83cd6dd04	2015-06-20 04:35:13.042286	2
283	121	5578b315e13823b83a9780d5	2015-06-20 05:01:27.592791	2
288	121	55791796e13823b83cd6ab4d	2015-06-20 05:02:07.637122	2
289	121	55786805e13823b82a7767dc	2015-06-20 06:00:58.217014	2
295	121	557a6c56e13823b832e29c46	2015-06-20 06:28:09.801776	2
\.


--
-- Name: blunder_tasks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('blunder_tasks_id_seq', 303, true);


--
-- Data for Name: blunder_votes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY blunder_votes (id, blunder_id, assign_date, vote, user_id) FROM stdin;
24	557a18bde13823b8223a01b2	2015-06-20 05:02:01.263359	1	121
25	55786805e13823b82a7767dc	2015-06-20 06:01:00.462385	1	121
\.


--
-- Name: blunder_votes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('blunder_votes_id_seq', 25, true);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY users (id, username, password, role, registration, last_login, elo, email, salt) FROM stdin;
120	JackalSh	$2a$12$2lOJlAl0eLr8DqyId6236.1ZGbFhTgIel79qUoAxbj0.nLQoiOwmC	0	2015-05-28 03:24:31.500694	2015-06-19 15:29:03.427196	1195	jackalsh@gmail.com	$2a$12$2lOJlAl0eLr8DqyId6236.
122	demo	$2a$12$cqwAprmH0bZYi/J2pWnVSeiGZcvA4u9KKbuK40EN30I//zNPZA6.a	3	2015-06-03 16:38:04.173926	2015-06-18 15:25:38.116715	1291		$2a$12$cqwAprmH0bZYi/J2pWnVSe
121	Failuref	$2a$12$pXj7c8krKAGjM2dGLO6UoubtDLHKVNy4eQL/R9FvawhimxaVwwRsa	0	2015-05-28 03:25:05.64194	2015-06-20 10:30:44.936375	1217	chezstov@gmail.com	$2a$12$pXj7c8krKAGjM2dGLO6Uou
123	aba	$2a$12$LGstAiTN/CF587nakaOAEO2A9zzKQAFtypjKk1h3/4Y0fftat4/iO	3	2015-06-18 17:29:41.601927	2015-06-18 17:29:42.025593	1500		$2a$12$LGstAiTN/CF587nakaOAEO
140	1dsadsa	$2a$12$yGqPKHXPFWTtLeXKgWAGF.7meFxCW.roXQz6bSIPPhrT3UUjGibka	3	2015-06-20 07:32:22.043547	2015-06-20 07:32:22.626799	1500		$2a$12$yGqPKHXPFWTtLeXKgWAGF.
141	bab4324	$2a$12$xoMjie/80Pnbxz3ZsCbt.OB6sF6oM6KQGWfZ.dXhkgqugpwpeV7wq	3	2015-06-20 07:36:42.838293	2015-06-20 07:36:43.310381	1500		$2a$12$xoMjie/80Pnbxz3ZsCbt.O
142	%$$$@#@!	$2a$12$lEpjY.WLWvovOZwTMASKaeIfwa5QD5D15KjeteTz6SHvc8kOCLZs2	3	2015-06-20 07:49:45.344091	2015-06-20 07:49:45.791405	1500	me@gmail.com	$2a$12$lEpjY.WLWvovOZwTMASKae
143	$$megaraper$$	$2a$12$r/wJLdzfqc8IMw1ZO61uFOenJIPLBJkoFKKjdu2ZkfcC0fM6LNHBO	3	2015-06-20 08:01:52.960232	2015-06-20 08:01:53.499483	1500	a-1-0-0@gmail.com	$2a$12$r/wJLdzfqc8IMw1ZO61uFO
144	meagdsads	$2a$12$2nZQ7JeDwYgp3RItPhoifukZIJydAsvQan.XAStNqbmJ17Dit24xu	3	2015-06-20 08:26:36.709588	2015-06-20 08:26:37.236817	1500		$2a$12$2nZQ7JeDwYgp3RItPhoifu
145	Username	$2a$12$bOb8aB.UNsqoFkqQ5ngsFeZ0PukDLPIbmlWTst5aG6bLf42UMZGGu	3	2015-06-20 10:33:49.263593	2015-06-20 10:33:49.712924	1500		$2a$12$bOb8aB.UNsqoFkqQ5ngsFe
\.


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('users_id_seq', 145, true);


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
-- Name: blunder_task_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY blunder_task_type
    ADD CONSTRAINT blunder_task_type_pkey PRIMARY KEY (id);


--
-- Name: blunder_tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY blunder_tasks
    ADD CONSTRAINT blunder_tasks_pkey PRIMARY KEY (id);


--
-- Name: blunder_tasks_user_id_type_id_blunder_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY blunder_tasks
    ADD CONSTRAINT blunder_tasks_user_id_type_id_blunder_id_key UNIQUE (user_id, type_id, blunder_id);


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
-- Name: blunder_tasks_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY blunder_tasks
    ADD CONSTRAINT blunder_tasks_type_id_fkey FOREIGN KEY (type_id) REFERENCES blunder_task_type(id);


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

