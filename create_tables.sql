CREATE TABLE ocean_temperatures (
    year INTEGER NOT NULL,
    temperature DECIMAL(6,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_ocean_temps_year ON ocean_temperatures(year);

CREATE TABLE global_temperatures (
    year INTEGER NOT NULL,
    temperature DECIMAL(6,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_global_temps_year ON global_temperatures(year);
        