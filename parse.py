import glob
import json
import psycopg


def create_table():
    with psycopg.connect("host=localhost dbname=mydb user=postgres password=postgres") as conn:
        with conn.cursor() as cur:
            cur.execute(
                "CREATE TABLE articles (id serial PRIMARY KEY, title text, parsed_data text)"
            )
            conn.commit()


def add_search_index():
    with psycopg.connect("host=localhost dbname=mydb user=postgres password=postgres") as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                ALTER TABLE articles ADD COLUMN search_vector tsvector
                GENERATED ALWAYS AS (
                    to_tsvector(
                        'english',
                        coalesce(title, '') || ' ' || coalesce(parsed_data, '')
                    )
                ) STORED;
                """
            )
            conn.commit()

def parse_json_into_table():
    json_files = glob.glob("data/*.json")

    for json_file in json_files:
        with open(json_file) as input_file:
            data = json.load(input_file)

            title = data["Title"]
            intro = "\n".join(data["Opening"]["Introduction"])


            del data["Title"]
            del data["Opening"]

            sub_headings = data.keys()



            gem_text = f"""

# {title}

{intro}
"""
            for sub in sub_headings:
                paragraphs = "\n\n".join(
                    paragraph
                    for key in data[sub]
                    for paragraph in data[sub][key]
                    if len(paragraph.strip()) != 0
                )
                gem_text += f"""
## {sub}

{paragraphs}
"""

        with psycopg.connect("host=localhost dbname=mydb user=postgres password=postgres") as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    INSERT INTO articles (title, parsed_data)
                    VALUES (%s, %s)
                    """, (title, gem_text)
                )
                conn.commit()


if __name__ == "__main__":
    # create_table()
    # add_search_index()
    parse_json_into_table()
