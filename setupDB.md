This article shows how to setup the database used in valueNotifier.

## Create database and user

```sql
CREATE DATABASE valuenotifier; 

CREATE USER vu WITH ENCRYPTED PASSWORD 'vu101'; 

GRANT ALL PRIVILEGES ON DATABASE valuenotifier TO vu; 

```
Update pg_hba.conf to enable remove connection.

## Create invitation_codes table

```bash
psql -U vu -d valuenotifier
```


```sql
CREATE TABLE invitation_codes ( 

    id SERIAL PRIMARY KEY,         -- Auto-incrementing ID 

    code VARCHAR(255) NOT NULL,    -- The invitation code 

    used BOOLEAN NOT NULL DEFAULT FALSE, -- Indicates if the code is used 

    created_at TIMESTAMP NOT NULL DEFAULT NOW(), -- Timestamp for code creation 

    user_id INTEGER               -- The user who used this invitation ID 

); 
```
