class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.translation = ""


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, translation):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.translation = translation


def build_trie(filename):
    trie = Trie()
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            word, translation = line.strip().split('	')
            trie.insert(word, translation)
    return trie


def generate_cpp_code(trie, indent=0):
    code = ""
    if trie.is_end_of_word:
        code += '    ' * indent + f'cout << "{trie.translation}" << endl;\n'
        code += '    ' * indent + 'return;\n'
    for char, child in trie.children.items():
        code += '    ' * indent + f'if (input[index] == \'{char}\') ' + '{\n'
        code += '    ' * (indent + 1) + f'index++;\n'
        code += generate_cpp_code(child, indent + 1)
        code += '    ' * indent + '}\n'
    return code


filename = "words.txt"
trie = build_trie(filename)
cpp_code = f"""
#include <iostream>
#include <string>
using namespace std;

void find_translation(const string &input, int index) {{
{generate_cpp_code(trie.root)}
    cout << "No translation found" << endl;
}}

int main() {{
    string input;
    cin >> input;
    find_translation(input, 0);
    return 0;
}}
"""
with open("main.cpp", "w") as f:
    f.write(cpp_code)