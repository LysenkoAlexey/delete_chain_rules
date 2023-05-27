

def parse_rules(rules: list) -> dict:
    parsed_rules = {}
    for rule in rules:
        left, right = rule.rstrip(';').split(' -> ')
        parsed_rules[left] = right.split('|')
    return parsed_rules


def delete_chains(rules: dict, not_terminals: list) -> dict:
    # Удаление цепных правил из грамматики
    # https://neerc.ifmo.ru/wiki/index.php?title=%D0%A3%D0%B4%D0%B0%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5_%D1%86%D0%B5%D0%BF%D0%BD%D1%8B%D1%85_%D0%BF%D1%80%D0%B0%D0%B2%D0%B8%D0%BB_%D0%B8%D0%B7_%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B0%D1%82%D0%B8%D0%BA%D0%B8
    pairs = []
    for c in not_terminals:
        pairs.append((c, c))
    for c in rules.keys():
        for left, right in pairs:
            if right == c:
                for elem in rules[c]:
                    if elem in not_terminals:
                        if elem != c: #Новое, убирает бесконечный цикл при проверке самого себя
                            pairs.append((left, elem))
    new_rules = {}
    for c in rules:
        new_rules[c] = []
    for c in rules:
        for elem in rules[c]:
            if elem not in not_terminals:
                new_rules[c].append(elem)
    for left, right in pairs:
        if left != right:
            new_rules[left].extend(new_rules[right])
    return new_rules


def pretty_rules(rules: dict) -> list:
    result = []
    for c in rules:
        text = '|'.join(rules[c])
        result.append(f'{c} -> {text}')
    return result




def delete_unattainable(currently_checking, rules, not_terminal_symbols, new_not_terminal_symbols):
    for rule in pretty_rules(rules):
        if currently_checking == rule[0]:
            left, right = rule.split(' -> ')
            for ch in right:
                if ch in not_terminal_symbols:
                    if ch not in new_not_terminal_symbols:
                        new_not_terminal_symbols.append(ch)
    return new_not_terminal_symbols




if __name__ == '__main__':
    axiom = 'S'
    rules_inference = ['A -> B|ab;', 'B -> a|C;', 'C -> b;', 'S -> AB;']

    parsed_rules = parse_rules(rules_inference)

    not_terminal_symbols = set(parsed_rules.keys())
    terminal_symbols = set()
    for c in parsed_rules.values():
        for elem in ''.join(c):
            if elem not in not_terminal_symbols:
                terminal_symbols.add(elem)
    
    print('Not terminal symbols:')
    print(' '.join(not_terminal_symbols))
    
    print('Terminal symbols:')
    terminal_symbols.discard('&')
    print(' '.join(terminal_symbols))

    print('Axiom:')
    print(axiom)

    print('Rules:')
    for rule in rules_inference:
        print(rule)
    print('Parsed rules (dictionary)')
    print(parsed_rules)
    print('Rules with deleted chains (dictionary)')
    new_rules = delete_chains(parsed_rules, not_terminal_symbols)
    print(new_rules)

    print('Rules with deleted chains')
    for rule in pretty_rules(new_rules):
        print(rule)

    #Удаление недостижимых символов
    new_checked_rules = []
    new_not_terminal_symbols = []


    new_checked_rules = []
    new_not_terminal_symbols = []
    for rule in pretty_rules(new_rules):
        if rule[0] == axiom:
            new_not_terminal_symbols.append(axiom)
            new_not_terminal_symbols = delete_unattainable(axiom, new_rules,
                not_terminal_symbols, new_not_terminal_symbols)

    print('Not terminal symbols without unattainable')
    print(new_not_terminal_symbols)
    for rule in pretty_rules(new_rules):
        if rule[0] in new_not_terminal_symbols:
            new_checked_rules.append(rule+';')

    for rule in new_checked_rules:
        print(rule)


def main_final_try(rules_inference, axiom):
    parsed_rules = parse_rules(rules_inference)

    not_terminal_symbols = set(parsed_rules.keys())
    terminal_symbols = set()
    for c in parsed_rules.values():
        for elem in ''.join(c):
            if elem not in not_terminal_symbols:
                terminal_symbols.add(elem)


    terminal_symbols.discard('&')

    new_rules = delete_chains(parsed_rules, not_terminal_symbols)

    # Удаление недостижимых символов
    new_checked_rules = []
    new_not_terminal_symbols = []
    for rule in pretty_rules(new_rules):
        if rule[0] == axiom:
            new_not_terminal_symbols.append(axiom)
            new_not_terminal_symbols = delete_unattainable(axiom, new_rules,
                                                                not_terminal_symbols, new_not_terminal_symbols)
    for rule in pretty_rules(new_rules):
        if rule[0] in new_not_terminal_symbols:
            new_checked_rules.append(rule + ';')
    return new_checked_rules