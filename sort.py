#!/usr/bin/env python3
Sections = dict[str, set[str]]

L = "\n"


def make_section(
    sections: Sections, section: set[str] | None, line: str
) -> set[str] | None:
    line = line.strip()
    if section is None:
        if line.startswith("#"):
            # Start of new section.
            sections[line] = set()
            return sections[line]
        else:
            # No section yet.
            return None
    else:
        if len(line) == 0:
            # Empty line, end of section.
            return None
        else:
            # Add line to section.
            section.add(line)
            return section


def main():
    sections: Sections = {}
    section: set[str] | None = None

    def add_line(line: str):
        nonlocal section, sections
        section = make_section(sections, section, line)

    with open(".gitignore", "r") as fd:
        for line in fd.read().splitlines():
            add_line(line)
        add_line("")

    sections_list = list(sections.items())
    sections_list.sort(key=lambda s: s[0])
    sorted_sections = []
    for head, body in sections_list:
        section_list = list(body)
        section_list.sort()
        sorted_sections.append(f"{head}\n{L.join(section_list)}")
    sorted = "\n\n".join(sorted_sections)

    with open(".gitignore", "w") as fd:
        fd.write(sorted)


main() if __name__ == "__main__" else None
