-- Initial seed data for development and testing
-- Green Energy Trading Platform

-- Insert test users
INSERT INTO users (id, username, email, password_hash, role, wallet_balance) VALUES
('user-1', 'alice_trader', 'alice@test.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyVEk5c0dW4q', 'trader', 15000.00),
('user-2', 'bob_seller', 'bob@test.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyVEk5c0dW4q', 'trader', 12000.00),
('user-3', 'charlie_buyer', 'charlie@test.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyVEk5c0dW4q', 'trader', 20000.00),
('user-4', 'diana_energy', 'diana@test.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyVEk5c0dW4q', 'trader', 18000.00)
ON CONFLICT (email) DO NOTHING;

-- Insert sample energy assets
INSERT INTO energy_assets (id, owner_id, asset_type, capacity, location, status, efficiency) VALUES
('asset-1', 'user-1', 'solar', 500.00, 'California Solar Farm', 'active', 92.5),
('asset-2', 'user-2', 'wind', 800.00, 'Texas Wind Park', 'active', 88.0),
('asset-3', 'user-3', 'hydro', 1200.00, 'Oregon Hydro Plant', 'active', 95.0),
('asset-4', 'user-4', 'biomass', 600.00, 'Iowa Biomass Facility', 'active', 85.5)
ON CONFLICT (id) DO NOTHING;

-- Insert sample transactions
INSERT INTO transactions (id, energy_type, quantity, price, order_type, user_id, status, created_at) VALUES
('tx-1', 'solar', 100.00, 0.12, 'sell', 'user-1', 'pending', CURRENT_TIMESTAMP - INTERVAL '2 hours'),
('tx-2', 'wind', 150.00, 0.10, 'buy', 'user-2', 'pending', CURRENT_TIMESTAMP - INTERVAL '1 hour'),
('tx-3', 'hydro', 200.00, 0.08, 'sell', 'user-3', 'completed', CURRENT_TIMESTAMP - INTERVAL '3 hours'),
('tx-4', 'biomass', 80.00, 0.15, 'buy', 'user-4', 'completed', CURRENT_TIMESTAMP - INTERVAL '4 hours'),
('tx-5', 'solar', 120.00, 0.11, 'buy', 'user-2', 'pending', CURRENT_TIMESTAMP - INTERVAL '30 minutes')
ON CONFLICT (id) DO NOTHING;

-- Insert historical price data (last 7 days)
DO $$
DECLARE
    energy VARCHAR(20);
    base_price DECIMAL(10,3);
    i INTEGER;
BEGIN
    FOREACH energy IN ARRAY ARRAY['solar', 'wind', 'hydro', 'biomass']
    LOOP
        -- Set base price for each energy type
        CASE energy
            WHEN 'solar' THEN base_price := 0.12;
            WHEN 'wind' THEN base_price := 0.10;
            WHEN 'hydro' THEN base_price := 0.08;
            WHEN 'biomass' THEN base_price := 0.15;
        END CASE;
        
        -- Generate hourly prices for last 7 days
        FOR i IN 0..167 LOOP
            INSERT INTO price_history (energy_type, price, timestamp, volume)
            VALUES (
                energy,
                base_price + (random() * 0.04 - 0.02),
                CURRENT_TIMESTAMP - (i || ' hours')::INTERVAL,
                50 + random() * 100
            );
        END LOOP;
    END LOOP;
END $$;

-- Insert initial performance metrics
INSERT INTO performance_metrics (
    metric_date,
    transaction_efficiency,
    verification_time_reduction,
    weekly_transactions,
    success_rate,
    uptime_percentage,
    average_execution_time
) VALUES
(CURRENT_DATE, 35.0, 60.0, 1250, 99.9, 99.9, 2.3),
(CURRENT_DATE - 1, 34.5, 59.5, 1200, 99.8, 99.9, 2.4),
(CURRENT_DATE - 2, 35.2, 60.5, 1280, 99.9, 100.0, 2.2)
ON CONFLICT (metric_date) DO NOTHING;
