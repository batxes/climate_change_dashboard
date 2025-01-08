CREATE TABLE ocean_temperatures (
    id SERIAL PRIMARY KEY,
    year INTEGER NOT NULL,
    temperature DECIMAL(6,2),
    lower_confidence_interval DECIMAL(6,2),
    upper_confidence_interval DECIMAL(6,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_ocean_temps_year ON ocean_temperatures(year);
        