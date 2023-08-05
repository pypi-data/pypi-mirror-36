import os

from homotopy import preprocessor, parser, code_generator, snippet_provider, util


class Homotopy:
    """
    Facade class for accessing homotopy tool.
    """
    stdlib_path = os.path.join(os.path.split(__file__)[0], 'stdlib')

    def __init__(self, language):
        """
        Initialize instance.

        :param language: Language
        """
        self.user_path = []
        self.soft_tab = False
        self.soft_tab_size = 4
        self.put_cursor_marker = False
        self.language = language

    def add_lib_folder(self, path):
        """
        Add path to a snippet library

        :param path: Path
        """
        self.user_path.append(path)

    def clear_user_lib(self):
        """
        Clear user lib paths.
        """
        self.user_path.clear()

    def enable_soft_tab(self, tab_size):
        """
        Enable soft tabs and set tab size.

        :param tab_size: Tab size
        """
        self.soft_tab = True
        self.soft_tab_size = tab_size

    def disable_soft_tab(self):
        """
        Disable soft tabs.
        """
        self.soft_tab = False

    def enable_cursor_marker(self):
        """
        Enable cursor marker.
        """
        self.put_cursor_marker = True

    def disable_cursor_marker(self):
        """
        Disable cursor marker.
        """
        self.put_cursor_marker = False

    def set_language(self, language):
        """
        Set language.

        :param language: Language
        """
        self.language = language

    def compile(self, snippet_text):
        """
        Compile a snippet.

        :param snippet_text: Snippet text
        :return: Compiled snippet text
        """
        snippet_provider_instance = snippet_provider.SnippetProvider(
            self.language, self.user_path + [Homotopy.stdlib_path]
        )
        indent_manager_instance = util.IndentManager()

        snippet_text = indent_manager_instance.take_base_indent(snippet_text)

        preprocessor_instance = preprocessor.Preprocessor(snippet_provider_instance)
        compiler_instance = code_generator.CodeGenerator(snippet_provider_instance, indent_manager_instance)
        parser_instance = parser.Parser()

        preprocessed_text = preprocessor_instance.expand_decorators(snippet_text)
        if self.put_cursor_marker:
            preprocessed_text = preprocessor_instance.put_cursor_marker(preprocessed_text)

        syntax_tree = parser_instance.parse(preprocessed_text)
        compiled_snippet = compiler_instance.generate_code(syntax_tree)

        result = indent_manager_instance.indent_base(compiled_snippet)

        if self.soft_tab:
            result = result.expandtabs(self.soft_tab_size)

        return result
