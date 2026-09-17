import json
from pathlib import Path


# ============================================================
# INPUT / OUTPUT
# ============================================================

input_folder = Path(r"data\output")
output_file = Path(r"data\output\mahabharata_all_tables.txt")


# ============================================================
# TABLES
# ============================================================

editions = []
parvas = []
chapters = []
chapter_topics = []
verses = []


# ============================================================
# IDs
# ============================================================

edition_id = 1
parva_id = 1
chapter_id = 1
topic_id = 1
verse_id = 1


# ============================================================
# READ ALL JSON FILES
# ============================================================

json_files = sorted(
    input_folder.glob("mahabharata-k-*-sa.json")
)

print(f"Found {len(json_files)} JSON files")


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
# WRITE TXT
# ============================================================

with open(output_file, "w", encoding="utf-8") as file:

    # ========================================================
    # EDITION TABLE
    # ========================================================

    file.write("=" * 150 + "\n")
    file.write("EDITION TABLE\n")
    file.write("=" * 150 + "\n")

    file.write(
        f"{'ID':<5} | "
        f"{'Name':<30} | "
        f"{'Tradition':<20} | "
        f"{'Language':<15} | "
        f"{'Source File':<35} | "
        f"{'Source'}\n"
    )

    file.write("-" * 150 + "\n")

    for row in editions:
        file.write(
            f"{str(row['id']):<5} | "
            f"{row['name']:<30} | "
            f"{row['tradition']:<20} | "
            f"{row['language']:<15} | "
            f"{row['source_file']:<35} | "
            f"{row['source']}\n"
        )


    # ========================================================
    # PARVA TABLE
    # ========================================================

    file.write("\n\n")
    file.write("=" * 150 + "\n")
    file.write("PARVA TABLE\n")
    file.write("=" * 150 + "\n")

    file.write(
        f"{'ID':<5} | "
        f"{'Edition FK':<12} | "
        f"{'Number':<10} | "
        f"{'Sanskrit Name':<30} | "
        f"{'English Name'}\n"
    )

    file.write("-" * 150 + "\n")

    for row in parvas:
        file.write(
            f"{str(row['id']):<5} | "
            f"{str(row['edition_id']):<12} | "
            f"{str(row['number']):<10} | "
            f"{row['name_sanskrit']:<30} | "
            f"{row['name_english']}\n"
        )


    # ========================================================
    # CHAPTER TABLE
    # ========================================================

    file.write("\n\n")
    file.write("=" * 150 + "\n")
    file.write("CHAPTER TABLE\n")
    file.write("=" * 150 + "\n")

    file.write(
        f"{'ID':<5} | "
        f"{'Parva FK':<10} | "
        f"{'Number':<10} | "
        f"{'Title'}\n"
    )

    file.write("-" * 150 + "\n")

    for row in chapters:
        file.write(
            f"{str(row['id']):<5} | "
            f"{str(row['parva_id']):<10} | "
            f"{str(row['number']):<10} | "
            f"{row['title']}\n"
        )


    # ========================================================
    # TOPIC TABLE
    # ========================================================

    file.write("\n\n")
    file.write("=" * 150 + "\n")
    file.write("CHAPTER_TOPIC TABLE\n")
    file.write("=" * 150 + "\n")

    file.write(
        f"{'ID':<5} | "
        f"{'Chapter FK':<12} | "
        f"{'Topic'}\n"
    )

    file.write("-" * 150 + "\n")

    for row in chapter_topics:
        file.write(
            f"{str(row['id']):<5} | "
            f"{str(row['chapter_id']):<12} | "
            f"{row['topic']}\n"
        )


    # ========================================================
    # VERSE TABLE
    # ========================================================

    file.write("\n\n")
    file.write("=" * 150 + "\n")
    file.write("VERSE TABLE\n")
    file.write("=" * 150 + "\n")

    file.write(
        f"{'ID':<5} | "
        f"{'Chapter FK':<12} | "
        f"{'Reference':<20} | "
        f"{'Verse No.':<12} | "
        f"{'Text'}\n"
    )

    file.write("-" * 150 + "\n")

    for row in verses:
        file.write(
            f"{str(row['id']):<5} | "
            f"{str(row['chapter_id']):<12} | "
            f"{str(row['reference']):<20} | "
            f"{str(row['verse_number']):<12} | "
            f"{row['text']}\n"
        )


    # ========================================================
    # SUMMARY
    # ========================================================

    file.write("\n\n")
    file.write("=" * 150 + "\n")
    file.write("SUMMARY\n")
    file.write("=" * 150 + "\n")

    file.write(f"JSON files processed : {len(json_files)}\n")
    file.write(f"Editions             : {len(editions)}\n")
    file.write(f"Parvas               : {len(parvas)}\n")
    file.write(f"Chapters             : {len(chapters)}\n")
    file.write(f"Topics               : {len(chapter_topics)}\n")
    file.write(f"Verses               : {len(verses)}\n")


print()
print("=" * 60)
print("DONE")
print("=" * 60)
print(f"Output: {output_file}")
print(f"Files processed: {len(json_files)}")
