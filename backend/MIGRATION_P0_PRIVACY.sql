-- P0 privacy/security migration.
-- Run this before deploying the code that filters on deleted_at.
-- PostgreSQL syntax.

ALTER TABLE users
    ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMP NULL;

ALTER TABLE resumes
    ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMP NULL;

ALTER TABLE job_descriptions
    ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMP NULL;

ALTER TABLE analysis_results
    ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMP NULL;

CREATE INDEX IF NOT EXISTS ix_resumes_user_deleted_created
    ON resumes (user_id, deleted_at, created_at DESC);

CREATE INDEX IF NOT EXISTS ix_analysis_results_user_deleted_created
    ON analysis_results (user_id, deleted_at, created_at DESC);

CREATE INDEX IF NOT EXISTS ix_analysis_results_resume_id
    ON analysis_results (resume_id);

CREATE INDEX IF NOT EXISTS ix_analysis_results_job_description_id
    ON analysis_results (job_description_id);

