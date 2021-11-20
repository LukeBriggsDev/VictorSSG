import regex as re

# REGEX
# whole header including '---' delimiter
header_re = re.compile(r"^-{3}\n[\w\W]+?-{3}")
# header without '---' delimiter
yaml_re = re.compile(r"(?<=^-{3})\n[\w\W]+?(?=-{3})")
# code to be eval in evaluation block
eval_re = re.compile(r"(?<={{)([^{{}}]*)(?=}})")
# whole code including '{{' '}}'
code_re = re.compile(r"({{[^{{}}]*}})")