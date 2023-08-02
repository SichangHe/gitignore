#!/usr/bin/env python3
Section = tuple[str, list[str]]

L = "\n"


def make_section(section: Section | None, line: str) -> tuple[bool, Section | None]:
    line = line.strip()
    if section is None:
        if line.startswith("#"):
            # Start of new section.
            return False, (line, [])
        else:
            # No section yet.
            return False, None
    else:
        if len(line) == 0:
            # Empty line, end of section.
            return True, section
        else:
            # Add line to section.
            section[1].append(line)
            return False, section


def main():
    sections: list[Section] = []
    section: Section | None = None

    def add_line(line: str):
        nonlocal section, sections
        append, section = make_section(section, line)
        if append:
            assert section is not None
            sections.append(section)
            section = None

    with open(".gitignore", "r") as fd:
        for line in fd.read().splitlines():
            add_line(line)
        add_line("")

    sections.sort(key=lambda s: s[0])
    for section in sections:
        section[1].sort()
    sorted = "\n\n".join(f"{head}\n{L.join(body)}" for head, body in sections)

    with open(".gitignore", "w") as fd:
        fd.write(sorted)


main() if __name__ == "__main__" else None