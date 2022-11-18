CREATE TABLE users(
    user_id BIGSERIAL PRIMARY KEY,
    first_name VARCHAR(32) NOT NULL,
    phone VARCHAR(14) NULL,
    email VARCHAR(320) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);
