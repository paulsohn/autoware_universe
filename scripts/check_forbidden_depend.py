#!/usr/bin/env python3
import sys
import xml.etree.ElementTree as ET

FORBIDDEN_PKGS = ["autoware_launch"]


def is_dependency_tag(tag: str) -> bool:
    return tag.endswith("depend")


def main() -> int:
    files = sys.argv[1:]
    failed = False

    for file_path in files:
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()

            # iterate through all elements in the XML tree
            for element in root.iter():
                tag_name = element.tag

                if not is_dependency_tag(tag_name):
                    continue

                if not element.text:
                    continue

                dependency = element.text.strip()
                if dependency in FORBIDDEN_PKGS:
                    print(
                        f"❌ Forbidden dependency '<{tag_name}>{dependency}</{tag_name}>' found in {file_path}"
                    )
                    failed = True

        except ET.ParseError:
            print(f"⚠️  Could not parse XML: {file_path}")
            failed = True
            continue

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
