import subprocess
import sys
import unittest

import helloworld_2


class HelloWorldMissionTests(unittest.TestCase):
    def test_make_sky_places_custom_message_in_middle_row(self) -> None:
        sky = helloworld_2.make_sky(48, height=5, message="Hi, Luna!")

        self.assertEqual(len(sky), 5)
        self.assertIn("Hi, Luna!", sky[2])
        self.assertTrue(all(len(row) <= 48 for row in sky))

    def test_build_manifest_is_deterministic_and_personalized(self) -> None:
        first = helloworld_2.build_manifest(
            message="Hi",
            name="Ada",
            destination="Venus",
            scene="orbit",
        )
        second = helloworld_2.build_manifest(
            message="Hi",
            name="Ada",
            destination="Venus",
            scene="orbit",
        )

        self.assertEqual(first, second)
        self.assertIn(("Commander", "Ada"), first)
        self.assertIn(("Destination", "Venus"), first)
        self.assertIn(("Scene", "orbit"), first)
        self.assertIn(("Payload", "Hi"), first)

    def test_decode_payload_preserves_decoded_message_and_checksum(self) -> None:
        encoded, decoded, checksum = helloworld_2.decode_payload("Az hi!")

        self.assertEqual(encoded, "Hg op!")
        self.assertEqual(decoded, "Az hi!")
        self.assertEqual(checksum, sum(ord(character) for character in "Az hi!"))

    def test_cli_runs_with_plain_text_fallback(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "helloworld_2.py",
                "--fast",
                "--quiet",
                "--message",
                "Hi",
                "--theme",
                "ocean",
                "--scene",
                "landing",
                "--name",
                "Ada",
                "--destination",
                "Neptune",
            ],
            check=True,
            capture_output=True,
            text=True,
        )

        self.assertIn("Commander Ada", result.stdout)
        self.assertIn("Neptune", result.stdout)
        self.assertIn("Mini-scene: landing", result.stdout)
        self.assertNotIn("\033[", result.stdout)


if __name__ == "__main__":
    unittest.main()
