import unittest
import os
from path import validate_input


class PathValidatingTest(unittest.TestCase):
    def test_input_validating(self):
        # File w\o extension
        absolute_path = os.path.abspath("./test/log")
        self.assertEqual(validate_input(absolute_path), None)

        # Nontarget file extension
        absolute_path = os.path.abspath("./test/text.txt")
        self.assertEqual(validate_input(absolute_path), None)

        # Target file
        absolute_path = os.path.abspath("./test/Sysmon.evtx")
        self.assertEqual(
            validate_input(absolute_path),
            "C:\\Users\\oidaho\\VSCode Projects\\evtx-viewer-cli\\test\\Sysmon.evtx",
        )

        # Target file via different name
        absolute_path = os.path.abspath("./test/Security.evtx")
        self.assertEqual(
            validate_input(absolute_path),
            "C:\\Users\\oidaho\\VSCode Projects\\evtx-viewer-cli\\test\\Security.evtx",
        )

        # Wrong extension
        absolute_path = os.path.abspath("./test/log") + "awdw"
        self.assertEqual(validate_input(absolute_path), None)

        # Non-existent path
        absolute_path = os.path.abspath("./test/log").replace("test", "guns")
        self.assertEqual(validate_input(absolute_path), None)

        # Target directory via EVTX files
        absolute_path = os.path.abspath("./test/")
        self.assertEqual(
            validate_input(absolute_path),
            [
                "C:\\Users\\oidaho\\VSCode Projects\\evtx-viewer-cli\\test\\Security.evtx",
                "C:\\Users\\oidaho\\VSCode Projects\\evtx-viewer-cli\\test\\Sysmon.evtx",
            ],
        )

        # Target directory w\o EVTX files
        absolute_path = os.path.abspath("./parser/")
        self.assertEqual(validate_input(absolute_path), None)


if __name__ == "__main__":
    unittest.main()
