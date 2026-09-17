import pandas as pd
import json
from pathlib import Path
from database import insert_df
input_folder = Path(r"data\output")

# ============================================================
# TABLES
# ============================================================

editions = []
parvas = []
chapters = []
chapter_topics = []
verses = []


edition_id = 1
parva_id = 1
chapter_id = 1
topic_id = 1
verse_id = 1


json_files = sorted(
    input_folder.glob("mahabharata-k-*-sa.json")
)


for input_file in json_files:

    print(f"Processing: {input_file.name}")

    with open(input_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    edition = data.get("edition") or {}
    parva = data.get("parva") or {}
    chapters_data = data.get("chapters") or []


    # ========================================================
    # EDITION
    # ========================================================

    current_edition_id = edition_id

    editions.append({
        "id": current_edition_id,
        "name": edition.get("name") or "N/A",
        "tradition": edition.get("tradition") or "N/A",
        "language": edition.get("language") or "N/A",
        "source_file": edition.get("source_file") or input_file.name,
        "source": edition.get("source") or "N/A",
    })

    edition_id += 1


    # ========================================================
    # PARVA
    # FK: edition_id
    # ========================================================

    current_parva_id = parva_id

    parvas.append({
        "id": current_parva_id,
        "edition_id": current_edition_id,
        "number": parva.get("number") or "N/A",
        "name_sanskrit": parva.get("name_sanskrit") or "N/A",
        "name_english": parva.get("name_english") or "N/A",
    })

    parva_id += 1


    # ========================================================
    # CHAPTER
    # FK: parva_id
    # ========================================================

    for chapter in chapters_data:

        current_chapter_id = chapter_id

        chapters.append({
            "id": current_chapter_id,
            "parva_id": current_parva_id,
            "number": chapter.get("number") or "N/A",
            "title": chapter.get("title") or "No title",
        })

        chapter_id += 1


        # ====================================================
        # TOPICS
        # FK: chapter_id
        # ====================================================

        topics = chapter.get("topics") or []

        for topic in topics:

            if isinstance(topic, dict):
                topic_value = topic.get("topic")
            else:
                topic_value = topic

            if not topic_value:
                continue

            chapter_topics.append({
                "id": topic_id,
                "chapter_id": current_chapter_id,
                "topic": str(topic_value),
            })

            topic_id += 1


        # ====================================================
        # VERSES
        # FK: chapter_id
        # ====================================================

        verses_data = chapter.get("verses") or []

        for verse in verses_data:

            verses.append({
                "id": verse_id,
                "chapter_id": current_chapter_id,
                "reference": verse.get("reference") or "N/A",
                "verse_number": verse.get("verse_number") or "N/A",
                "text": verse.get("text") or "No text",
            })

            verse_id += 1


# ============================================================
# DATAFRAMES
# ============================================================

editions_df = pd.DataFrame(editions)

parvas_df = pd.DataFrame(parvas)

chapters_df = pd.DataFrame(chapters)

chapter_topics_df = pd.DataFrame(chapter_topics)

verses_df = pd.DataFrame(verses)


# ============================================================
# LIST ALL DATAFRAMES
# ============================================================

dataframes = {
    "editions": editions_df,
    "parvas": parvas_df,
    "chapters": chapters_df,
    "chapter_topics": chapter_topics_df,
    "verses": verses_df,
}
print(chapters_df)
print("chapters_df")
# inserted = insert_df(editions_df, "edition")
# inserted = insert_df(editions_df, "edition")
# inserted = insert_df(parvas_df, "parva")
# inserted = insert_df(chapters_df, "chapter")
# inserted = insert_df(chapter_topics_df, "chapter_topic")
# inserted = insert_df(verses_df, "verse")
# ============================================================
# DISPLAY ALL DATAFRAMES
# ============================================================
# for name, df in dataframes.items():
#     print(f"\n{name}:")
#     for column in df.columns:
#         print(f"  - {column}")