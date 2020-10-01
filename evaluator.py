import sys

default_symbols = {
	'A': True,
	'B': False,
}

connectives = {
		'∨',
		'∧',
		'¬',
		'→',
		'↔',
	}

class Evaluator():
	"""
	Evaluator of sentential logic formulas.

	Inspired by the course Math 125A at UC Berkeley.

	Supports the following connectives: '∨' (or), '∧' (and), '¬' (not),
	'→' (implies), and '↔' (if and only if).

	Formulas must be provided in standard logical notation, for example::

		'(((A ∨ B) → (¬(C ↔ B))) ∧ A)'


	Attributes
	__________
	symbol_dict: dict of strings to bools
		Contains sentence symbols mapped to truth assignments. All strings
		must have length 1. Must not contain logical symbols (parentheses
		or connectives).


	Methods
	-------
	is_well_formed(formula)
		Verify whether a formula is well-formed.
	is_true(formula)
		Evaluates the truthiness of the provided formula.
	evaluate(formula)
		Verifies whether a formula is well-formed and evaluates
		its truthiness.
	"""

	def __init__(self, symbol_dict=default_symbols.copy()):

		# Validate symbol dict
		if not isinstance(symbol_dict, dict):
			raise TypeError('expected symbol_dict to be type dict,'
						+ 'but instead got {}'.format(type(symbol_dict)))
		print('Symbol dict: ', symbol_dict)

		for symbol, value in symbol_dict.items():

			if not isinstance(symbol, str):
				print('Symbol: ', symbol, ' type: ', type(symbol))
				raise TypeError('expected type of key in symbol_dict to be '
							+ 'str, but instead got {}'.format(type(symbol)))

			if len(symbol) != 1:
				raise ValueError('expected key of symbol_dict to be length 1, '
							+ 'but instead got length {}'.format(len(symbol)))

			if not isinstance(value, bool):
				raise TypeError('expected symbol_dict[{}] to be of type bool, '
							+ 'but instead got type {}'.format(symbol, type(value)))

		self.symbol_dict = symbol_dict

	def is_well_formed(self, formula):
		"""Determines whether or not a formula is well-formed.

		Parameters
		----------
		formula: str
			Formula to validate.

		Raises
		------
		TypeError
			If formula is not a string.

		Returns
		-------
		bool
			True if the formula is well-formed, else False.
		"""

		return self.evaluate(formula)[0]

	def is_true(self, formula):
		"""Determines whether or not a formula is true.

		Formula must be in standard logical notation, for example:

			'(((A ∨ B) → (¬(C ↔ B))) ∧ A)'

		Parameters
		----------
		formula: str
			Formula to evaluate. Formula must be well-formed.

		Raises
		------
		TypeError
			If formula is not a string.
		ValueError
			If formula is not well-formed.

		Returns
		-------
		bool
			True if the formula evaluates to true, else False.
		"""

		is_valid, is_true = self.evaluate(formula)

		# Raise error if formula is not valid
		if not is_valid:
			return ValueError('formula is not valid')

		# If formula is valid, then it is either true or false
		return is_true


	def evaluate(self, formula):
		"""Determines whether a formula is well-formed and true.

		Parameters
		----------
		formula: str
			Formula to evaulate.

		Raises
		------
		TypeError
			If formula is not a string.

		Returns
		-------
		tuple[bool, bool]
			The value at index 0 is True if the formula is well-formed, else
			False. If the formula is well-formed, then the value at index 1 is
			True if the formula evaluates to true, else False. If the formula
			is not well-formed, the value at index 1 may be True or False.
		"""


		# Returns (is_valid, is_true) tuple

		# Check input type
		if not isinstance(formula, str):
			raise TypeError('expected type str, but got {}'.format(type(formula)))

		return self._evaluate(formula)

	def _evaluate(self, formula):

		# Remove whitespace
		formula = ''.join(formula.split())

		# Base case
		if len(formula) == 1:

			# In the base case, symbol must be a sentence variable
			if formula not in self.symbol_dict:
				return (False, False)

			return (True, self.symbol_dict[formula])

		# Alternate invalid base cases
		if len(formula) == 0 or formula[0] != '(' or formula[-1] != ')':
			return (False, False)

		# Recursive case. We evaluate the formula construction tree in a DFS manner
		formula = formula[1:-1]
		paren_depth = 0
		for i in range(len(formula)):
			if formula[i] == '(':
				paren_depth += 1
			elif formula[i] == ')':
				paren_depth -= 1

			if paren_depth == 0 and formula[i] in connectives:
				# We have found the connective corresponding to the outermost
				# set of parentheses.

				# Unary connective case
				if formula[i] == '¬':
					if i != 0:
						return (False, False)
					is_valid, is_true = self._evaluate(formula[1:])
					return (is_valid, not is_true)

				# Binary connective cases
				else:
					left = self._evaluate(formula[:i])
					right = self._evaluate(formula[i+1:])

					# Check if sub-formulas are valid
					if not left[0] or not right[0]:
						return (False, False)

					if formula[i] == '∨':
						return (True, left[1] or right[1])

					elif formula[i] == '∧':
						return (True, left[1] and right[1])

					elif formula[i] == '→':
						return (True, not left[1] or right[1])

					else:
						# formula[i] == '↔'
						return (True, left[1] == right[1])


		# If function has not returned, no connective was found at
		# paren depth of 0.
		return (False, False)




def main():
	# Takes 1 arg, and evaluates with default symbol dict.
	if len(sys.argv) !=  2:
		print('usage: evaluator.py formula')
		return
	e = Evaluator()
	print(e.is_true(sys.argv[1]))


if __name__ == '__main__':
	main()
