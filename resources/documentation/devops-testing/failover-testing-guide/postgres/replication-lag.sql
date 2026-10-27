-- PostgreSQL 15+ — replication lag in bytes per standby.
-- Run on the PRIMARY before and during a failover drill.
-- Any lag_bytes > 0 at the moment of promotion means committed data at risk.
SELECT client_addr,
       state,
       sent_lsn,
       write_lsn,
       flush_lsn,
       replay_lsn,
       pg_wal_lsn_diff(sent_lsn, replay_lsn) AS lag_bytes
FROM pg_stat_replication;

-- Optional: streaming lag as a time interval (needs stats on the standby too).
-- SELECT client_addr, replay_lag FROM pg_stat_replication;
