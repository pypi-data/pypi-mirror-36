import re

from homotopy.syntax_tree import SnippetVisitor
from homotopy.parser import Parser
from homotopy.util import ContextManager


class CodeGenerator(SnippetVisitor):
    """
    Compiler for snippets. Turns syntax tree into text.
    """
    def __init__(self, snippet_provider, indent_manager):
        self.context_manager = ContextManager()
        self.context_manager.new_scope()
        self.snippet_provider = snippet_provider
        self.indent_manager = indent_manager
        self.inside_parameter = False

    def visit_composite_snippet(self, composite_snippet):
        """
        Generate output for composite snippet.

        :param composite_snippet: Composite snippet
        :return: Text of left side replaced with right side
        """
        left_side = self.visit(composite_snippet.left)
        operation_text = composite_snippet.operation * 3

        if operation_text not in left_side:
            left_side = self.expand_snippet(left_side, operation_text)

        return self.substitute(left_side, composite_snippet.operation, composite_snippet.right, operation_text)

    def visit_simple_snippet(self, simple_snippet):
        """
        Compile simple snippet.

        :param simple_snippet: Simple snippet
        :return: Text of compile snippet
        """
        snippet_text = simple_snippet.value if self.inside_parameter else self.snippet_provider[simple_snippet.value]

        return self.expand_variable_operators(snippet_text)

    def expand_snippet(self, snippet_text, operation_text):
        """
        Expend snippet to uncover possible operator definition.

        :param snippet_text: Snippet text
        :param operation_text: Operation text
        :return: Expanded snippet
        """
        match_found = False

        def expansion_function(match_object):
            nonlocal match_found

            if not match_found and operation_text in self.snippet_provider[match_object.group(1)]:
                match_found = True
                return self.snippet_provider[match_object.group(1)]

            return match_object.group(0)

        return re.sub(
            r'{{([^{]*?)}}',
            expansion_function,
            snippet_text)

    def expand_variable_operators(self, text):
        """
        Expend parameter variables.

        :param text: Text
        :return: Expended text
        """
        return re.sub(
            r'{{[?](.*?)}}',
            lambda match_group: self.context_manager[match_group.group(1)],
            text)

    def substitute(self, left, operation, right_tree, operation_text):
        """
        Replace right site in the appropriate place in the left side.

        :param left: left side value
        :param operation: operation character
        :param right_tree: right side tree
        :param operation_text: operation text in left side value
        :return:
        """
        if operation == Parser.in_operator:
            self.context_manager.new_scope()

            before_operation_text = left[0:left.find(operation_text)]
            m = re.search(r"\n([\t ]*)\Z", before_operation_text)
            indent = m.group(1) if m else ""
        else:
            old_inside_parameter = self.inside_parameter
            self.inside_parameter = True

        right = self.generate_code(right_tree)

        if operation == Parser.in_operator:
            self.context_manager.remove_scope()

            right = self.indent_manager.indent_new_lines(right, indent)
        else:
            self.context_manager.add_variable(operation_text, right)

            self.inside_parameter = old_inside_parameter

        return left.replace(operation_text, right)

    def generate_code(self, snippet):
        """
        Generate code for a snippet. Visit and then perform a clean.

        :param snippet: Snippet
        :return: Text of compiled snippet
        """
        compiled_snippet = self.visit(snippet)

        return re.sub(r'({{[^{]*?}})', "", compiled_snippet)
