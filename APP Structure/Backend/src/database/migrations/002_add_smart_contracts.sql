-- Add additional smart contract features
-- Migration 002: Enhanced smart contract tracking

-- Add contract events table
CREATE TABLE IF NOT EXISTS contract_events (
    id SERIAL PRIMARY KEY,
    contract_id VARCHAR(36) NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    event_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (contract_id) REFERENCES smart_contracts(id) ON DELETE CASCADE,
    CHECK (event_type IN ('deployed', 'executed', 'verified', 'failed'))
);

-- Add contract metadata
ALTER TABLE smart_contracts 
ADD COLUMN IF NOT EXISTS metadata JSONB;

-- Add failure reason for failed contracts
ALTER TABLE smart_contracts 
ADD COLUMN IF NOT EXISTS failure_reason TEXT;

-- Add block number for blockchain tracking
ALTER TABLE smart_contracts 
ADD COLUMN IF NOT EXISTS block_number INTEGER;

-- Create index on contract events
CREATE INDEX idx_contract_events_contract_id ON contract_events(contract_id);
CREATE INDEX idx_contract_events_created_at ON contract_events(created_at DESC);

-- Add view for contract statistics
CREATE OR REPLACE VIEW contract_statistics AS
SELECT 
    status,
    COUNT(*) as count,
    AVG(execution_time) as avg_execution_time,
    AVG(gas_used) as avg_gas_used,
    SUM(total_value) as total_value
FROM smart_contracts
GROUP BY status;
