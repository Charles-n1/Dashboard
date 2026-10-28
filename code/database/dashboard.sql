--
-- PostgreSQL database dump
--

\restrict crNs0LZ41pO8tadZAh83Hxcdqg2E6fx9DndLyE0o3c7a2BmxEYDDTbLhs4f2eTw

-- Dumped from database version 17.11 (Debian 17.11-1.pgdg13+2)
-- Dumped by pg_dump version 17.11 (Debian 17.11-1.pgdg13+2)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: dashing
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO dashing;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: dashing
--

COMMENT ON SCHEMA public IS '';


--
-- Name: set_updated_at(); Type: FUNCTION; Schema: public; Owner: dashing
--

CREATE FUNCTION public.set_updated_at() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.updated_at := CURRENT_DATE;
    RETURN NEW;
END;
$$;


ALTER FUNCTION public.set_updated_at() OWNER TO dashing;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: cell; Type: TABLE; Schema: public; Owner: dashing
--

CREATE TABLE public.cell (
    id integer NOT NULL,
    grid_id integer NOT NULL,
    widget_type character varying(512) NOT NULL,
    widget_id character varying(128) NOT NULL,
    x integer NOT NULL,
    y integer NOT NULL,
    width integer DEFAULT 1 NOT NULL,
    height integer DEFAULT 1 NOT NULL
);


ALTER TABLE public.cell OWNER TO dashing;

--
-- Name: cell_id_seq; Type: SEQUENCE; Schema: public; Owner: dashing
--

CREATE SEQUENCE public.cell_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cell_id_seq OWNER TO dashing;

--
-- Name: cell_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dashing
--

ALTER SEQUENCE public.cell_id_seq OWNED BY public.cell.id;


--
-- Name: discord; Type: TABLE; Schema: public; Owner: dashing
--

CREATE TABLE public.discord (
    primary_id integer NOT NULL,
    id bigint NOT NULL,
    username character varying(256) NOT NULL,
    global_name character varying(256) NOT NULL,
    email character varying(256) NOT NULL,
    avatar character varying(256) NOT NULL,
    user_id integer NOT NULL,
    hashed_token character varying(1024) NOT NULL
);


ALTER TABLE public.discord OWNER TO dashing;

--
-- Name: discord_primary_id_seq; Type: SEQUENCE; Schema: public; Owner: dashing
--

CREATE SEQUENCE public.discord_primary_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.discord_primary_id_seq OWNER TO dashing;

--
-- Name: discord_primary_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dashing
--

ALTER SEQUENCE public.discord_primary_id_seq OWNED BY public.discord.primary_id;


--
-- Name: grid; Type: TABLE; Schema: public; Owner: dashing
--

CREATE TABLE public.grid (
    id integer NOT NULL,
    user_id integer NOT NULL,
    columns integer DEFAULT 13 NOT NULL,
    rows integer DEFAULT 6 NOT NULL
);


ALTER TABLE public.grid OWNER TO dashing;

--
-- Name: grid_id_seq; Type: SEQUENCE; Schema: public; Owner: dashing
--

CREATE SEQUENCE public.grid_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.grid_id_seq OWNER TO dashing;

--
-- Name: grid_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dashing
--

ALTER SEQUENCE public.grid_id_seq OWNED BY public.grid.id;


--
-- Name: log; Type: TABLE; Schema: public; Owner: dashing
--

CREATE TABLE public.log (
    id integer NOT NULL,
    type character varying(64) NOT NULL,
    message character varying(1024) NOT NULL,
    user_id integer NOT NULL,
    created_on date NOT NULL
);


ALTER TABLE public.log OWNER TO dashing;

--
-- Name: log_id_seq; Type: SEQUENCE; Schema: public; Owner: dashing
--

CREATE SEQUENCE public.log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.log_id_seq OWNER TO dashing;

--
-- Name: log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dashing
--

ALTER SEQUENCE public.log_id_seq OWNED BY public.log.id;


--
-- Name: steam; Type: TABLE; Schema: public; Owner: dashing
--

CREATE TABLE public.steam (
    primary_id integer NOT NULL,
    user_id integer NOT NULL,
    steam_id bigint NOT NULL
);


ALTER TABLE public.steam OWNER TO dashing;

--
-- Name: steam_primary_id_seq; Type: SEQUENCE; Schema: public; Owner: dashing
--

CREATE SEQUENCE public.steam_primary_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.steam_primary_id_seq OWNER TO dashing;

--
-- Name: steam_primary_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dashing
--

ALTER SEQUENCE public.steam_primary_id_seq OWNED BY public.steam.primary_id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: dashing
--

CREATE TABLE public."user" (
    password_hash character varying(1024) NOT NULL,
    id integer NOT NULL,
    username character varying(256) NOT NULL,
    email character varying(1024) NOT NULL,
    first_name character varying(256),
    last_name character varying(256),
    created_at date DEFAULT now() NOT NULL,
    updated_at date DEFAULT now() NOT NULL,
    status character varying(64) DEFAULT 'active'::character varying NOT NULL,
    is_admin boolean DEFAULT false NOT NULL
);


ALTER TABLE public."user" OWNER TO dashing;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: dashing
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_id_seq OWNER TO dashing;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dashing
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- Name: cell id; Type: DEFAULT; Schema: public; Owner: dashing
--

ALTER TABLE ONLY public.cell ALTER COLUMN id SET DEFAULT nextval('public.cell_id_seq'::regclass);


--
-- Name: discord primary_id; Type: DEFAULT; Schema: public; Owner: dashing
--

ALTER TABLE ONLY public.discord ALTER COLUMN primary_id SET DEFAULT nextval('public.discord_primary_id_seq'::regclass);


--
-- Name: grid id; Type: DEFAULT; Schema: public; Owner: dashing
--

ALTER TABLE ONLY public.grid ALTER COLUMN id SET DEFAULT nextval('public.grid_id_seq'::regclass);


--
-- Name: log id; Type: DEFAULT; Schema: public; Owner: dashing
--

ALTER TABLE ONLY public.log ALTER COLUMN id SET DEFAULT nextval('public.log_id_seq'::regclass);


--
-- Name: steam primary_id; Type: DEFAULT; Schema: public; Owner: dashing
--

ALTER TABLE ONLY public.steam ALTER COLUMN primary_id SET DEFAULT nextval('public.steam_primary_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: dashing
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- Data for Name: cell; Type: TABLE DATA; Schema: public; Owner: dashing
--

COPY public.cell (id, grid_id, widget_type, widget_id, x, y) FROM stdin;
\.


--
-- Data for Name: discord; Type: TABLE DATA; Schema: public; Owner: dashing
--

COPY public.discord (primary_id, id, username, global_name, email, avatar, user_id, hashed_token) FROM stdin;
\.


--
-- Data for Name: grid; Type: TABLE DATA; Schema: public; Owner: dashing
--

COPY public.grid (id, user_id) FROM stdin;
\.


--
-- Data for Name: log; Type: TABLE DATA; Schema: public; Owner: dashing
--

COPY public.log (id, type, message, user_id, created_on) FROM stdin;
\.


--
-- Data for Name: steam; Type: TABLE DATA; Schema: public; Owner: dashing
--

COPY public.steam (primary_id, user_id, steam_id) FROM stdin;
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: dashing
--

COPY public."user" (password_hash, id, username, email, first_name, last_name, created_at, updated_at, status, is_admin) FROM stdin;
pbkdf2_sha256$600000$56b994123697dfa22cba013d673de62c$a7440b55d9b62bac5b665afc991bb2a0a1f88ef106b04305fb72b8ecc6746635	55	gay	comegirod233@gmail.com	Côme	Girod	2026-10-05	2026-10-05	active	f
pbkdf2_sha256$600000$146553283ac547f68da31861bc8b0b51$48ccf8edd94d536aaf451f684f653c2ce579d2ee030765ac244ef2226a19db4a	54	efefezvf	ok@gmail.com	ok@gmail.com	ok@gmail.com	2026-10-02	2026-10-06	active	f
\.


--
-- Name: cell_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dashing
--

SELECT pg_catalog.setval('public.cell_id_seq', 1, false);


--
-- Name: discord_primary_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dashing
--

SELECT pg_catalog.setval('public.discord_primary_id_seq', 5, true);


--
-- Name: grid_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dashing
--

SELECT pg_catalog.setval('public.grid_id_seq', 1, false);


--
-- Name: log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dashing
--

SELECT pg_catalog.setval('public.log_id_seq', 1, false);


--
-- Name: steam_primary_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dashing
--

SELECT pg_catalog.setval('public.steam_primary_id_seq', 1, false);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dashing
--

SELECT pg_catalog.setval('public.user_id_seq', 56, true);


--
-- Name: cell cell_pkey; Type: CONSTRAINT; Schema: public; Owner: dashing
--

ALTER TABLE ONLY public.cell
    ADD CONSTRAINT cell_pkey PRIMARY KEY (id);


--
-- Name: discord discord_external_id_unique; Type: CONSTRAINT; Schema: public; Owner: dashing
--

ALTER TABLE ONLY public.discord
    ADD CONSTRAINT discord_external_id_unique UNIQUE (id);


--
-- Name: discord discord_pkey; Type: CONSTRAINT; Schema: public; Owner: dashing
--

ALTER TABLE ONLY public.discord
    ADD CONSTRAINT discord_pkey PRIMARY KEY (primary_id);


--
-- Name: grid grid_pkey; Type: CONSTRAINT; Schema: public; Owner: dashing
--

ALTER TABLE ONLY public.grid
    ADD CONSTRAINT grid_pkey PRIMARY KEY (id);


--
-- Name: log log_pkey; Type: CONSTRAINT; Schema: public; Owner: dashing
--

ALTER TABLE ONLY public.log
    ADD CONSTRAINT log_pkey PRIMARY KEY (id);


--
-- Name: steam steam_pkey; Type: CONSTRAINT; Schema: public; Owner: dashing
--

ALTER TABLE ONLY public.steam
    ADD CONSTRAINT steam_pkey PRIMARY KEY (primary_id);


--
-- Name: user user_email_unique; Type: CONSTRAINT; Schema: public; Owner: dashing
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_email_unique UNIQUE (email);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: dashing
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: user user_username_unique; Type: CONSTRAINT; Schema: public; Owner: dashing
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_username_unique UNIQUE (username);


--
-- Name: user trg_user_set_updated_at; Type: TRIGGER; Schema: public; Owner: dashing
--

CREATE TRIGGER trg_user_set_updated_at BEFORE UPDATE ON public."user" FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();


--
-- Name: cell grid_fk; Type: FK CONSTRAINT; Schema: public; Owner: dashing
--

ALTER TABLE ONLY public.cell
    ADD CONSTRAINT grid_fk FOREIGN KEY (grid_id) REFERENCES public.grid(id);


--
-- Name: discord user_fk; Type: FK CONSTRAINT; Schema: public; Owner: dashing
--

ALTER TABLE ONLY public.discord
    ADD CONSTRAINT user_fk FOREIGN KEY (user_id) REFERENCES public."user"(id) NOT VALID;


--
-- Name: grid user_fk; Type: FK CONSTRAINT; Schema: public; Owner: dashing
--

ALTER TABLE ONLY public.grid
    ADD CONSTRAINT user_fk FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: log user_fk; Type: FK CONSTRAINT; Schema: public; Owner: dashing
--

ALTER TABLE ONLY public.log
    ADD CONSTRAINT user_fk FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: steam user_fk; Type: FK CONSTRAINT; Schema: public; Owner: dashing
--

ALTER TABLE ONLY public.steam
    ADD CONSTRAINT user_fk FOREIGN KEY (user_id) REFERENCES public."user"(id) NOT VALID;


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: dashing
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;


--
-- PostgreSQL database dump complete
--

\unrestrict crNs0LZ41pO8tadZAh83Hxcdqg2E6fx9DndLyE0o3c7a2BmxEYDDTbLhs4f2eTw
