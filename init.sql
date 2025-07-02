  CREATE TABLE urls (
     id SERIAL PRIMARY KEY,
     original_url TEXT NOT NULL,
     short_code CHAR(6) UNIQUE,
     created_at TIMESTAMPTZ DEFAULT NOW(),
     expires_at TIMESTAMPTZ,
     access_count INT DEFAULT 0
  );

  // log in to postgres using this command: docker exec -it my-postgres psql -U postgres -d postgres