-- Analytics and reporting tables
-- Migration 003: Analytics enhancement

-- Daily trading volume table
CREATE TABLE IF NOT EXISTS daily_trading_volume (
    id SERIAL PRIMARY KEY,
    trade_date DATE NOT NULL,
    energy_type VARCHAR(20) NOT NULL,
    total_volume DECIMAL(15, 2) NOT NULL,
    total_transactions INTEGER NOT NULL,
    average_price DECIMAL(10, 3) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(trade_date, energy_type),
    CHECK (energy_type IN ('solar', 'wind', 'hydro', 'biomass'))
);

-- Performance metrics table
CREATE TABLE IF NOT EXISTS performance_metrics (
    id SERIAL PRIMARY KEY,
    metric_date DATE NOT NULL,
    transaction_efficiency DECIMAL(5, 2),
    verification_time_reduction DECIMAL(5, 2),
    weekly_transactions INTEGER,
    success_rate DECIMAL(5, 2),
    uptime_percentage DECIMAL(5, 2),
    average_execution_time DECIMAL(8, 3),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(metric_date)
);

-- User activity log
CREATE TABLE IF NOT EXISTS user_activity_log (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    activity_type VARCHAR(50) NOT NULL,
    activity_data JSONB,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- AI predictions cache
CREATE TABLE IF NOT EXISTS ai_predictions_cache (
    id SERIAL PRIMARY KEY,
    prediction_type VARCHAR(50) NOT NULL,
    energy_type VARCHAR(20) NOT NULL,
    prediction_data JSONB NOT NULL,
    confidence DECIMAL(5, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    CHECK (prediction_type IN ('price', 'demand', 'trend'))
);

-- Create indexes
CREATE INDEX idx_daily_volume_date ON daily_trading_volume(trade_date DESC);
CREATE INDEX idx_performance_metrics_date ON performance_metrics(metric_date DESC);
CREATE INDEX idx_user_activity_user_id ON user_activity_log(user_id);
CREATE INDEX idx_user_activity_created_at ON user_activity_log(created_at DESC);
CREATE INDEX idx_predictions_cache_expires ON ai_predictions_cache(expires_at);

-- Create view for trading dashboard
CREATE OR REPLACE VIEW trading_dashboard AS
SELECT 
    t.energy_type,
    COUNT(*) as total_trades,
    SUM(t.quantity) as total_volume,
    AVG(t.price) as average_price,
    COUNT(CASE WHEN t.status = 'completed' THEN 1 END) as completed_trades,
    COUNT(CASE WHEN t.status = 'pending' THEN 1 END) as pending_trades
FROM transactions t
WHERE t.created_at >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY t.energy_type;
