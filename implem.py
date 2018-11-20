from projet import *

GCycle = {
  "Cycle":          UnionRule("Empty", "NonEmpty"),
  "NonEmptyPerms":  ProductRule("Letter", "Perms",lambda l1, l2: l1 + l2),
  "NonEmpty":       BoxProdRule("Letter", "Perms", lambda a, b: (a , b)),
  "Perms":          UnionRule("Empty", "NonEmptyPerms"),
  "Letter":         SingletonRule(lambda x: x),
  "Empty":          EpsilonRule("")
}
init_grammar(GCycle)

assert GCycle["Cycle"].count(0) == 1
assert GCycle["Cycle"].count(1) == 1
assert GCycle["Cycle"].count(2) == 1
assert GCycle["Cycle"].count(3) == 2
assert GCycle["Cycle"].count(4) == 6
assert GCycle["Cycle"].count(5) == 24

OrdBinTrees = {
  "Tree": UnionRule("Node", "Char"),
  "Node": OrdProdRule("Tree", "Tree",lambda l1, l2: l1 + l2),
  "Char": SingletonRule(lambda x: x)
}
init_grammar(OrdBinTrees)

assert OrdBinTrees["Tree"].count(0) == 0
assert OrdBinTrees["Tree"].count(1) == 1
assert OrdBinTrees["Tree"].count(2) == 1
assert OrdBinTrees["Tree"].count(3) == 2
assert OrdBinTrees["Tree"].count(4) == 5
assert OrdBinTrees["Tree"].count(5) == 14

IncrBinTree = {
    "Tree":   UnionRule("Node", "Leaf"),
    "Node":   OrdProdRule("Label", "STree", lambda a, b: (a, b)),
    "Label":  SingletonRule(lambda x: x),
    "STree":  ProductRule("Tree", "Tree", lambda a, b: [a, b]),
    "Leaf" :  EpsilonRule("")
}
init_grammar(IncrBinTree)

assert IncrBinTree["Tree"].count(0) == 1
assert IncrBinTree["Tree"].count(1) == 1
assert IncrBinTree["Tree"].count(2) == 2
assert IncrBinTree["Tree"].count(3) == 6
assert IncrBinTree["Tree"].count(4) == 24
assert IncrBinTree["Tree"].count(5) == 120

ABR = {
    "Tree":   UnionRule("Node", "Leaf"),
    "Node":   BoxProdRule("Label", "STree", lambda a,b: (a, b)),
    "Label":  SingletonRule(lambda x: x),
    "STree":  OrdProdRule("Tree", "Tree", lambda a,b: [a, b]),
    "Leaf" :  EpsilonRule("")
}
init_grammar(ABR)

assert ABR["Tree"].count(0) == 1
assert ABR["Tree"].count(1) == 1
assert ABR["Tree"].count(2) == 2
assert ABR["Tree"].count(3) == 5
assert ABR["Tree"].count(4) == 14
assert ABR["Tree"].count(5) == 42
