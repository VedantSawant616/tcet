CREATE TABLE IF NOT EXISTS ml_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc'),
    model_name TEXT NOT NULL,
    prediction DOUBLE PRECISION,
    probability DOUBLE PRECISION,
    actual_label DOUBLE PRECISION,
    latency_ms INTEGER,
    features JSONB
);

CREATE TABLE IF NOT EXISTS llm_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc'),
    application_name TEXT NOT NULL,
    prompt TEXT,
    response TEXT,
    latency_ms INTEGER,
    tokens_used INTEGER,
    cost_usd DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS unified_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc'),
    entity_name TEXT NOT NULL,
    entity_type TEXT NOT NULL, -- 'ML' or 'LLM'
    metric_name TEXT NOT NULL, -- 'drift_psi', 'hallucination_score', 'risk_score'
    value DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc'),
    severity TEXT NOT NULL,
    message TEXT NOT NULL,
    resolved BOOLEAN DEFAULT FALSE
);

-- Optional: Create indexes for frequently queried columns
CREATE INDEX IF NOT EXISTS idx_ml_events_timestamp ON ml_events(timestamp);
CREATE INDEX IF NOT EXISTS idx_llm_events_timestamp ON llm_events(timestamp);
CREATE INDEX IF NOT EXISTS idx_unified_metrics_timestamp ON unified_metrics(timestamp);
