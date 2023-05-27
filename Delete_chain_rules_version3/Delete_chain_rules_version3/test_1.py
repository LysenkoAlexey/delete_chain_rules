import unittest
import Delete_chain_rules_version3

class test_chain_rules(unittest.TestCase):
    #Замкнут в аксиоме с возможностью выхода
    def test_circle_with_exit(self):
        self.assertEqual(Delete_chain_rules_version3.main_final_try(['S -> S|Sa|a;'], 'S'), ['S -> Sa|a;'])
    #Замкнут только нетерминал
    def test_cirle1(self):
        self.assertEqual(Delete_chain_rules_version3.main_final_try(['S -> S;'], 'S'), [])
    #Замкнут без возможности выхода
    def test_full_cirle(self):
        self.assertEqual(Delete_chain_rules_version3.main_final_try(['S -> S|Sa;'], 'S'), ['S -> Sa;'])
    #Исходные данные не изменяются
    def test_no_change(self):
        self.assertEqual(Delete_chain_rules_version3.main_final_try(['A -> Ba;', 'B -> bbb;', 'C -> c;', 'S -> AB|CD;', 'D -> d;'], 'S'), ['A -> Ba;', 'B -> bbb;', 'C -> c;', 'S -> AB|CD;', 'D -> d;'])
    #Необходимо изменение только в одном правиле
    def test_just_one(self):
        self.assertEqual(Delete_chain_rules_version3.main_final_try(['A -> C;', 'B -> b;', 'C -> c;', 'S -> ABC;'], 'S'), ['A -> c;', 'B -> b;', 'C -> c;', 'S -> ABC;'])
    #Необходимо изменение в ранее измененном правиле
    def test_chain_in_chain(self):
        self.assertEqual(Delete_chain_rules_version3.main_final_try(['A -> B;', 'B -> C;', 'C -> b;', 'S -> ABC;'], 'S'), ['A -> b;', 'B -> b;', 'C -> b;', 'S -> ABC;'])
    #Необходимо изменение в правиле с аксиомой
    def test_in_axiom(self):
        self.assertEqual(Delete_chain_rules_version3.main_final_try(['S -> A;', 'A -> ab;'], 'S'), ['S -> ab;'])
    #Необходимо изменение с логическим оператором "или"
    def test_or(self):
        self.assertEqual(Delete_chain_rules_version3.main_final_try(['S -> A|ab;', 'A -> a;'], 'S'), ['S -> ab|a;'])
    #Изменение в зацикливающихся правилах
    def test_cycle(self):
        self.assertEqual(Delete_chain_rules_version3.main_final_try(['S -> AB;', 'A -> B|a;', 'B -> A'], 'S'), ['S -> AB;', 'A -> a;', 'B -> a;'])
    #Лямбда (пустой терминал) в аксиоме
    def test_lambda_in_axiom(self):
        self.assertEqual(Delete_chain_rules_version3.main_final_try(['A -> B|ab;', 'B -> a|C;', 'C -> b;', 'S -> AB|&;'], 'S'), ['A -> ab|a|b;', 'B -> a|b;', 'S -> AB|&;'])
    #Только правило с аксиомой
    def test_just_axiom(self):
        self.assertEqual(Delete_chain_rules_version3.main_final_try(['S -> b'], 'S'), ['S -> b;'])
    #Только правило с аксиомой и лямбдой
    def test_just_axiom_lambda(self):
        self.assertEqual(Delete_chain_rules_version3.main_final_try(['S -> &'], 'S'), ['S -> &;'])
    #Необходимо удаление недостижимых символов после цепных правил
    def test_delete_unatteinable(self):
        self.assertEqual(Delete_chain_rules_version3.main_final_try(['A -> B|ab;', 'B -> a|C;', 'C -> b;', 'D -> aa', 'S -> A;'], 'S'), ['S -> ab|a|b;'])
    #Из аксиомы нет выхода
    def test_no_enter(self):
        self.assertEqual(Delete_chain_rules_version3.main_final_try(['A -> a'], 'S'), [])
    #Пустые входные данные
    def test_empty(self):
        self.assertEqual(Delete_chain_rules_version3.main_final_try([], 'S'), [])
    #Другая аксиома во входных данных
    def test_different_axiom(self):
        self.assertEqual(Delete_chain_rules_version3.main_final_try(['A -> B|ab;', 'B -> a|C;', 'C -> b;', 'D -> aa'], 'A'), ['A -> ab|a|b;'])
    #Аксиома отсутствует
    def test_no_axiom(self):
        self.assertEqual(Delete_chain_rules_version3.main_final_try(['A -> B|ab;', 'B -> a|C;', 'C -> b;', 'D -> aa'], ''), [])

if __name__ == '__main__':
    unittest.main()
