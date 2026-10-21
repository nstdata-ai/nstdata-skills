"""Exercise the standard installer in disposable projects, without calling MCP."""
import os
from pathlib import Path
import shutil
import subprocess
from tempfile import TemporaryDirectory
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = 'nstdata-web-scraping'
FILES = ('SKILL.md', 'LICENSE', 'references/continuation.md')


@unittest.skipUnless(os.getenv('NSTDATA_SKILLS_CLI'), 'Set NSTDATA_SKILLS_CLI to the installed skills CLI entry')
class InstallationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cli = str(Path(os.environ['NSTDATA_SKILLS_CLI']).resolve())
        cls.node = os.getenv('NSTDATA_SKILLS_NODE') or shutil.which('node')
        if not cls.node or not Path(cls.cli).is_file():
            raise RuntimeError('Node and the installed skills CLI are required')

    def run_cli(self, project, *args):
        env = {key: os.environ[key] for key in ('PATH', 'TMPDIR', 'SystemRoot') if key in os.environ}
        env.update(CI='1', DISABLE_TELEMETRY='1', DO_NOT_TRACK='1',
                   XDG_STATE_HOME=str(project / '.installer-state'),
                   XDG_CONFIG_HOME=str(project / '.installer-config'),
                   XDG_CACHE_HOME=str(project / '.installer-cache'))
        result = subprocess.run([self.node, self.cli, *args], cwd=project, env=env,
                                capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result.stdout

    def install(self, project, agent):
        self.run_cli(project, 'add', str(ROOT), '--skill', SKILL, '--agent', agent, '--yes')

    def assert_skill(self, directory, project):
        self.assertTrue(directory.is_dir())
        self.assertTrue(directory.resolve().is_relative_to(project))
        for name in FILES:
            self.assertEqual((directory / name).read_bytes(), (ROOT / SKILL / name).read_bytes())
        self.assertEqual({p.relative_to(directory).as_posix() for p in directory.rglob('*') if p.is_file()}, set(FILES))

    def test_project_install_for_each_documented_agent(self):
        for agent, location in [('cursor', '.agents/skills'), ('claude-code', '.claude/skills')]:
            with self.subTest(agent=agent), TemporaryDirectory() as temp:
                project = Path(temp).resolve()
                config = project / '.cursor/mcp.json'
                config.parent.mkdir()
                config.write_text('{"mcpServers":{"existing":{"command":"existing-server"}}}\n')
                original = config.read_bytes()
                other = project / '.agents/skills/unrelated/SKILL.md'
                other.parent.mkdir(parents=True)
                other.write_text('---\nname: unrelated\ndescription: An unrelated installed skill.\n---\nKeep.\n')
                self.install(project, agent)
                self.assert_skill(project / location / SKILL, project)
                self.assertEqual(config.read_bytes(), original)
                self.assertEqual(other.read_text().splitlines()[-1], 'Keep.')

    def test_reinstall_replaces_only_selected_skill(self):
        with TemporaryDirectory() as temp:
            project = Path(temp).resolve()
            self.install(project, 'cursor')
            other = project / '.agents/skills/unrelated/SKILL.md'
            other.parent.mkdir()
            other.write_text('---\nname: unrelated\ndescription: Unrelated.\n---\nKeep.\n')
            installed = project / '.agents/skills' / SKILL
            self.assert_skill(installed, project)
            (installed / 'SKILL.md').write_text('Old local content')
            (installed / 'obsolete.txt').write_text('Remove on replacement')
            self.install(project, 'cursor')
            self.assert_skill(installed, project)
            self.assertEqual(other.read_text().splitlines()[-1], 'Keep.')

    def test_remove_preserves_other_project_files(self):
        with TemporaryDirectory() as temp:
            project = Path(temp).resolve()
            sentinel = project / 'keep.txt'
            sentinel.write_text('Keep')
            self.install(project, 'cursor')
            other = project / '.agents/skills/unrelated/SKILL.md'
            other.parent.mkdir()
            other.write_text('---\nname: unrelated\ndescription: Unrelated.\n---\nKeep.\n')
            self.run_cli(project, 'remove', SKILL, '--yes')
            self.assertFalse((project / '.agents/skills' / SKILL).exists())
            self.assertEqual(sentinel.read_text(), 'Keep')
            self.assertEqual(other.read_text().splitlines()[-1], 'Keep.')


if __name__ == '__main__':
    unittest.main()
