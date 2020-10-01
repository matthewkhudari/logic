import pytest
from evaluator import Evaluator


example_formulas = {
	'A': (True, True),
	'B': (True, False),
	'C': (False,),
	'': (False,),
	' ': (False,),
	'AB': (False,),
	'(A)': (False,),
	'¬': (False,),
	'∧': (False,),
	'(∧)': (False,),

	'(¬A)': (True, False),
	'(¬B)': (True, True),

	'(A∨A)': (True, True),
	'(A∨B)': (True, True),
	'(B∨A)': (True, True),
	'(B∨B)': (True, False),

	'(A∧A)': (True, True),
	'(A∧B)': (True, False),
	'(B∧A)': (True, False),
	'(B∧B)': (True, False),

	'(A→A)': (True, True),
	'(A→B)': (True, False),
	'(B→A)': (True, True),
	'(B→B)': (True, True),

	'(A↔A)': (True, True),
	'(A↔B)': (True, False),
	'(B↔A)': (True, False),
	'(B↔B)': (True, True),

	'(¬(A↔A))': (True, False),
	'(¬(B∧A))': (True, True),
	'((A∨B)→(B↔(¬A)))': (True, True),
	'((A∨B)→(B↔(¬(¬A))))': (True, False),

	'     ((A∨B)  →(B ↔(¬A)))': (True, True),
	'((A ∨ B) → ( B ↔ (¬(¬A))))  ': (True, False),

	'((A∨B)→(B↔(¬(¬A)))': (False,),
	'((A∨B)→(B↔(¬(¬A)))))': (False,),

	'((A∨B)→(C↔(¬(¬A))))': (False,),
	'((A∨1)→(B↔(¬(¬A))))': (False,),
	'((A∨B)→(B↔(¬(¬AA))))': (False,),
	'()((A∨B)→(B↔(¬(¬A))))': (False,),
}


def test_evaluator_init():
	e = Evaluator()

def test_all_default_symbols():
	e = Evaluator()
	for formula, tup in example_formulas.items():
		assert e.is_well_formed(formula) is tup[0], \
				'is_well_formed({}) should have returned {}'.format(formula, tup[0])
		if tup[0]:
			assert e.is_true(formula) is tup[1], \
				'is_true({}) should have returned {}'.format(formula, tup[1])
			eval_tup = e.evaluate(formula)
			assert eval_tup == tup, \
					'evaluate({}) should have returned {}'.format(formula, tup)
		else:
			assert e.evaluate(formula)[0] is False, \
					'evaluate({})[0] should have returned False'




