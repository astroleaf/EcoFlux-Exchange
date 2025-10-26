-- Initial Database Schema for Green Energy Trading Platform
-- Creates core tables for transactions, users, contracts, and assets

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(36) PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'trader',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    total_trades INTEGER DEFAULT 0,
    total_volume DECIMAL(15, 2) DEFAULT 0.00,
    wallet_balance DECIMAL(15, 2) DEFAULT 10000.00
);

-- Transactions table
CREATE TABLE IF NOT EXISTS transactions (
    id VARCHAR(36) PRIMARY KEY,
    energy_type VARCHAR(20) NOT NULL,
    quantity DECIMAL(10, 2) NOT NULL,
    price DECIMAL(10, 3) NOT NULL,
    order_type VARCHAR(10) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    matched_with VARCHAR(36),
    contract_id VARCHAR(36),
    execution_time DECIMAL(8, 3),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CHECK (energy_type IN ('solar', 'wind', 'hydro', 'biomass')),
    CHECK (order_type IN ('buy', 'sell')),
    CHECK (status IN ('pending', 'matched', 'completed', 'cancelled')),
    CHECK (quantity > 0),
    CHECK (price > 0)
);

-- Smart Contracts table
CREATE TABLE IF NOT EXISTS smart_contracts (
    id VARCHAR(36) PRIMARY KEY,
    buyer_id VARCHAR(36) NOT NULL,
    seller_id VARCHAR(36) NOT NULL,
    energy_type VARCHAR(20) NOT NULL,
    quantity DECIMAL(10, 2) NOT NULL,
    price DECIMAL(10, 3) NOT NULL,
    total_value DECIMAL(15, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deployed_at TIMESTAMP,
    executed_at TIMESTAMP,
    transaction_hash VARCHAR(66) NOT NULL,
    verification_status VARCHAR(20) DEFAULT 'unverified',
    execution_time DECIMAL(8, 3),
    gas_used DECIMAL(10, 6) DEFAULT 0,
    FOREIGN KEY (buyer_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (seller_id) REFERENCES users(id) ON DELETE CASCADE,
    CHECK (status IN ('pending', 'active', 'completed', 'failed')),
    CHECK (verification_status IN ('unverified', 'verified', 'failed'))
);

-- Energy Assets table
CREATE TABLE IF NOT EXISTS energy_assets (
    id VARCHAR(36) PRIMARY KEY,
    owner_id VARCHAR(36) NOT NULL,
    asset_type VARCHAR(20) NOT NULL,
    capacity DECIMAL(10, 2) NOT NULL,
    location VARCHAR(255) NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_maintenance TIMESTAMP,
    total_production DECIMAL(15, 2) DEFAULT 0.00,
    current_production DECIMAL(10, 2) DEFAULT 0.00,
    efficiency DECIMAL(5, 2) DEFAULT 95.00,
    age_months INTEGER DEFAULT 0,
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE,
    CHECK (asset_type IN ('solar', 'wind', 'hydro', 'biomass')),
    CHECK (status IN ('active', 'inactive', 'maintenance')),
    CHECK (efficiency >= 0 AND efficiency <= 100)
);

-- Price History table (for AI predictions)
CREATE TABLE IF NOT EXISTS price_history (
    id SERIAL PRIMARY KEY,
    energy_type VARCHAR(20) NOT NULL,
    price DECIMAL(10, 3) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    volume DECIMAL(10, 2),
    CHECK (energy_type IN ('solar', 'wind', 'hydro', 'biomass'))
);

-- Market Analytics table
CREATE TABLE IF NOT EXISTS market_analytics (
    id SERIAL PRIMARY KEY,
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(15, 2) NOT NULL,
    energy_type VARCHAR(20),
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

-- Create indexes for performance
CREATE INDEX idx_transactions_user_id ON transactions(user_id);
CREATE INDEX idx_transactions_status ON transactions(status);
CREATE INDEX idx_transactions_created_at ON transactions(created_at DESC);
CREATE INDEX idx_transactions_energy_type ON transactions(energy_type);
CREATE INDEX idx_contracts_buyer_id ON smart_contracts(buyer_id);
CREATE INDEX idx_contracts_seller_id ON smart_contracts(seller_id);
CREATE INDEX idx_contracts_status ON smart_contracts(status);
CREATE INDEX idx_assets_owner_id ON energy_assets(owner_id);
CREATE INDEX idx_price_history_energy_type ON price_history(energy_type);
CREATE INDEX idx_price_history_timestamp ON price_history(timestamp DESC);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply trigger to transactions table
CREATE TRIGGER update_transactions_updated_at BEFORE UPDATE ON transactions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert default admin user (password: admin123 - CHANGE IN PRODUCTION)
INSERT INTO users (id, username, email, password_hash, role, wallet_balance)
VALUES (
    'admin-user-id',
    'admin',
    'admin@energyplatform.com',
    -- bcrypt hash of 'admin123'
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyVEk5c0dW4q',
    'admin',
    100000.00
) ON CONFLICT (email) DO NOTHING;
