from urllib.parse import urlparse
import random
import string
from urllib.parse import urlparse

# Memory stores
short_to_long = {}
long_to_short = {}

# Short code generator
def generate_short_code(length=3):
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choices(characters, k=length))

# Extract keyword from domain
def get_short_keyword(url):
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    if "facebook" in domain:
        return "fb"
    elif "youtube" in domain:
        return "yt"
    elif "google" in domain:
        return "gg"
    elif "twitter" in domain:
        return "tw"
    elif "linkedin" in domain:
        return "li"
    elif "instagram" in domain:
        return "ig"
    else:
        domain = domain.replace("www.", "")
        return domain[:2]

# Shorten a long URL
def shorten_url(long_url):
    if long_url in long_to_short:
        return long_to_short[long_url] 
    
    keyword = get_short_keyword(long_url)
    while True:
        code = keyword + generate_short_code()
        short_url = f"https://{code}short.ly"
        if short_url not in short_to_long:
            break
    
    # Store the relationship
    short_to_long[short_url] = long_url
    long_to_short[long_url] = short_url
    
    return short_url

# Retrieve long URL
def expand_url(short_url):
    return short_to_long.get(short_url, "❌ Short URL not found.")

# Main menu
def main():
    while True:
        print("\n====== URL Shortener ======")
        print("1. Shorten a URL")
        print("2. Expand a URL")
        print("3. Exit")

        choice = input("Choose an option (1/2/3): ")

        if choice == "1":
            long_url = input("Enter the long URL: ")
            short = shorten_url(long_url)
            print("Shortened URL:", short)

        elif choice == "2":
            short_url = input("Enter the short URL to expand: ")
            original = expand_url(short_url)
            print("🔗 Original URL:", original)

        elif choice == "3":
            print("Scrappy!")
            break

        else:
            print("Invalid choice. Try again.")

# Run the program
main()
