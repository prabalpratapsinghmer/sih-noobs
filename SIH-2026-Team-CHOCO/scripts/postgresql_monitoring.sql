-- =====================================================================
-- SIH26184 — PostgreSQL monitoring queries (checklist §5.7)
-- Run as ops:  psql -U sih_admin -d sih26184_app -f scripts/postgresql_monitoring.sql
-- =====================================================================

-- 1. Active sessions
SELECT pid, usename, application_name, state, wait_event_type,
       now() - query_start AS duration, left(query, 80) AS query
FROM pg_stat_activity
WHERE datname = current_database() AND state <> 'idle'
ORDER BY duration DESC;

-- 2. Slow query candidates (longest running)
SELECT pid, now() - query_start AS duration, left(query, 120) AS query
FROM pg_stat_activity
WHERE datname = current_database() AND state = 'active'
ORDER BY duration DESC LIMIT 20;

-- 3. Table sizes + estimated rows
SELECT relname AS table, n_live_tup AS est_rows,
       pg_size_pretty(pg_total_relation_size(relid)) AS total_size
FROM pg_stat_user_tables
ORDER BY pg_total_relation_size(relid) DESC;

-- 4. Connection count vs max
SELECT count(*) AS connections,
       (SELECT setting FROM pg_settings WHERE name = 'max_connections') AS max_connections
FROM pg_stat_activity;

-- 5. Dead tuples (vacuum pressure)
SELECT relname, n_dead_tup, last_vacuum, last_autovacuum
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000 ORDER BY n_dead_tup DESC;

-- 6. Index usage (unused index candidates)
SELECT schemaname, relname, indexrelname, idx_scan, idx_tup_read
FROM pg_stat_user_indexes
WHERE idx_scan = 0 ORDER BY relname;

-- 7. Cache hit ratio (target > 99%)
SELECT sum(heap_blks_hit) / nullif(sum(heap_blks_hit) + sum(heap_blks_read), 0) AS cache_hit_ratio
FROM pg_statio_user_tables;

-- 8. Commit/rollback ratio (transaction health)
SELECT xact_commit, xact_rollback,
       round(xact_rollback * 100.0 / nullif(xact_commit + xact_rollback, 0), 2) AS rollback_pct
FROM pg_stat_database WHERE datname = current_database();

-- 9. Locks (blocked sessions)
SELECT pid, state, wait_event_type, wait_event, left(query, 80) AS query
FROM pg_stat_activity
WHERE wait_event_type IS NOT NULL
ORDER BY wait_event_type, wait_event;