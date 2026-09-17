-- ============================================================
-- 1. EDITION
-- ============================================================
CREATE TABLE edition (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    tradition VARCHAR(255),
    language VARCHAR(100),
    source_file VARCHAR(500),
    source TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- ============================================================
-- 2. PARVA
-- ============================================================
CREATE TABLE parva (
    id BIGSERIAL PRIMARY KEY,
    edition_id BIGINT NOT NULL,
    number VARCHAR(100),
    name_sanskrit VARCHAR(255),
    name_english VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_parva_edition FOREIGN KEY (edition_id) REFERENCES edition(id) ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE INDEX idx_parva_edition_id ON parva(edition_id);
-- ============================================================
-- 3. CHAPTER
-- ============================================================
CREATE TABLE chapter (
    id BIGSERIAL PRIMARY KEY,
    parva_id BIGINT NOT NULL,
    number VARCHAR(100),
    title TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_chapter_parva FOREIGN KEY (parva_id) REFERENCES parva(id) ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE INDEX idx_chapter_parva_id ON chapter(parva_id);
-- ============================================================
-- 4. CHAPTER TOPIC
-- ============================================================
CREATE TABLE chapter_topic (
    id BIGSERIAL PRIMARY KEY,
    chapter_id BIGINT NOT NULL,
    topic TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_topic_chapter FOREIGN KEY (chapter_id) REFERENCES chapter(id) ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE INDEX idx_topic_chapter_id ON chapter_topic(chapter_id);
-- ============================================================
-- 5. VERSE
-- ============================================================
CREATE TABLE verse (
    id BIGSERIAL PRIMARY KEY,
    chapter_id BIGINT NOT NULL,
    reference VARCHAR(255),
    verse_number VARCHAR(100),
    text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_verse_chapter FOREIGN KEY (chapter_id) REFERENCES chapter(id) ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE INDEX idx_verse_chapter_id ON verse(chapter_id);
CREATE INDEX idx_verse_reference ON verse(reference);
ALTER TABLE parva DROP CONSTRAINT IF EXISTS fk_parva_edition;
ALTER TABLE chapter DROP CONSTRAINT IF EXISTS fk_chapter_parva;
ALTER TABLE chapter_topic DROP CONSTRAINT IF EXISTS fk_topic_chapter;
ALTER TABLE verse DROP CONSTRAINT IF EXISTS fk_verse_chapter;