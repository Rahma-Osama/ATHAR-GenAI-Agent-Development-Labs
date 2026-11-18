
import os
import json
import re
import webbrowser
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional

import requests
from dotenv import load_dotenv


# ==========================================
# 1. Configuration
# ==========================================

load_dotenv()

API_KEY = os.getenv("NASA_API_KEY")
BASE_URL = "https://science.nasa.gov/wp-json/wp/v2/apod-basic/"

DATA_DIR = Path("data")
IMAGES_DIR = DATA_DIR / "images"
JSON_DIR = DATA_DIR / "saved_pictures"

TIMEOUT = 20


# ==========================================
# 2. Data Model
# ==========================================

@dataclass
class AstronomyPicture:
    title: str
    date: str
    explanation: str
    media_type: str
    image_url: Optional[str]
    copyright: str = "Not available"

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            title=data.get("title", "Untitled"),
            date=data.get("date", "Unknown"),
            explanation=data.get("explanation", "No explanation available."),
            media_type=data.get("media_type", "Unknown"),
            image_url=data.get("hdurl") or data.get("url"),
            copyright=data.get("copyright") or "Not available"
        )

    def display(self):

        print("\n" + "=" * 65)
        print("                 NASA ASTRONOMY PICTURE")
        print("=" * 65)

        print(f"Title      : {self.title}")
        print(f"Date       : {self.date}")
        print(f"Media Type : {self.media_type}")
        print(f"Copyright  : {self.copyright}")

        print("\nExplanation:")
        print("-" * 65)
        print(self.explanation)

        print("\nImage URL:")
        print(self.image_url or "Not available")

        print("=" * 65)


# ==========================================
# 3. API Service
# ==========================================

def fetch_pictures():

    if not API_KEY:
        print("Error: NASA_API_KEY is missing from .env file.")
        return []

    try:
        print("\nFetching astronomy pictures...")

        response = requests.get(
            BASE_URL,
            params={"api_key": API_KEY},
            timeout=TIMEOUT
        )

        response.raise_for_status()

        data = response.json()

        if not isinstance(data, list):
            print("Error: Unexpected API response format.")
            return []

        if not data:
            print("No pictures found.")
            return []

        pictures = [
            AstronomyPicture.from_dict(item)
            for item in data
            if isinstance(item, dict)
        ]

        print(f"Successfully retrieved {len(pictures)} pictures.")

        return pictures

    except requests.exceptions.Timeout:
        print("Error: Request timed out.")

    except requests.exceptions.ConnectionError:
        print("Error: Check your internet connection.")

    except requests.exceptions.HTTPError as error:
        print(f"HTTP Error: {error}")

    except requests.exceptions.RequestException as error:
        print(f"Request Error: {error}")

    except ValueError:
        print("Error: The API returned invalid JSON.")

    return []


# ==========================================
# 4. Display Pictures
# ==========================================

def display_all_pictures(pictures):

    print("\nAVAILABLE ASTRONOMY PICTURES")
    print("-" * 65)

    for index, picture in enumerate(pictures, start=1):

        print(f"{index}. {picture.title} ({picture.date})")


def select_picture(pictures):

    display_all_pictures(pictures)

    try:
        choice = int(input("\nSelect picture number: "))

        if 1 <= choice <= len(pictures):
            return pictures[choice - 1]

        print("Invalid selection.")

    except ValueError:
        print("Please enter a valid number.")

    return None


# ==========================================
# 5. Save Picture Information as JSON
# ==========================================

def save_picture(picture):

    JSON_DIR.mkdir(parents=True, exist_ok=True)

    filename = f"{picture.date}.json"
    file_path = JSON_DIR / filename

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(
            asdict(picture),
            file,
            indent=4,
            ensure_ascii=False
        )

    print(f"Picture information saved to: {file_path}")


# ==========================================
# 6. Download Image
# ==========================================

def download_image(picture):

    if not picture.image_url:
        print("No image URL available.")
        return

    if picture.media_type.lower() != "image":
        print("This content is not an image.")
        return

    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    safe_title = re.sub(
        r'[<>:"/\\|?*]',
        "_",
        picture.title
    )

    file_path = IMAGES_DIR / f"{safe_title}.jpg"

    try:
        response = requests.get(
            picture.image_url,
            timeout=TIMEOUT,
            stream=True
        )

        response.raise_for_status()

        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)

        print(f"Image downloaded successfully: {file_path}")

    except requests.exceptions.RequestException as error:
        print(f"Download failed: {error}")


# ==========================================
# 7. Open Image in Browser
# ==========================================

def open_image(picture):

    if not picture.image_url:
        print("No media URL available.")
        return

    if not picture.image_url.startswith(("https://", "http://")):
        print("Invalid media URL.")
        return

    webbrowser.open(picture.image_url)


# ==========================================
# 8. Interactive Menu
# ==========================================

def main():

    pictures = fetch_pictures()

    if not pictures:
        return

    while True:

        print("\n" + "=" * 45)
        print("       NASA ASTRONOMY EXPLORER")
        print("=" * 45)

        print("1. Display all pictures")
        print("2. View picture details")
        print("3. Save picture information as JSON")
        print("4. Download picture")
        print("5. Open picture in browser")
        print("6. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            display_all_pictures(pictures)

        elif choice in ("2", "3", "4", "5"):

            picture = select_picture(pictures)

            if picture is None:
                continue

            if choice == "2":
                picture.display()

            elif choice == "3":
                save_picture(picture)

            elif choice == "4":
                download_image(picture)

            elif choice == "5":
                open_image(picture)

        elif choice == "6":
            print("\nThank you for exploring NASA Astronomy Pictures!")
            break

        else:
            print("Invalid choice. Please try again.")


# ==========================================
# 9. Application Entry Point
# ==========================================

if __name__ == "__main__":
    main()
