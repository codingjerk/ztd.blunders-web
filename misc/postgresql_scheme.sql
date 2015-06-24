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
    blunder_id character(24) NOT NULL,
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
    blunder_id character(24) NOT NULL,
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
    blunder_id character(24) NOT NULL,
    result integer NOT NULL,
    user_elo integer NOT NULL,
    blunder_elo integer NOT NULL,
    user_line text NOT NULL,
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
    name text NOT NULL
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
    blunder_id character(24) NOT NULL,
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
    blunder_id character(24) NOT NULL,
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
    username text NOT NULL,
    password text NOT NULL,
    role integer NOT NULL,
    registration timestamp without time zone NOT NULL,
    last_login timestamp without time zone NOT NULL,
    elo integer DEFAULT 1500 NOT NULL,
    email text DEFAULT ''::character varying NOT NULL,
    salt text NOT NULL
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
-- Name: vw_activities; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW vw_activities AS
 SELECT act.id AS user_id,
    max(act.date_finish) AS last_activity
   FROM ( SELECT blunder_history.id,
            blunder_history.date_finish
           FROM blunder_history
        UNION
         SELECT users.id,
            users.last_login
           FROM users
        UNION
         SELECT blunder_favorites.user_id,
            blunder_favorites.assign_date
           FROM blunder_favorites
        UNION
         SELECT blunder_votes.user_id,
            blunder_votes.assign_date
           FROM blunder_votes
        UNION
         SELECT blunder_comments.user_id,
            blunder_comments.date
           FROM blunder_comments
        UNION
         SELECT blunder_comments_votes.user_id,
            blunder_comments_votes.assign_date
           FROM blunder_comments_votes) act
  GROUP BY act.id;


ALTER TABLE vw_activities OWNER TO postgres;

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

SELECT pg_catalog.setval('blunder_comments_id_seq', 33, true);


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
\.


--
-- Name: blunder_favorites_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('blunder_favorites_id_seq', 69, true);


--
-- Data for Name: blunder_history; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY blunder_history (id, user_id, blunder_id, result, user_elo, blunder_elo, user_line, date_start, date_finish, spent_time) FROM stdin;
\.


--
-- Name: blunder_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('blunder_history_id_seq', 295, true);


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
\.


--
-- Name: blunder_tasks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('blunder_tasks_id_seq', 344, true);


--
-- Data for Name: blunder_votes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY blunder_votes (id, blunder_id, assign_date, vote, user_id) FROM stdin;
\.


--
-- Name: blunder_votes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('blunder_votes_id_seq', 31, true);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY users (id, username, password, role, registration, last_login, elo, email, salt) FROM stdin;
122	demo	$2a$12$cqwAprmH0bZYi/J2pWnVSeiGZcvA4u9KKbuK40EN30I//zNPZA6.a	3	2015-06-03 16:38:04.173926	2015-06-21 16:38:27.589153	1268		$2a$12$cqwAprmH0bZYi/J2pWnVSe
120	JackalSh	$2a$12$2lOJlAl0eLr8DqyId6236.1ZGbFhTgIel79qUoAxbj0.nLQoiOwmC	0	2015-05-28 03:24:31.500694	2015-06-24 17:44:23.074658	1293	jackalsh@gmail.com	$2a$12$2lOJlAl0eLr8DqyId6236.
124	Username	$2b$12$9n/1YKYiFpgDLwjyoM.BXuhNCxWJutEUtUGe111.G8t2O/64EdWe.	3	2015-06-21 17:09:19.804923	2015-06-21 17:09:20.281245	1500		$2b$12$9n/1YKYiFpgDLwjyoM.BXu
121	Failuref	$2a$12$pXj7c8krKAGjM2dGLO6UoubtDLHKVNy4eQL/R9FvawhimxaVwwRsa	0	2015-05-28 03:25:05.64194	2015-06-23 12:14:11.988801	1324	chezstov@gmail.com	$2a$12$pXj7c8krKAGjM2dGLO6Uou
\.


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('users_id_seq', 124, true);


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

