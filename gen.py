import requests
from datetime import datetime as dt


ENDPOINTS = {
    "departments": "https://api.studentiunimi.it/api/departments",
    "degrees": "https://api.studentiunimi.it/api/degrees"
}


def escape(link):
    ris = link.replace("&", "&amp;")
    ris = ris.replace("'", "&apos;")
    ris = ris.replace("\"", "&quot;")
    ris = ris.replace(">", "&gt;")
    ris = ris.replace("<", "&lt;")
    return ris


def generate_groups():
    ris = []
    deps = requests.get(ENDPOINTS["departments"]).json()
    for dep in deps:
        degrees = requests.get(
            ENDPOINTS["degrees"],
            params=(
                ("dep_id", dep["pk"]),
            )
        ).json()
        for degree in degrees:
            ris.append("https://studentiunimi.it/courses/" + degree["slug"])
    return ris


def write_to(fd, links):
    for link in links:
        fd.write("<url>\n")
        fd.write(f"<loc>{escape(link).strip()}</loc>\n")
        fd.write(f"<lastmod>{dt.now().strftime('%Y-%m-%d')}</lastmod>\n")
        fd.write("</url>\n")


def main():
    fd_o = open("sitemap.xml", "w")
    fd_o.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    fd_o.write("<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n")
    
    with open("base.txt", "r") as fd:
        write_to(fd_o, fd)
    write_to(fd_o, generate_groups())

    fd_o.write("</urlset>")
    fd_o.close()
    print("Done!")


if __name__ == "__main__":
    main()
