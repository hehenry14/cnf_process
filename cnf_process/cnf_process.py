from sympy.logic.boolalg import to_cnf
from sympy.parsing.sympy_parser import parse_expr
import logging


def __count_char__(string: str, char: str) -> bool:
    """
    This function counts amount of char in the string
    :param string: the string to be checked
    :param char: the char to be checked
    :return: amount of char in string, example there are 3 & in "variable & B &C&D".
    """
    return string.count(char)


def __count_word__(string: str, word: str) -> int:
    """
    This function counts amount of word in the string, i.e. there are 1 & in "variable & B &C&D"
    :param string: the string to be checked
    :param word: the word to be checked
    :return: the number of word in string
    """
    return string.split().count(word)


def __has_valid_op__(string1: str) -> bool:
    """
    This function checks if the string's operators are separated by space.
    :param string1: the string to be checked
    :return: check result
    """
    if not __count_char__(string1, '&') == __count_word__(string1, '&'):
        return False
    if not __count_char__(string1, '|') == __count_word__(string1, '|'):
        return False
    return True


class CNFStatement():
    """ variable CNF statement object, it will translate a normal string into a sympy boolean expression in the
     Conjunctive normal form, and CNFStatement.reduce() function can simply the result by fill in the boolean result
     of an variable.
    """

    def __init__(self, input_string: str):
        """
        Constructor for the CNFStatement.
        :param input_string: the string form of the CNF statement i.e. '(variable & D) | (~B & C | (G & F))'
        """
        self.logger = logging.getLogger('CNFStatement')
        self.math_statement = None
        if not self.is_valid_statement(input_string):
            raise ValueError('The input string violated input specification, please check the log message for detail.')
        # translate the string and self.math_statement =  self.translate(input_string)
        self.translate(input_string)

    def is_valid_statement(self, input_string: str) -> bool:
        """
        This function validates
        :param input_string: the input string i.e. '(variable & D) | (~B & C | (G & F))'
        inv:

        # input_string cannot be an empty string, 'E', 'I', 'O', 'S', 'N'.

        # input_string cannot have following symbols: ['`', '-', '=', '[', ']', '\\', ';', "'", ',', '.', '/', '!', '@',
         '#', '$', '%', '^', '*', ':', '<', '>', '?', '·', '+', '"']

        # input_string cannot start with a number or '_'

        # variable names must at least have one letter

        # variable names cannot start with a number.

        # the length of each variable should be no longer than 32 characters.

        :return: whether the input_string is a valid string
        """

        if input_string == "" or len(input_string.split()) == 0:
            self.logger.log(level=3, msg='string is empty')
            return False

        # Check if the string have forbidden characters
        if not self.__is_valid_string_sym__(input_string):
            return False

        # Check if 'E', 'I', 'O', 'S', 'N' is in the string
        if ' E ' in input_string or ' I ' in input_string or ' S ' in input_string or ' O ' in input_string or ' N ' in input_string:
            self.logger.log(level=3, msg='element id have following letters as a single check id: E,N,S,I,O')
            return False

        # Check if the string starts with numbers or _
        words = input_string.split()
        if not self.__is_valid_word_list__(words):
            return False

        # Check if | and & are all separate by space
        if not __has_valid_op__(input_string):
            self.logger.log(level=3, msg='the operator | and & should be separate by space before and after t'
                                         'he element id, it is violated in given statement: ' + input_string)
            return False

        # Check if the string has at least 1 letters:
        if not any(c.isalpha() for c in input_string):
            self.logger.log(level=3,
                            msg='the operator must contains 1 letters it is violated '
                                'in given statement: ' + input_string)
            return False

        # Check if the string ends with operators:
        if words[len(words) - 1] == '&' or words[len(words) - 1] == '|':
            self.logger.log(level=3, msg="the statement cannot end with & or ||, it is violated "
                                         "in given statement: " + input_string)
            return False

        # Check if the string starts with operators:
        if words[0] == '&' or words[0] == '|':
            self.logger.log(level=3, msg="the statement cannot start with & or |, it is violated"
                                         " in given statement: " + input_string)
            return False

        if not self.__check_length__(words):
            return False
        return True

    def __is_valid_string_sym__(self, string1: str) -> bool:
        """
        This function checks if the string has words has forbidden symbols.
        :param string1: the string to be checked.
        :return: True if there is a invalid char in string1.
        """
        for i in ['`', '-', '=', '[', ']', '\\', ';', "'", ',', '.', '/', '!', '@', '#', '$', '%', '^', '*', ':',
                  '<', '>', '?', '·', '+', '"']:
            if i in string1:
                self.logger.log(level=3,
                                msg='element id in' + string1 +
                                    ' have forbidden special characters: ' + i)
                return False
        if '"' in string1:
            return False
        return True

    def __is_valid_word_list__(self, word_list: list) -> bool:
        """
        This function checks if the word list has words starts with numbers or _.
        :param word_list: the world list to be checked
        :return: check result
        """
        for word in word_list:
            for i in '0123456789_':
                if word.startswith(i):
                    self.logger.log(level=3, msg='word starts with 0123456789_')
                    return False
        return True

    def __check_length__(self, words: list) -> str:
        """
        This function checks if the element id is shorter than 32 characters
        :param words: a list of word to be examined
        :return:  if the words has a element longer out of 1 to 32 characters range return False
        """
        for w in words:
            if len(w) < 1 or len(w) > 32:
                self.logger.log(level=3, msg=w + ' is out of range')
                return False
        return True

    def translate(self, string: str):
        """
        This function takes a boolean statement in string format and transform it into the boolean statement.
        :param string: he string of boolean statement
        :return: the sympy expr object translated from the string.
        """
        string1 = string.replace('not', '~')
        expr = to_cnf(parse_expr(string1))
        self.logger.log(level=1, msg=' is out of range')
        self.math_statement = expr

    def evaluate(self, variable: str, result: bool):
        """
        This function take a input and simplify the boolean expr with the result of one of the proposition.
        :param variable: the variable to be evaluated.
        :param result: the result of variable
        :return: the conjunctive normal form expression after the variable's result has be evaluated
        """
        expr = self.math_statement
        variable = variable.strip()
        if not isinstance(result, bool):
            self.logger.log(level=3, msg='result is not a Boolean')
            raise ValueError('result is not a Boolean')

        if result:
            expr = expr.subs({variable: result})
        else:
            expr = expr.subs(variable, 0)
        self.math_statement = expr
        return expr

    def get_current_expression_in_string(self) -> str:
        """
        Returns the current boolean cnf expression in string format
        :return: str(self.math_statement)
        """
        return str(self.math_statement)
