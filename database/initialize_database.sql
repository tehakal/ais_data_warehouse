
SELECT 'CREATE DATABASE willhaben_prop WITH OWNER postgres' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '‘willhaben_prop');