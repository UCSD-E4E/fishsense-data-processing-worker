CREATE TABLE IF NOT EXISTS preprocess_jobs (
    "cksum" TEXT PRIMARY KEY,
    "parameters" TEXT NOT NULL,
    "progress" INTEGER NOT NULL DEFAULT 0,
    "priority" INTEGER NOT NULL DEFAULT 99
);
CREATE TABLE IF NOT EXISTS preprocess_with_laser_jobs (
    "cksum" TEXT PRIMARY KEY,
    "parameters" TEXT NOT NULL,
    "progress" INTEGER NOT NULL DEFAULT 0,
    "priority" INTEGER NOT NULL DEFAULT 99
);