from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# common knwoledgf, they are all either a knight or a knave but not both
common_knowledge = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave))
)

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    common_knowledge,

    Implication(AKnight, And(AKnight, AKnave)),

    Implication(AKnight, Not(And(AKnight, AKnave))),

)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    common_knowledge,

    Implication(AKnight, And(AKnave, BKnave)),

    Implication(AKnave, Not(And(AKnave, BKnave))),
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    common_knowledge,

    # A
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),

    # B
    Implication(BKnight, Or(And(AKnave, BKnight), And(AKnight, BKnave))),
    Implication(BKnave, Not(Or(And(AKnave, BKnight), And(AKnight, BKnave)))),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    common_knowledge,

    Or(AKnight, AKnave),
    Implication(AKnight, Not(AKnave)),
    Implication(AKnave, Not(AKnight)),

    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Implication(BKnight, Not(BKnave)),
    Implication(BKnave, Not(BKnight)),

    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),
    Implication(CKnight, Not(CKnave)),
    Implication(CKnave, Not(CKnight)),

    # c to a
    Implication(CKnight, AKnight),
    Implication(CKnave, Not(AKnight)),

    # b to c
    Implication(BKnight, CKnave),
    Implication(BKnave, Not(CKnave)),

    # b to a
    Implication(BKnight, Or(Implication(AKnight, AKnave), Implication(AKnave, Not(AKnave)))),
    Implication(BKnave, Or(Implication(AKnave, Not(AKnave)), Implication(AKnight, Not(AKnight)))),
    Implication(AKnight, Or(AKnight, AKnave)),
    Implication(AKnave, Not(Or(AKnight, AKnave)))
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
