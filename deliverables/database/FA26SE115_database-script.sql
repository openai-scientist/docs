-- FA26SE115 database script (PostgreSQL 16), schema only.
-- Generated 2026-10-29: Alembic migrations of logos/services/management applied up to revision 20261022_0048, then pg_dump --schema-only --no-owner --no-privileges.
-- Contains no data and no secrets.

--
-- PostgreSQL database dump
--



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
-- Name: pg_trgm; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pg_trgm WITH SCHEMA public;


--
-- Name: EXTENSION pg_trgm; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION pg_trgm IS 'text similarity measurement and index searching based on trigrams';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


--
-- Name: audit_events; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.audit_events (
    id uuid NOT NULL,
    actor_user_id uuid,
    action character varying(100) NOT NULL,
    resource_type character varying(80) NOT NULL,
    resource_id character varying(64) NOT NULL,
    project_id uuid,
    request_id character varying(64),
    details json DEFAULT '{}'::json NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: auth_sessions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_sessions (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    token_digest character varying(64) NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    last_seen_at timestamp with time zone NOT NULL,
    idle_expires_at timestamp with time zone NOT NULL,
    absolute_expires_at timestamp with time zone NOT NULL,
    revoked_at timestamp with time zone
);


--
-- Name: comments; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.comments (
    id uuid NOT NULL,
    run_id uuid NOT NULL,
    artifact_id uuid,
    author_user_id uuid NOT NULL,
    body text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    edited_at timestamp with time zone,
    deleted_at timestamp with time zone
);


--
-- Name: cost_entries; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cost_entries (
    id uuid NOT NULL,
    project_id uuid NOT NULL,
    run_id uuid NOT NULL,
    source character varying(16) NOT NULL,
    source_id uuid NOT NULL,
    source_key character varying(200) NOT NULL,
    role character varying(20),
    provider character varying(32),
    model character varying(200),
    input_tokens bigint NOT NULL,
    output_tokens bigint NOT NULL,
    occurred_at timestamp with time zone NOT NULL,
    CONSTRAINT ck_cost_entries_source CHECK (((source)::text = ANY ((ARRAY['stage'::character varying, 'consultation'::character varying])::text[])))
);


--
-- Name: cost_ledger_start; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cost_ledger_start (
    id integer NOT NULL,
    started_at timestamp with time zone NOT NULL
);


--
-- Name: cost_ledger_start_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.cost_ledger_start_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: cost_ledger_start_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.cost_ledger_start_id_seq OWNED BY public.cost_ledger_start.id;


--
-- Name: data_connections; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.data_connections (
    id uuid NOT NULL,
    project_id uuid NOT NULL,
    name character varying(120) NOT NULL,
    kind character varying(16) NOT NULL,
    config json NOT NULL,
    secret_ciphertext text NOT NULL,
    last_tested_at timestamp with time zone,
    last_error_code character varying(40),
    created_by_user_id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT ck_data_connections_kind CHECK (((kind)::text = ANY ((ARRAY['postgres'::character varying, 'mysql'::character varying, 'bigquery'::character varying, 'google_sheets'::character varying, 'google_drive'::character varying, 'prometheus'::character varying, 'influxdb'::character varying, 'google'::character varying])::text[])))
);


--
-- Name: dataset_versions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.dataset_versions (
    id uuid NOT NULL,
    dataset_id uuid NOT NULL,
    version_number integer NOT NULL,
    storage_key character varying(400) NOT NULL,
    original_filename character varying(255) NOT NULL,
    size_bytes bigint NOT NULL,
    sha256 character varying(64) NOT NULL,
    row_count integer NOT NULL,
    column_names json NOT NULL,
    created_by_user_id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    source_type character varying(16) DEFAULT 'upload'::character varying NOT NULL,
    source_details json,
    CONSTRAINT ck_dataset_versions_source_type CHECK (((source_type)::text = ANY ((ARRAY['upload'::character varying, 'connection'::character varying])::text[])))
);


--
-- Name: datasets; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.datasets (
    id uuid NOT NULL,
    project_id uuid NOT NULL,
    name character varying(160) NOT NULL,
    description text,
    created_by_user_id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: email_otps; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.email_otps (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    purpose character varying(32) NOT NULL,
    code_digest character varying(64),
    expires_at timestamp with time zone NOT NULL,
    attempts integer NOT NULL,
    failed_attempts integer NOT NULL,
    locked_until timestamp with time zone,
    sent_at timestamp with time zone NOT NULL,
    send_count integer NOT NULL,
    send_window_started_at timestamp with time zone NOT NULL,
    link_token_digest character varying(64),
    CONSTRAINT ck_email_otps_purpose CHECK (((purpose)::text = 'sign_in'::text))
);


--
-- Name: engine_settings; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.engine_settings (
    engine_key character varying(100) NOT NULL,
    "values" json NOT NULL,
    updated_by_user_id uuid,
    updated_at timestamp with time zone NOT NULL
);


--
-- Name: frame_reviews; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.frame_reviews (
    id uuid NOT NULL,
    run_id uuid NOT NULL,
    sequence integer NOT NULL,
    request_storage_key character varying(400) NOT NULL,
    requested_at timestamp with time zone DEFAULT now() NOT NULL,
    decision_storage_key character varying(400),
    submitted_by_user_id uuid,
    submitted_at timestamp with time zone
);


--
-- Name: google_connection_grants; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.google_connection_grants (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    project_id uuid NOT NULL,
    state_hash character varying(64) NOT NULL,
    secret_ciphertext text,
    google_subject character varying(255),
    account_email character varying(320),
    expires_at timestamp with time zone NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: integration_deliveries; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.integration_deliveries (
    id uuid NOT NULL,
    integration_id uuid NOT NULL,
    event_id uuid NOT NULL,
    event_key character varying(40) NOT NULL,
    ref json NOT NULL,
    status character varying(8) NOT NULL,
    attempts integer NOT NULL,
    claims integer NOT NULL,
    config_version integer NOT NULL,
    next_attempt_at timestamp with time zone NOT NULL,
    locked_until timestamp with time zone,
    response_code integer,
    error_code character varying(40),
    created_at timestamp with time zone NOT NULL,
    sent_at timestamp with time zone,
    CONSTRAINT ck_deliveries_status CHECK (((status)::text = ANY ((ARRAY['pending'::character varying, 'sending'::character varying, 'sent'::character varying, 'failed'::character varying])::text[])))
);


--
-- Name: integration_secrets; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.integration_secrets (
    name character varying(100) NOT NULL,
    value_encrypted text NOT NULL,
    updated_by_user_id uuid,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: model_profiles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.model_profiles (
    id uuid NOT NULL,
    role character varying(20) NOT NULL,
    provider character varying(32) NOT NULL,
    base_url character varying(500),
    model character varying(200) NOT NULL,
    api_key_encrypted text,
    extra json DEFAULT '{}'::json NOT NULL,
    scope character varying(20) DEFAULT 'global'::character varying NOT NULL,
    updated_by_user_id uuid,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT ck_model_profiles_role CHECK (((role)::text = ANY ((ARRAY['stage'::character varying, 'review'::character varying])::text[]))),
    CONSTRAINT ck_model_profiles_scope CHECK (((scope)::text = 'global'::text))
);


--
-- Name: monitoring_alerts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.monitoring_alerts (
    id uuid NOT NULL,
    service_id character varying(160) NOT NULL,
    service character varying(64) NOT NULL,
    environment character varying(20) NOT NULL,
    code character varying(80) NOT NULL,
    severity character varying(16) NOT NULL,
    message character varying(240) NOT NULL,
    status character varying(16) NOT NULL,
    active_key character varying(220),
    started_at timestamp with time zone NOT NULL,
    resolved_at timestamp with time zone,
    acknowledged_at timestamp with time zone,
    acknowledged_by_user_id uuid,
    details json NOT NULL,
    CONSTRAINT ck_monitoring_alerts_severity CHECK (((severity)::text = ANY ((ARRAY['warning'::character varying, 'critical'::character varying])::text[]))),
    CONSTRAINT ck_monitoring_alerts_status CHECK (((status)::text = ANY ((ARRAY['active'::character varying, 'resolved'::character varying])::text[])))
);


--
-- Name: monitoring_capture_gaps; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.monitoring_capture_gaps (
    id uuid NOT NULL,
    service character varying(64) NOT NULL,
    environment character varying(20) NOT NULL,
    worker_id character varying(36),
    reason character varying(48) NOT NULL,
    started_at timestamp with time zone NOT NULL,
    ended_at timestamp with time zone NOT NULL,
    created_at timestamp with time zone NOT NULL,
    CONSTRAINT ck_monitoring_capture_gaps_interval CHECK ((ended_at >= started_at))
);


--
-- Name: monitoring_events; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.monitoring_events (
    id uuid NOT NULL,
    event_type character varying(48) NOT NULL,
    service character varying(64) NOT NULL,
    environment character varying(20) NOT NULL,
    worker_id character varying(36) NOT NULL,
    level character varying(16) NOT NULL,
    message character varying(160) NOT NULL,
    request_id character varying(64),
    trace_id character varying(64),
    project_id character varying(64),
    run_id character varying(64),
    actor_id character varying(64),
    provider_id character varying(100),
    method character varying(10),
    route character varying(200),
    status_code integer,
    duration_ms double precision,
    attributes json NOT NULL,
    created_at timestamp with time zone NOT NULL,
    CONSTRAINT ck_monitoring_events_duration CHECK (((duration_ms IS NULL) OR (duration_ms >= (0)::double precision))),
    CONSTRAINT ck_monitoring_events_status CHECK (((status_code IS NULL) OR ((status_code >= 100) AND (status_code <= 599))))
);


--
-- Name: monitoring_worker_states; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.monitoring_worker_states (
    worker_id character varying(36) NOT NULL,
    service character varying(64) NOT NULL,
    environment character varying(20) NOT NULL,
    status character varying(16) NOT NULL,
    started_at timestamp with time zone NOT NULL,
    heartbeat_at timestamp with time zone NOT NULL,
    stopped_at timestamp with time zone,
    persisted_watermark timestamp with time zone,
    dropped_count integer DEFAULT 0 NOT NULL
);


--
-- Name: notification_emails; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.notification_emails (
    id uuid NOT NULL,
    recipient_user_id uuid NOT NULL,
    kind character varying(32) NOT NULL,
    project_id uuid NOT NULL,
    run_id uuid,
    actor_user_id uuid,
    status character varying(16) NOT NULL,
    attempts integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    sent_at timestamp with time zone,
    CONSTRAINT ck_notification_emails_kind CHECK (((kind)::text = ANY ((ARRAY['run_awaiting_review'::character varying, 'run_finished'::character varying, 'added_to_project'::character varying, 'run_commented'::character varying, 'project_invited'::character varying, 'invite_accepted'::character varying, 'invite_declined'::character varying, 'member_role_changed'::character varying, 'removed_from_project'::character varying, 'integration_failed'::character varying, 'budget_warning'::character varying, 'budget_exceeded'::character varying])::text[]))),
    CONSTRAINT ck_notification_emails_status CHECK (((status)::text = ANY ((ARRAY['pending'::character varying, 'sending'::character varying, 'sent'::character varying, 'failed'::character varying, 'skipped'::character varying])::text[])))
);


--
-- Name: notification_preferences; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.notification_preferences (
    id uuid NOT NULL,
    project_id uuid NOT NULL,
    user_id uuid NOT NULL,
    events json NOT NULL,
    digest json NOT NULL,
    quiet_hours json NOT NULL,
    version integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


--
-- Name: notifications; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.notifications (
    id uuid NOT NULL,
    recipient_user_id uuid NOT NULL,
    kind character varying(32) NOT NULL,
    project_id uuid NOT NULL,
    run_id uuid,
    actor_user_id uuid,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    read_at timestamp with time zone,
    CONSTRAINT ck_notifications_kind CHECK (((kind)::text = ANY ((ARRAY['run_awaiting_review'::character varying, 'run_finished'::character varying, 'added_to_project'::character varying, 'run_commented'::character varying, 'project_invited'::character varying, 'invite_accepted'::character varying, 'invite_declined'::character varying, 'member_role_changed'::character varying, 'removed_from_project'::character varying, 'integration_failed'::character varying, 'budget_warning'::character varying, 'budget_exceeded'::character varying])::text[])))
);


--
-- Name: pi_consultations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.pi_consultations (
    id uuid NOT NULL,
    research_run_id uuid NOT NULL,
    stage_run_id uuid,
    kind character varying(32) NOT NULL,
    gate_id character varying(200),
    authority character varying(20) NOT NULL,
    status character varying(24) NOT NULL,
    request json NOT NULL,
    result json,
    failure json,
    applied_decision_id uuid,
    created_at timestamp with time zone NOT NULL,
    sent_at timestamp with time zone,
    decided_at timestamp with time zone,
    resolved_at timestamp with time zone,
    tokens_used bigint DEFAULT '0'::bigint NOT NULL,
    CONSTRAINT ck_pi_consultations_authority CHECK (((authority)::text = ANY ((ARRAY['pi'::character varying, 'researcher'::character varying])::text[]))),
    CONSTRAINT ck_pi_consultations_kind CHECK (((kind)::text = ANY ((ARRAY['charter'::character varying, 'gate_question'::character varying, 'gate_review'::character varying, 'stage_outcome'::character varying, 'failure'::character varying, 'close'::character varying, 'stage_review'::character varying])::text[]))),
    CONSTRAINT ck_pi_consultations_status CHECK (((status)::text = ANY ((ARRAY['queued'::character varying, 'sent'::character varying, 'decided'::character varying, 'applied'::character varying, 'awaiting_researcher'::character varying, 'endorsed'::character varying, 'overridden'::character varying, 'stale'::character varying, 'failed'::character varying])::text[])))
);


--
-- Name: pi_notes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.pi_notes (
    id uuid NOT NULL,
    research_run_id uuid NOT NULL,
    consultation_id uuid,
    kind character varying(16) NOT NULL,
    text text NOT NULL,
    stage_key character varying(100),
    actor character varying(8) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    CONSTRAINT ck_pi_notes_actor CHECK (((actor)::text = ANY ((ARRAY['pi'::character varying, 'user'::character varying])::text[]))),
    CONSTRAINT ck_pi_notes_kind CHECK (((kind)::text = ANY ((ARRAY['decision'::character varying, 'lesson'::character varying, 'risk'::character varying, 'observation'::character varying, 'question'::character varying, 'directive'::character varying, 'override'::character varying, 'brief'::character varying, 'critique'::character varying])::text[])))
);


--
-- Name: platform_settings; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.platform_settings (
    id integer NOT NULL,
    "values" json NOT NULL,
    updated_by_user_id uuid,
    updated_at timestamp with time zone NOT NULL,
    CONSTRAINT ck_platform_settings_single_row CHECK ((id = 1))
);


--
-- Name: platform_settings_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.platform_settings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: platform_settings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.platform_settings_id_seq OWNED BY public.platform_settings.id;


--
-- Name: project_files; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.project_files (
    id uuid NOT NULL,
    project_id uuid NOT NULL,
    kind character varying(16) NOT NULL,
    original_filename character varying(255) NOT NULL,
    content_type character varying(100) NOT NULL,
    storage_key character varying(400) NOT NULL,
    size_bytes bigint NOT NULL,
    sha256 character varying(64) NOT NULL,
    created_by_user_id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT ck_project_files_kind CHECK (((kind)::text = ANY ((ARRAY['pdf'::character varying, 'csv'::character varying, 'excel'::character varying])::text[])))
);


--
-- Name: project_integrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.project_integrations (
    id uuid NOT NULL,
    project_id uuid NOT NULL,
    provider character varying(16) NOT NULL,
    name character varying(80) NOT NULL,
    events json NOT NULL,
    secret_ciphertext text NOT NULL,
    url_hint character varying(300) NOT NULL,
    status character varying(8) NOT NULL,
    consecutive_failures integer NOT NULL,
    config_version integer NOT NULL,
    last_delivered_at timestamp with time zone,
    last_error_code character varying(40),
    last_error_at timestamp with time zone,
    created_by_user_id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    CONSTRAINT ck_integrations_provider CHECK (((provider)::text = ANY ((ARRAY['slack'::character varying, 'teams'::character varying, 'discord'::character varying])::text[]))),
    CONSTRAINT ck_integrations_status CHECK (((status)::text = ANY ((ARRAY['active'::character varying, 'paused'::character varying, 'error'::character varying])::text[])))
);


--
-- Name: project_memberships; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.project_memberships (
    id uuid NOT NULL,
    project_id uuid NOT NULL,
    user_id uuid NOT NULL,
    role_code character varying(32) NOT NULL,
    status character varying(20) DEFAULT 'active'::character varying NOT NULL,
    created_by_user_id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    revoked_at timestamp with time zone,
    invite_sent_at timestamp with time zone,
    invite_expires_at timestamp with time zone,
    CONSTRAINT ck_project_memberships_role CHECK (((role_code)::text = ANY ((ARRAY['project_manager'::character varying, 'researcher'::character varying, 'reviewer'::character varying])::text[]))),
    CONSTRAINT ck_project_memberships_status CHECK (((status)::text = ANY ((ARRAY['invited'::character varying, 'active'::character varying, 'revoked'::character varying])::text[])))
);


--
-- Name: project_settings; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.project_settings (
    project_id uuid NOT NULL,
    version integer NOT NULL,
    sections json NOT NULL,
    updated_by_user_id uuid,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


--
-- Name: projects; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.projects (
    id uuid NOT NULL,
    name character varying(160) NOT NULL,
    description text,
    domain character varying(160),
    objective text,
    status character varying(20) DEFAULT 'active'::character varying NOT NULL,
    owner_user_id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    tags json NOT NULL,
    archived_at timestamp with time zone,
    CONSTRAINT ck_projects_status CHECK (((status)::text = ANY ((ARRAY['draft'::character varying, 'data_ready'::character varying, 'researching'::character varying, 'needs_review'::character varying, 'completed'::character varying])::text[])))
);


--
-- Name: research_contexts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.research_contexts (
    id uuid NOT NULL,
    project_id uuid NOT NULL,
    version_number integer NOT NULL,
    body text NOT NULL,
    front_matter json,
    created_by_user_id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: research_runs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.research_runs (
    id uuid NOT NULL,
    project_id uuid NOT NULL,
    dataset_version_id uuid,
    research_context_id uuid,
    created_by_user_id uuid NOT NULL,
    status character varying(20) NOT NULL,
    auto_review boolean NOT NULL,
    failure_message text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    started_at timestamp with time zone,
    finished_at timestamp with time zone,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    review_mode character varying(20) DEFAULT 'copilot'::character varying,
    last_seq integer DEFAULT 0 NOT NULL,
    last_source_seq integer DEFAULT 0 NOT NULL,
    pipeline_key character varying(100),
    current_stage_key character varying(100),
    interaction_mode character varying(20),
    iteration integer DEFAULT 1 NOT NULL,
    charter_status character varying(10) DEFAULT 'none'::character varying NOT NULL,
    obligations json DEFAULT '[]'::json NOT NULL,
    token_budget bigint DEFAULT '4000000'::bigint NOT NULL,
    tokens_used bigint DEFAULT '0'::bigint NOT NULL,
    research_case json NOT NULL,
    CONSTRAINT ck_research_runs_charter_status CHECK (((charter_status)::text = ANY ((ARRAY['none'::character varying, 'pending'::character varying, 'settled'::character varying, 'skipped'::character varying])::text[]))),
    CONSTRAINT ck_research_runs_interaction_mode CHECK (((interaction_mode IS NULL) OR ((interaction_mode)::text = ANY ((ARRAY['auto'::character varying, 'light'::character varying])::text[])))),
    CONSTRAINT ck_research_runs_status CHECK (((status)::text = ANY ((ARRAY['queued'::character varying, 'running'::character varying, 'paused'::character varying, 'awaiting_review'::character varying, 'completed'::character varying, 'budget_exceeded'::character varying, 'failed'::character varying, 'stopped'::character varying])::text[])))
);


--
-- Name: run_artifacts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.run_artifacts (
    id uuid NOT NULL,
    run_id uuid NOT NULL,
    kind character varying(20) NOT NULL,
    filename character varying(255) NOT NULL,
    content_type character varying(100) NOT NULL,
    storage_key character varying(400) NOT NULL,
    size_bytes bigint NOT NULL,
    sha256 character varying(64) NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    stage_run_id uuid,
    schema character varying(160),
    version integer,
    "primary" boolean DEFAULT false NOT NULL,
    review_round integer,
    metadata json DEFAULT '{}'::json NOT NULL,
    CONSTRAINT ck_run_artifacts_kind CHECK (((kind)::text = ANY ((ARRAY['paper_pdf'::character varying, 'paper_tex'::character varying, 'figure'::character varying, 'results'::character varying, 'other'::character varying])::text[])))
);


--
-- Name: run_events; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.run_events (
    run_id uuid NOT NULL,
    seq integer NOT NULL,
    source_seq integer,
    type character varying(48) NOT NULL,
    stage_key character varying(32),
    actor character varying(32),
    payload json NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    stage_run_id uuid,
    step_key character varying(100),
    iteration integer DEFAULT 1 NOT NULL,
    phase character varying(32),
    class character varying(20) DEFAULT 'lifecycle'::character varying NOT NULL,
    summary text,
    refs json DEFAULT '[]'::json NOT NULL,
    CONSTRAINT ck_run_events_seq CHECK ((seq >= 1))
);


--
-- Name: run_gates; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.run_gates (
    id uuid NOT NULL,
    run_id uuid NOT NULL,
    gate_key character varying(32) NOT NULL,
    kind character varying(32) NOT NULL,
    spec json NOT NULL,
    opened_seq integer NOT NULL,
    answer json,
    answered_by_user_id uuid,
    answered_at timestamp with time zone,
    resolved_seq integer,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    stage_run_id uuid
);


--
-- Name: spending_alerts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.spending_alerts (
    id uuid NOT NULL,
    project_id uuid NOT NULL,
    period character varying(7) NOT NULL,
    kind character varying(32) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    CONSTRAINT ck_spending_alerts_kind CHECK (((kind)::text = ANY ((ARRAY['budget_warning'::character varying, 'budget_exceeded'::character varying])::text[])))
);


--
-- Name: stage_decisions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.stage_decisions (
    id uuid NOT NULL,
    stage_run_id uuid NOT NULL,
    gate_id character varying(200),
    action character varying(32) NOT NULL,
    payload json DEFAULT '{}'::json NOT NULL,
    actor character varying(20) NOT NULL,
    reason text,
    status character varying(20) DEFAULT 'applied'::character varying NOT NULL,
    decided_by_user_id uuid,
    decided_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT ck_stage_decisions_action CHECK (((action)::text = ANY ((ARRAY['answer_gate'::character varying, 'approve'::character varying, 'comment'::character varying, 'accept'::character varying, 'send_back'::character varying, 'rerun'::character varying, 'stop'::character varying])::text[]))),
    CONSTRAINT ck_stage_decisions_actor CHECK (((actor)::text = ANY ((ARRAY['user'::character varying, 'system'::character varying, 'pi'::character varying])::text[]))),
    CONSTRAINT ck_stage_decisions_status CHECK (((status)::text = ANY ((ARRAY['pending'::character varying, 'applied'::character varying])::text[])))
);


--
-- Name: stage_runs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.stage_runs (
    id uuid NOT NULL,
    research_run_id uuid NOT NULL,
    iteration integer DEFAULT 1 NOT NULL,
    stage_key character varying(100) NOT NULL,
    engine_key character varying(100) NOT NULL,
    engine_run_id character varying(200),
    prior_stage_run_id uuid,
    origin_decision_id uuid,
    status character varying(20) DEFAULT 'PENDING'::character varying NOT NULL,
    phase character varying(32),
    step_key character varying(100),
    waiting_input boolean DEFAULT false NOT NULL,
    open_gate json,
    input_refs json DEFAULT '[]'::json NOT NULL,
    config_snapshot json DEFAULT '{}'::json NOT NULL,
    last_source_seq integer DEFAULT 0 NOT NULL,
    failure json,
    engine_unreachable_since timestamp with time zone,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    finished_at timestamp with time zone,
    tokens_used bigint DEFAULT '0'::bigint NOT NULL,
    CONSTRAINT ck_stage_runs_status CHECK (((status)::text = ANY ((ARRAY['PENDING'::character varying, 'RUNNING'::character varying, 'COMPLETED'::character varying, 'ACCEPTED'::character varying, 'FAILED'::character varying, 'STOPPED'::character varying, 'SUPERSEDED'::character varying])::text[])))
);


--
-- Name: user_platform_roles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_platform_roles (
    user_id uuid NOT NULL,
    role_code character varying(32) DEFAULT 'platform_admin'::character varying NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT ck_user_platform_roles_code CHECK (((role_code)::text = 'platform_admin'::text))
);


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id uuid NOT NULL,
    email character varying(320) NOT NULL,
    email_normalized character varying(320) NOT NULL,
    display_name character varying(200),
    status character varying(32) DEFAULT 'active'::character varying NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    last_login_at timestamp with time zone,
    created_by_user_id uuid,
    avatar_storage_key character varying(400),
    avatar_content_type character varying(32),
    invite_sent_at timestamp with time zone,
    email_verified_at timestamp with time zone,
    google_subject character varying(255),
    onboarded_at timestamp with time zone,
    CONSTRAINT ck_users_status CHECK (((status)::text = ANY ((ARRAY['active'::character varying, 'suspended'::character varying])::text[])))
);


--
-- Name: cost_ledger_start id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cost_ledger_start ALTER COLUMN id SET DEFAULT nextval('public.cost_ledger_start_id_seq'::regclass);


--
-- Name: platform_settings id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.platform_settings ALTER COLUMN id SET DEFAULT nextval('public.platform_settings_id_seq'::regclass);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: audit_events audit_events_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.audit_events
    ADD CONSTRAINT audit_events_pkey PRIMARY KEY (id);


--
-- Name: auth_sessions auth_sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_sessions
    ADD CONSTRAINT auth_sessions_pkey PRIMARY KEY (id);


--
-- Name: auth_sessions auth_sessions_token_digest_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_sessions
    ADD CONSTRAINT auth_sessions_token_digest_key UNIQUE (token_digest);


--
-- Name: comments comments_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_pkey PRIMARY KEY (id);


--
-- Name: cost_entries cost_entries_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cost_entries
    ADD CONSTRAINT cost_entries_pkey PRIMARY KEY (id);


--
-- Name: cost_ledger_start cost_ledger_start_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cost_ledger_start
    ADD CONSTRAINT cost_ledger_start_pkey PRIMARY KEY (id);


--
-- Name: data_connections data_connections_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.data_connections
    ADD CONSTRAINT data_connections_pkey PRIMARY KEY (id);


--
-- Name: dataset_versions dataset_versions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dataset_versions
    ADD CONSTRAINT dataset_versions_pkey PRIMARY KEY (id);


--
-- Name: dataset_versions dataset_versions_storage_key_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dataset_versions
    ADD CONSTRAINT dataset_versions_storage_key_key UNIQUE (storage_key);


--
-- Name: datasets datasets_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.datasets
    ADD CONSTRAINT datasets_pkey PRIMARY KEY (id);


--
-- Name: email_otps email_otps_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.email_otps
    ADD CONSTRAINT email_otps_pkey PRIMARY KEY (id);


--
-- Name: engine_settings engine_settings_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.engine_settings
    ADD CONSTRAINT engine_settings_pkey PRIMARY KEY (engine_key);


--
-- Name: frame_reviews frame_reviews_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.frame_reviews
    ADD CONSTRAINT frame_reviews_pkey PRIMARY KEY (id);


--
-- Name: google_connection_grants google_connection_grants_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.google_connection_grants
    ADD CONSTRAINT google_connection_grants_pkey PRIMARY KEY (id);


--
-- Name: google_connection_grants google_connection_grants_state_hash_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.google_connection_grants
    ADD CONSTRAINT google_connection_grants_state_hash_key UNIQUE (state_hash);


--
-- Name: integration_deliveries integration_deliveries_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.integration_deliveries
    ADD CONSTRAINT integration_deliveries_pkey PRIMARY KEY (id);


--
-- Name: integration_secrets integration_secrets_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.integration_secrets
    ADD CONSTRAINT integration_secrets_pkey PRIMARY KEY (name);


--
-- Name: model_profiles model_profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.model_profiles
    ADD CONSTRAINT model_profiles_pkey PRIMARY KEY (id);


--
-- Name: monitoring_alerts monitoring_alerts_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.monitoring_alerts
    ADD CONSTRAINT monitoring_alerts_pkey PRIMARY KEY (id);


--
-- Name: monitoring_capture_gaps monitoring_capture_gaps_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.monitoring_capture_gaps
    ADD CONSTRAINT monitoring_capture_gaps_pkey PRIMARY KEY (id);


--
-- Name: monitoring_events monitoring_events_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.monitoring_events
    ADD CONSTRAINT monitoring_events_pkey PRIMARY KEY (id);


--
-- Name: monitoring_worker_states monitoring_worker_states_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.monitoring_worker_states
    ADD CONSTRAINT monitoring_worker_states_pkey PRIMARY KEY (worker_id);


--
-- Name: notification_emails notification_emails_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notification_emails
    ADD CONSTRAINT notification_emails_pkey PRIMARY KEY (id);


--
-- Name: notification_preferences notification_preferences_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notification_preferences
    ADD CONSTRAINT notification_preferences_pkey PRIMARY KEY (id);


--
-- Name: notifications notifications_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_pkey PRIMARY KEY (id);


--
-- Name: pi_consultations pi_consultations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pi_consultations
    ADD CONSTRAINT pi_consultations_pkey PRIMARY KEY (id);


--
-- Name: pi_notes pi_notes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pi_notes
    ADD CONSTRAINT pi_notes_pkey PRIMARY KEY (id);


--
-- Name: run_events pk_run_events; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.run_events
    ADD CONSTRAINT pk_run_events PRIMARY KEY (run_id, seq);


--
-- Name: platform_settings platform_settings_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.platform_settings
    ADD CONSTRAINT platform_settings_pkey PRIMARY KEY (id);


--
-- Name: project_files project_files_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.project_files
    ADD CONSTRAINT project_files_pkey PRIMARY KEY (id);


--
-- Name: project_files project_files_storage_key_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.project_files
    ADD CONSTRAINT project_files_storage_key_key UNIQUE (storage_key);


--
-- Name: project_integrations project_integrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.project_integrations
    ADD CONSTRAINT project_integrations_pkey PRIMARY KEY (id);


--
-- Name: project_memberships project_memberships_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.project_memberships
    ADD CONSTRAINT project_memberships_pkey PRIMARY KEY (id);


--
-- Name: project_settings project_settings_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.project_settings
    ADD CONSTRAINT project_settings_pkey PRIMARY KEY (project_id);


--
-- Name: projects projects_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_pkey PRIMARY KEY (id);


--
-- Name: research_contexts research_contexts_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.research_contexts
    ADD CONSTRAINT research_contexts_pkey PRIMARY KEY (id);


--
-- Name: research_runs research_runs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.research_runs
    ADD CONSTRAINT research_runs_pkey PRIMARY KEY (id);


--
-- Name: run_artifacts run_artifacts_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.run_artifacts
    ADD CONSTRAINT run_artifacts_pkey PRIMARY KEY (id);


--
-- Name: run_artifacts run_artifacts_storage_key_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.run_artifacts
    ADD CONSTRAINT run_artifacts_storage_key_key UNIQUE (storage_key);


--
-- Name: run_gates run_gates_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.run_gates
    ADD CONSTRAINT run_gates_pkey PRIMARY KEY (id);


--
-- Name: spending_alerts spending_alerts_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.spending_alerts
    ADD CONSTRAINT spending_alerts_pkey PRIMARY KEY (id);


--
-- Name: stage_decisions stage_decisions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stage_decisions
    ADD CONSTRAINT stage_decisions_pkey PRIMARY KEY (id);


--
-- Name: stage_runs stage_runs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stage_runs
    ADD CONSTRAINT stage_runs_pkey PRIMARY KEY (id);


--
-- Name: cost_entries uq_cost_entries_source_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cost_entries
    ADD CONSTRAINT uq_cost_entries_source_key UNIQUE (source_key);


--
-- Name: dataset_versions uq_dataset_versions_number; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dataset_versions
    ADD CONSTRAINT uq_dataset_versions_number UNIQUE (dataset_id, version_number);


--
-- Name: integration_deliveries uq_deliveries_integration_event; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.integration_deliveries
    ADD CONSTRAINT uq_deliveries_integration_event UNIQUE (integration_id, event_id);


--
-- Name: email_otps uq_email_otps_link_token_digest; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.email_otps
    ADD CONSTRAINT uq_email_otps_link_token_digest UNIQUE (link_token_digest);


--
-- Name: email_otps uq_email_otps_user_purpose; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.email_otps
    ADD CONSTRAINT uq_email_otps_user_purpose UNIQUE (user_id, purpose);


--
-- Name: frame_reviews uq_frame_reviews_sequence; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.frame_reviews
    ADD CONSTRAINT uq_frame_reviews_sequence UNIQUE (run_id, sequence);


--
-- Name: model_profiles uq_model_profiles_role_scope; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.model_profiles
    ADD CONSTRAINT uq_model_profiles_role_scope UNIQUE (role, scope);


--
-- Name: monitoring_alerts uq_monitoring_alerts_active_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.monitoring_alerts
    ADD CONSTRAINT uq_monitoring_alerts_active_key UNIQUE (active_key);


--
-- Name: notification_preferences uq_notification_preferences_member; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notification_preferences
    ADD CONSTRAINT uq_notification_preferences_member UNIQUE (project_id, user_id);


--
-- Name: research_contexts uq_research_contexts_number; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.research_contexts
    ADD CONSTRAINT uq_research_contexts_number UNIQUE (project_id, version_number);


--
-- Name: run_artifacts uq_run_artifacts_stage_schema_version; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.run_artifacts
    ADD CONSTRAINT uq_run_artifacts_stage_schema_version UNIQUE (stage_run_id, schema, version);


--
-- Name: spending_alerts uq_spending_alerts_period_kind; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.spending_alerts
    ADD CONSTRAINT uq_spending_alerts_period_kind UNIQUE (project_id, period, kind);


--
-- Name: stage_decisions uq_stage_decisions_gate; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stage_decisions
    ADD CONSTRAINT uq_stage_decisions_gate UNIQUE (stage_run_id, gate_id);


--
-- Name: user_platform_roles user_platform_roles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_platform_roles
    ADD CONSTRAINT user_platform_roles_pkey PRIMARY KEY (user_id);


--
-- Name: users users_email_normalized_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_normalized_key UNIQUE (email_normalized);


--
-- Name: users users_google_subject_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_google_subject_key UNIQUE (google_subject);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_audit_action_created_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_audit_action_created_id ON public.audit_events USING btree (action, created_at, id);


--
-- Name: ix_audit_created_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_audit_created_id ON public.audit_events USING btree (created_at, id);


--
-- Name: ix_audit_project_created; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_audit_project_created ON public.audit_events USING btree (project_id, created_at);


--
-- Name: ix_auth_sessions_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_auth_sessions_user_id ON public.auth_sessions USING btree (user_id);


--
-- Name: ix_comments_run_created; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_comments_run_created ON public.comments USING btree (run_id, created_at);


--
-- Name: ix_cost_entries_project_occurred; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_cost_entries_project_occurred ON public.cost_entries USING btree (project_id, occurred_at);


--
-- Name: ix_cost_entries_source_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_cost_entries_source_id ON public.cost_entries USING btree (source_id);


--
-- Name: ix_data_connections_project_created; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_data_connections_project_created ON public.data_connections USING btree (project_id, created_at);


--
-- Name: ix_datasets_name_trgm; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_datasets_name_trgm ON public.datasets USING gin (name public.gin_trgm_ops);


--
-- Name: ix_integration_deliveries_due; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_integration_deliveries_due ON public.integration_deliveries USING btree (status, next_attempt_at);


--
-- Name: ix_integration_deliveries_integration_created; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_integration_deliveries_integration_created ON public.integration_deliveries USING btree (integration_id, created_at);


--
-- Name: ix_monitoring_alerts_service_status_started; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_monitoring_alerts_service_status_started ON public.monitoring_alerts USING btree (service_id, status, started_at);


--
-- Name: ix_monitoring_capture_gaps_interval; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_monitoring_capture_gaps_interval ON public.monitoring_capture_gaps USING btree (started_at, ended_at);


--
-- Name: ix_monitoring_capture_gaps_worker; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_monitoring_capture_gaps_worker ON public.monitoring_capture_gaps USING btree (worker_id, started_at);


--
-- Name: ix_monitoring_events_request_aggregation; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_monitoring_events_request_aggregation ON public.monitoring_events USING btree (service, environment, event_type, created_at, id);


--
-- Name: ix_monitoring_events_request_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_monitoring_events_request_id ON public.monitoring_events USING btree (request_id);


--
-- Name: ix_monitoring_events_service_environment_time; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_monitoring_events_service_environment_time ON public.monitoring_events USING btree (service, environment, created_at);


--
-- Name: ix_monitoring_events_type_time; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_monitoring_events_type_time ON public.monitoring_events USING btree (event_type, created_at, id);


--
-- Name: ix_monitoring_events_worker_time; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_monitoring_events_worker_time ON public.monitoring_events USING btree (worker_id, created_at);


--
-- Name: ix_monitoring_worker_states_status_heartbeat; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_monitoring_worker_states_status_heartbeat ON public.monitoring_worker_states USING btree (status, heartbeat_at);


--
-- Name: ix_notification_emails_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_notification_emails_status ON public.notification_emails USING btree (status, created_at);


--
-- Name: ix_notifications_recipient; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_notifications_recipient ON public.notifications USING btree (recipient_user_id, read_at, created_at);


--
-- Name: ix_pi_consultations_run_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_pi_consultations_run_status ON public.pi_consultations USING btree (research_run_id, status);


--
-- Name: ix_pi_consultations_stage_kind; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_pi_consultations_stage_kind ON public.pi_consultations USING btree (stage_run_id, kind);


--
-- Name: ix_pi_notes_run_created; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_pi_notes_run_created ON public.pi_notes USING btree (research_run_id, created_at);


--
-- Name: ix_project_files_project_created; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_project_files_project_created ON public.project_files USING btree (project_id, created_at);


--
-- Name: ix_project_integrations_project_created; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_project_integrations_project_created ON public.project_integrations USING btree (project_id, created_at);


--
-- Name: ix_project_memberships_project_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_project_memberships_project_id ON public.project_memberships USING btree (project_id);


--
-- Name: ix_project_memberships_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_project_memberships_user_id ON public.project_memberships USING btree (user_id);


--
-- Name: ix_projects_description_trgm; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_projects_description_trgm ON public.projects USING gin (description public.gin_trgm_ops);


--
-- Name: ix_projects_name_trgm; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_projects_name_trgm ON public.projects USING gin (name public.gin_trgm_ops);


--
-- Name: ix_projects_owner_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_projects_owner_user_id ON public.projects USING btree (owner_user_id);


--
-- Name: ix_research_runs_project_created; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_research_runs_project_created ON public.research_runs USING btree (project_id, created_at);


--
-- Name: ix_run_events_run_id_seq; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_run_events_run_id_seq ON public.run_events USING btree (run_id, seq);


--
-- Name: ix_stage_runs_run_iteration_stage; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_stage_runs_run_iteration_stage ON public.stage_runs USING btree (research_run_id, iteration, stage_key);


--
-- Name: ix_users_display_name_trgm; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_users_display_name_trgm ON public.users USING gin (display_name public.gin_trgm_ops);


--
-- Name: ix_users_email_trgm; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_users_email_trgm ON public.users USING gin (email public.gin_trgm_ops);


--
-- Name: run_events_source_seq; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX run_events_source_seq ON public.run_events USING btree (stage_run_id, source_seq) WHERE (source_seq IS NOT NULL);


--
-- Name: uq_data_connections_project_name; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX uq_data_connections_project_name ON public.data_connections USING btree (project_id, lower((name)::text));


--
-- Name: uq_datasets_project_name; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX uq_datasets_project_name ON public.datasets USING btree (project_id, lower((name)::text));


--
-- Name: uq_frame_reviews_pending_run; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX uq_frame_reviews_pending_run ON public.frame_reviews USING btree (run_id) WHERE (submitted_at IS NULL);


--
-- Name: uq_project_integrations_project_name; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX uq_project_integrations_project_name ON public.project_integrations USING btree (project_id, lower((name)::text));


--
-- Name: uq_project_membership_open; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX uq_project_membership_open ON public.project_memberships USING btree (user_id, project_id) WHERE ((status)::text = ANY ((ARRAY['invited'::character varying, 'active'::character varying])::text[]));


--
-- Name: uq_research_runs_active_project; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX uq_research_runs_active_project ON public.research_runs USING btree (project_id) WHERE (((status)::text = ANY ((ARRAY['queued'::character varying, 'running'::character varying, 'paused'::character varying, 'awaiting_review'::character varying])::text[])) OR (((status)::text = 'budget_exceeded'::text) AND (pipeline_key IS NOT NULL)));


--
-- Name: uq_run_gates_open; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX uq_run_gates_open ON public.run_gates USING btree (stage_run_id) WHERE (answer IS NULL);


--
-- Name: audit_events audit_events_actor_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.audit_events
    ADD CONSTRAINT audit_events_actor_user_id_fkey FOREIGN KEY (actor_user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: auth_sessions auth_sessions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_sessions
    ADD CONSTRAINT auth_sessions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: comments comments_artifact_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_artifact_id_fkey FOREIGN KEY (artifact_id) REFERENCES public.run_artifacts(id) ON DELETE RESTRICT;


--
-- Name: comments comments_author_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_author_user_id_fkey FOREIGN KEY (author_user_id) REFERENCES public.users(id) ON DELETE RESTRICT;


--
-- Name: comments comments_run_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_run_id_fkey FOREIGN KEY (run_id) REFERENCES public.research_runs(id) ON DELETE RESTRICT;


--
-- Name: cost_entries cost_entries_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cost_entries
    ADD CONSTRAINT cost_entries_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id) ON DELETE RESTRICT;


--
-- Name: cost_entries cost_entries_run_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cost_entries
    ADD CONSTRAINT cost_entries_run_id_fkey FOREIGN KEY (run_id) REFERENCES public.research_runs(id) ON DELETE RESTRICT;


--
-- Name: data_connections data_connections_created_by_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.data_connections
    ADD CONSTRAINT data_connections_created_by_user_id_fkey FOREIGN KEY (created_by_user_id) REFERENCES public.users(id) ON DELETE RESTRICT;


--
-- Name: data_connections data_connections_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.data_connections
    ADD CONSTRAINT data_connections_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id) ON DELETE RESTRICT;


--
-- Name: dataset_versions dataset_versions_created_by_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dataset_versions
    ADD CONSTRAINT dataset_versions_created_by_user_id_fkey FOREIGN KEY (created_by_user_id) REFERENCES public.users(id) ON DELETE RESTRICT;


--
-- Name: dataset_versions dataset_versions_dataset_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dataset_versions
    ADD CONSTRAINT dataset_versions_dataset_id_fkey FOREIGN KEY (dataset_id) REFERENCES public.datasets(id) ON DELETE RESTRICT;


--
-- Name: datasets datasets_created_by_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.datasets
    ADD CONSTRAINT datasets_created_by_user_id_fkey FOREIGN KEY (created_by_user_id) REFERENCES public.users(id) ON DELETE RESTRICT;


--
-- Name: datasets datasets_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.datasets
    ADD CONSTRAINT datasets_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id) ON DELETE RESTRICT;


--
-- Name: email_otps email_otps_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.email_otps
    ADD CONSTRAINT email_otps_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: engine_settings engine_settings_updated_by_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.engine_settings
    ADD CONSTRAINT engine_settings_updated_by_user_id_fkey FOREIGN KEY (updated_by_user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: project_memberships fk_project_memberships_project; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.project_memberships
    ADD CONSTRAINT fk_project_memberships_project FOREIGN KEY (project_id) REFERENCES public.projects(id) ON DELETE RESTRICT;


--
-- Name: run_artifacts fk_run_artifacts_stage_run; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.run_artifacts
    ADD CONSTRAINT fk_run_artifacts_stage_run FOREIGN KEY (stage_run_id) REFERENCES public.stage_runs(id);


--
-- Name: run_events fk_run_events_stage_run; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.run_events
    ADD CONSTRAINT fk_run_events_stage_run FOREIGN KEY (stage_run_id) REFERENCES public.stage_runs(id);


--
-- Name: run_gates fk_run_gates_stage_run; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.run_gates
    ADD CONSTRAINT fk_run_gates_stage_run FOREIGN KEY (stage_run_id) REFERENCES public.stage_runs(id);


--
-- Name: stage_runs fk_stage_runs_origin_decision; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stage_runs
    ADD CONSTRAINT fk_stage_runs_origin_decision FOREIGN KEY (origin_decision_id) REFERENCES public.stage_decisions(id);


--
-- Name: users fk_users_created_by_user; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT fk_users_created_by_user FOREIGN KEY (created_by_user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: frame_reviews frame_reviews_run_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.frame_reviews
    ADD CONSTRAINT frame_reviews_run_id_fkey FOREIGN KEY (run_id) REFERENCES public.research_runs(id) ON DELETE RESTRICT;


--
-- Name: frame_reviews frame_reviews_submitted_by_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.frame_reviews
    ADD CONSTRAINT frame_reviews_submitted_by_user_id_fkey FOREIGN KEY (submitted_by_user_id) REFERENCES public.users(id) ON DELETE RESTRICT;


--
-- Name: google_connection_grants google_connection_grants_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.google_connection_grants
    ADD CONSTRAINT google_connection_grants_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id) ON DELETE CASCADE;


--
-- Name: google_connection_grants google_connection_grants_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.google_connection_grants
    ADD CONSTRAINT google_connection_grants_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: integration_deliveries integration_deliveries_integration_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.integration_deliveries
    ADD CONSTRAINT integration_deliveries_integration_id_fkey FOREIGN KEY (integration_id) REFERENCES public.project_integrations(id) ON DELETE CASCADE;


--
-- Name: integration_secrets integration_secrets_updated_by_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.integration_secrets
    ADD CONSTRAINT integration_secrets_updated_by_user_id_fkey FOREIGN KEY (updated_by_user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: model_profiles model_profiles_updated_by_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.model_profiles
    ADD CONSTRAINT model_profiles_updated_by_user_id_fkey FOREIGN KEY (updated_by_user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: monitoring_alerts monitoring_alerts_acknowledged_by_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.monitoring_alerts
    ADD CONSTRAINT monitoring_alerts_acknowledged_by_user_id_fkey FOREIGN KEY (acknowledged_by_user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: notification_emails notification_emails_actor_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notification_emails
    ADD CONSTRAINT notification_emails_actor_user_id_fkey FOREIGN KEY (actor_user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: notification_emails notification_emails_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notification_emails
    ADD CONSTRAINT notification_emails_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id) ON DELETE CASCADE;


--
-- Name: notification_emails notification_emails_recipient_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notification_emails
    ADD CONSTRAINT notification_emails_recipient_user_id_fkey FOREIGN KEY (recipient_user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: notification_emails notification_emails_run_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notification_emails
    ADD CONSTRAINT notification_emails_run_id_fkey FOREIGN KEY (run_id) REFERENCES public.research_runs(id) ON DELETE CASCADE;


--
-- Name: notification_preferences notification_preferences_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notification_preferences
    ADD CONSTRAINT notification_preferences_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id) ON DELETE CASCADE;


--
-- Name: notification_preferences notification_preferences_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notification_preferences
    ADD CONSTRAINT notification_preferences_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: notifications notifications_actor_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_actor_user_id_fkey FOREIGN KEY (actor_user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: notifications notifications_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id) ON DELETE CASCADE;


--
-- Name: notifications notifications_recipient_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_recipient_user_id_fkey FOREIGN KEY (recipient_user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: notifications notifications_run_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_run_id_fkey FOREIGN KEY (run_id) REFERENCES public.research_runs(id) ON DELETE CASCADE;


--
-- Name: pi_consultations pi_consultations_applied_decision_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pi_consultations
    ADD CONSTRAINT pi_consultations_applied_decision_id_fkey FOREIGN KEY (applied_decision_id) REFERENCES public.stage_decisions(id) ON DELETE SET NULL;


--
-- Name: pi_consultations pi_consultations_research_run_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pi_consultations
    ADD CONSTRAINT pi_consultations_research_run_id_fkey FOREIGN KEY (research_run_id) REFERENCES public.research_runs(id) ON DELETE RESTRICT;


--
-- Name: pi_consultations pi_consultations_stage_run_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pi_consultations
    ADD CONSTRAINT pi_consultations_stage_run_id_fkey FOREIGN KEY (stage_run_id) REFERENCES public.stage_runs(id) ON DELETE RESTRICT;


--
-- Name: pi_notes pi_notes_consultation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pi_notes
    ADD CONSTRAINT pi_notes_consultation_id_fkey FOREIGN KEY (consultation_id) REFERENCES public.pi_consultations(id) ON DELETE SET NULL;


--
-- Name: pi_notes pi_notes_research_run_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pi_notes
    ADD CONSTRAINT pi_notes_research_run_id_fkey FOREIGN KEY (research_run_id) REFERENCES public.research_runs(id) ON DELETE CASCADE;


--
-- Name: platform_settings platform_settings_updated_by_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.platform_settings
    ADD CONSTRAINT platform_settings_updated_by_user_id_fkey FOREIGN KEY (updated_by_user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: project_files project_files_created_by_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.project_files
    ADD CONSTRAINT project_files_created_by_user_id_fkey FOREIGN KEY (created_by_user_id) REFERENCES public.users(id) ON DELETE RESTRICT;


--
-- Name: project_files project_files_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.project_files
    ADD CONSTRAINT project_files_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id) ON DELETE RESTRICT;


--
-- Name: project_integrations project_integrations_created_by_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.project_integrations
    ADD CONSTRAINT project_integrations_created_by_user_id_fkey FOREIGN KEY (created_by_user_id) REFERENCES public.users(id) ON DELETE RESTRICT;


--
-- Name: project_integrations project_integrations_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.project_integrations
    ADD CONSTRAINT project_integrations_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id) ON DELETE RESTRICT;


--
-- Name: project_memberships project_memberships_created_by_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.project_memberships
    ADD CONSTRAINT project_memberships_created_by_user_id_fkey FOREIGN KEY (created_by_user_id) REFERENCES public.users(id) ON DELETE RESTRICT;


--
-- Name: project_memberships project_memberships_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.project_memberships
    ADD CONSTRAINT project_memberships_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE RESTRICT;


--
-- Name: project_settings project_settings_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.project_settings
    ADD CONSTRAINT project_settings_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id) ON DELETE CASCADE;


--
-- Name: project_settings project_settings_updated_by_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.project_settings
    ADD CONSTRAINT project_settings_updated_by_user_id_fkey FOREIGN KEY (updated_by_user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: projects projects_owner_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_owner_user_id_fkey FOREIGN KEY (owner_user_id) REFERENCES public.users(id) ON DELETE RESTRICT;


--
-- Name: research_contexts research_contexts_created_by_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.research_contexts
    ADD CONSTRAINT research_contexts_created_by_user_id_fkey FOREIGN KEY (created_by_user_id) REFERENCES public.users(id) ON DELETE RESTRICT;


--
-- Name: research_contexts research_contexts_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.research_contexts
    ADD CONSTRAINT research_contexts_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id) ON DELETE RESTRICT;


--
-- Name: research_runs research_runs_created_by_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.research_runs
    ADD CONSTRAINT research_runs_created_by_user_id_fkey FOREIGN KEY (created_by_user_id) REFERENCES public.users(id) ON DELETE RESTRICT;


--
-- Name: research_runs research_runs_dataset_version_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.research_runs
    ADD CONSTRAINT research_runs_dataset_version_id_fkey FOREIGN KEY (dataset_version_id) REFERENCES public.dataset_versions(id) ON DELETE RESTRICT;


--
-- Name: research_runs research_runs_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.research_runs
    ADD CONSTRAINT research_runs_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id) ON DELETE RESTRICT;


--
-- Name: research_runs research_runs_research_context_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.research_runs
    ADD CONSTRAINT research_runs_research_context_id_fkey FOREIGN KEY (research_context_id) REFERENCES public.research_contexts(id) ON DELETE RESTRICT;


--
-- Name: run_artifacts run_artifacts_run_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.run_artifacts
    ADD CONSTRAINT run_artifacts_run_id_fkey FOREIGN KEY (run_id) REFERENCES public.research_runs(id) ON DELETE RESTRICT;


--
-- Name: run_events run_events_run_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.run_events
    ADD CONSTRAINT run_events_run_id_fkey FOREIGN KEY (run_id) REFERENCES public.research_runs(id) ON DELETE CASCADE;


--
-- Name: run_gates run_gates_answered_by_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.run_gates
    ADD CONSTRAINT run_gates_answered_by_user_id_fkey FOREIGN KEY (answered_by_user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: run_gates run_gates_run_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.run_gates
    ADD CONSTRAINT run_gates_run_id_fkey FOREIGN KEY (run_id) REFERENCES public.research_runs(id) ON DELETE CASCADE;


--
-- Name: spending_alerts spending_alerts_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.spending_alerts
    ADD CONSTRAINT spending_alerts_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id) ON DELETE CASCADE;


--
-- Name: stage_decisions stage_decisions_decided_by_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stage_decisions
    ADD CONSTRAINT stage_decisions_decided_by_user_id_fkey FOREIGN KEY (decided_by_user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: stage_decisions stage_decisions_stage_run_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stage_decisions
    ADD CONSTRAINT stage_decisions_stage_run_id_fkey FOREIGN KEY (stage_run_id) REFERENCES public.stage_runs(id) ON DELETE RESTRICT;


--
-- Name: stage_runs stage_runs_prior_stage_run_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stage_runs
    ADD CONSTRAINT stage_runs_prior_stage_run_id_fkey FOREIGN KEY (prior_stage_run_id) REFERENCES public.stage_runs(id);


--
-- Name: stage_runs stage_runs_research_run_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stage_runs
    ADD CONSTRAINT stage_runs_research_run_id_fkey FOREIGN KEY (research_run_id) REFERENCES public.research_runs(id) ON DELETE RESTRICT;


--
-- Name: user_platform_roles user_platform_roles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_platform_roles
    ADD CONSTRAINT user_platform_roles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--


