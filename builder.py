from sublime import platform
from sublime_plugin import WindowCommand
from os.path import split as split_path

is_windows = platform() == "windows"
path_separator = "\\" if is_windows else "/"


class PythonicBuilderCommand(WindowCommand):
    def run(self, **kwargs):
        parent, file_name = self._get_current_file()
        python = self._get_python()

        if file_name.startswith("test_"):
            kwargs["working_dir"] = parent
            _, parent_name = split_path(parent)
            file_name = parent_name + path_separator + file_name
            flags = "-m unittest"
        else:
            flags = "-u"

        shell_cmd = " ".join([python, flags, file_name])
        kwargs["shell_cmd"] = shell_cmd
        self.window.run_command("exec", kwargs)

    def _get_current_file(self):
        return split_path(self._get_view().file_name())

    def _get_python(self) -> str:
        return self._get_view().settings().get("python_path", "python")

    def _get_view(self):
        return self.window.active_view()
