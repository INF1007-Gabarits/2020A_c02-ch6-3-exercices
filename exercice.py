#!/usr/bin/env python
# -*- coding: utf-8 -*-


def check_brackets(text, brackets):
	opening_brackets = dict(zip(brackets[0::2], brackets[1::2]))
	closing_brackets = dict(zip(brackets[1::2], brackets[0::2]))

	bracket_stack = []
	for chr in text:
		if chr in opening_brackets:
			bracket_stack.append(chr)
		elif chr in closing_brackets:
			if len(bracket_stack) == 0 or bracket_stack[-1] != closing_brackets[chr]:
				return False
			bracket_stack.pop()
	return len(bracket_stack) == 0

def remove_comments(full_text, comment_start, comment_end):
	text = full_text
	while True:
		start = text.find(comment_start)
		end = text.find(comment_end)
		if start == -1 and end == -1:
			return text
		if start > end or (start == -1) != (end == -1):
			return None
		text = text[0:start] + text[end + len(comment_end):]

def get_tag_prefix(text, opening_tags, closing_tags):
	for t in zip(opening_tags, closing_tags):
		if text.startswith(t[0]):
			return (t[0], None)
		elif text.startswith(t[1]):
			return (None, t[1])
	return (None, None)

def check_tags(full_text, tag_names, comment_tags):
	text = remove_comments(full_text, *comment_tags)
	if text is None:
		return False

	opening_tags = {f"<{name}>": f"</{name}>" for name in tag_names}
	closing_tags = dict((v, k) for k, v in opening_tags.items())

	tag_stack = []
	while len(text) != 0:
		tag = get_tag_prefix(text, opening_tags, closing_tags)
		if tag[0] is not None:
			tag_stack.append(tag[0])
			text = text[len(tag[0]):]
		elif tag[1] is not None:
			if len(tag_stack) == 0 or tag_stack[-1] != closing_tags[tag[1]]:
				return False
			tag_stack.pop()
			text = text[len(tag[1]):]
		else:
			text = text[1:]
	return len(tag_stack) == 0


if __name__ == "__main__":
	brackets = ("(", ")", "{", "}")
	yeet = "(yeet){yeet}"
	yeeet = "({yeet})"
	yeeeet = "({yeet)}"
	yeeeeet = "(yeet"
	print(check_brackets(yeet, brackets))
	print(check_brackets(yeeet, brackets))
	print(check_brackets(yeeeet, brackets))
	print(check_brackets(yeeeeet, brackets))
	print()

	spam = "Hello, /* OOGAH BOOGAH */world!"
	eggs = "Hello, /* OOGAH BOOGAH world!"
	parrot = "Hello, OOGAH BOOGAH*/ world!"
	print(remove_comments(spam, "/*", "*/"))
	print(remove_comments(eggs, "/*", "*/"))
	print(remove_comments(parrot, "/*", "*/"))
	print()

	otags = ("<head>", "<body>", "<h1>")
	ctags = ("</head>", "</body>", "</h1>")
	print(get_tag_prefix("<body><h1>Hello!</h1></body>", otags, ctags))
	print(get_tag_prefix("<h1>Hello!</h1></body>", otags, ctags))
	print(get_tag_prefix("Hello!</h1></body>", otags, ctags))
	print(get_tag_prefix("</h1></body>", otags, ctags))
	print(get_tag_prefix("</body>", otags, ctags))
	print()

	spam = (
		"<html>"
		"  <head>"
		"    <title>"
		"      <!-- Ici j'ai écrit qqch -->"
		"      Example"
		"    </title>"
		"  </head>"
		"  <body>"
		"    <h1>Hello, world</h1>"
		"    <!-- Les tags vides sont ignorés -->"
		"    <br>"
		"    <h1/>"
		"  </body>"
		"</html>"
	)
	eggs = (
		"<html>"
		"  <head>"
		"    <title>"
		"      <!-- Ici j'ai écrit qqch -->"
		"      Example"
		"    <!-- Il manque un end tag"
		"    </title>-->"
		"  </head>"
		"</html>"
	)
	parrot = (
		"<html>"
		"  <head>"
		"    <title>"
		"      Commentaire mal formé -->"
		"      Example"
		"    </title>"
		"  </head>"
		"</html>"
	)
	tags = ("html", "head", "title", "body", "h1")
	comment_tags = ("<!--", "-->")
	print(check_tags(spam, tags, comment_tags))
	print(check_tags(eggs, tags, comment_tags))
	print(check_tags(parrot, tags, comment_tags))
	print()

