import requests
import time
import json
import re
import wikipedia

wikipedia.set_user_agent("Archival-Attempt/1.0 (I will not abuse, thank you !)")

queue = ["Baruch Spinoza"]
seen = set()

def scrape(link: str):

    parser = {"Title": link, "Opening": {"Introduction": []} }

    page = wikipedia.page(link)

    lines = page.content.split("\n")
    main_heading = r"^== (.*?) ==$"
    sub_heading = r"^=== (.*?) ===$"

    current_heading = "Opening"
    current_sub_heading = "Introduction"

    for line in lines:
        main_heading_match = re.match(main_heading, line.strip())
        sub_heading_match = re.match(sub_heading, line.strip())
        if len(line) == 0:
            continue
        if main_heading_match:
            heading = main_heading_match.group(1)
            current_heading = heading
            parser[current_heading] = {"Base": []}
            current_sub_heading = "Base"
        elif sub_heading_match:
            heading = sub_heading_match.group(1)
            current_sub_heading = heading
            parser[current_heading][current_sub_heading] = []
        else:
            parser[current_heading][current_sub_heading].append(line)

    with open(f"data/{link}.json", "w") as output:
        json.dump(parser, output, indent=4, sort_keys=True)

    seen.add(link)
    for link in page.links:
        if link not in seen:
            queue.append(link)
            seen.add(link)

if __name__ == "__main__":
    while True:
        time.sleep(30)
        link = queue.pop(0)
        try:
            scrape(link)
        except Exception as e:
            print("Failed:", link)
            queue.append(link)
            continue
