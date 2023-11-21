def format_program(program: dict) -> dict:
    program.pop("createdAt", None)
    program.pop("id", None)
    program.pop("isPinned", None)
    program.pop("title", None)

    program["sections"] = format_sections(program.get("sections"))

    return program


def format_sections(sections: list) -> list:
    updated_sections = []

    for i in range(len(sections)):
        section: dict = sections[i]
        section["number"] = i + 1
        section.pop("id", None)

        section["themes"] = format_themes(section.get("themes"))
        updated_sections.append(section)

    return updated_sections


def format_themes(themes: list) -> list:
    updated_themes = []

    for i in range(len(themes)):
        theme: dict = themes[i]

        theme.pop("id", None)
        theme["number"] = i + 1

        theme["independents"].pop("isHidden", None)
        theme["laboratorys"].pop("isHidden", None)
        theme["practicals"].pop("isHidden", None)
        theme["theoreticals"].pop("isHidden", None)

        for j in range(len(theme["independents"]["lessons"])):
            independents = theme["independents"]["lessons"]
            independents[j].pop("id", None)
            independents[j]["number"] = j + 1

        for j in range(len(theme["laboratorys"]["lessons"])):
            independents = theme["laboratorys"]["lessons"]
            independents[j].pop("id", None)
            independents[j]["number"] = j + 1

        for j in range(len(theme["practicals"]["lessons"])):
            independents = theme["practicals"]["lessons"]
            independents[j].pop("id", None)
            independents[j]["number"] = j + 1

        for j in range(len(theme["theoreticals"]["lessons"])):
            independents = theme["theoreticals"]["lessons"]
            independents[j].pop("id", None)
            independents[j]["number"] = j + 1

        updated_themes.append(theme)

    return updated_themes
