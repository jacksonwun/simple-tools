import os
import time
import xml.etree.ElementTree as ET

# Configuration
DOMAIN = "mytool.agency"
SCAN_DIRECTORY = "."  # Change to your local site folder
OUTPUT_FILE = "sitemap.xml"
FREQ = "daily"  # Options: always, hourly, daily, weekly, monthly, yearly, never
PRIORITY = "0.8"  # Adjust based on importance

def get_file_mod_time(filepath):
    """Get last modified time of file in ISO format."""
    mod_time = time.gmtime(os.path.getmtime(filepath))
    return time.strftime("%Y-%m-%dT%H:%M:%S+00:00", mod_time)

def generate_sitemap():
    """Scan directory and generate sitemap.xml"""
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

    for root, _, files in os.walk(SCAN_DIRECTORY):
        for file in files:
            if file.endswith(".html"):
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, SCAN_DIRECTORY)
                url = f"{DOMAIN}/{relative_path.replace(os.sep, '/')}"
                
                # Create URL entry
                url_elem = ET.SubElement(urlset, "url")
                ET.SubElement(url_elem, "loc").text = url
                ET.SubElement(url_elem, "lastmod").text = get_file_mod_time(full_path)
                ET.SubElement(url_elem, "changefreq").text = FREQ
                ET.SubElement(url_elem, "priority").text = PRIORITY

    # Save XML file
    tree = ET.ElementTree(urlset)
    with open(OUTPUT_FILE, "wb") as f:
        tree.write(f, encoding="utf-8", xml_declaration=True)
    
    print(f"Sitemap generated: {OUTPUT_FILE}")

# Run the script
if __name__ == "__main__":
    generate_sitemap()
