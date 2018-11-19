import math

###                                                                          ###
### ======================================================================== ###
###                                 HELPERS                                  ###
### ======================================================================== ###
###                                                                          ###

def binop(n, k):
  return math.factorial(n) / (math.factorial(k) * math.factorial(n - k))

###                                                                          ###
### ======================================================================== ###
###                           CLASSES & METHODS                              ###
### ======================================================================== ###
###                                                                          ###

class AbstractRule():
  """
  Classe abstraite pour tous les ensembles engendrés par une grammaire.
  """

  def __init__(self):
    """
    Méthode d'initialisation pour tous les ensembles
    """
    self._valuation = math.inf

  def valuation(self):
    return self._valuation

  def _set_valuation(self, v):
    self._valuation = v

  def _set_grammar(self, d):
    self._grammar = d

  def _set_tag(self, t):
    self._tag = t

# !class AbstractRule()



class ConstantRule(AbstractRule):
  """
  Représente un ensemble composé d'un objet unique dont la taille
  est spécifié par la méthode degree
  """

# !class ConstantRule(AbstractRule)




class SingletonRule(ConstantRule):
  """
  Représente un ensemble composé d'un objet unique de taille 1
  """

  def __init__(self, fun):
    """
    Input :
      - fun, la fonction qui construit l'objet depuis l'etiquette
    """
    ConstantRule.__init__(self) # initialisation de la super classe
    self._fun = fun
    self._valuation = 1

  def __repr__(self):
    return "Singleton"

  def fun(self, x):
    """
    Retourne l'objet unique associé à l'ensemble

    Input :

      - x, une étiquette
    """
    return self._fun(x)

  def degree(self):
    return 1

  def count(self, n):
    if n == 1:
      return self.degree()
    return 0

  def list(self, S):
    if len(S) == 1:
      return [self._fun(S[0])]
    return []

# !class SingletonRule(ConstantRule)



class EpsilonRule(ConstantRule):
  """
  Représente un ensemble composé d'un objet unique de taille 0
  """
  def __init__(self, obj):
    """
    Input :
      - obj, l'objet unique appartement à l'ensemble
    """
    AbstractRule.__init__(self) # initialisation de la super classe
    self._obj = obj
    self._valuation = 0

  def obj(self):
    """
    Retourne l'objet unique associé à l'ensemble
    """
    return self._obj

  def __repr__(self):
    return "Epsilon " + str(self.obj())

  def degree(self):
    return 1

  def count(self, n):
    if n == 0:
      return self.degree()
    return 0

  def list(self, lst):
    if len(lst) == 0:
      return [self._obj]
    return []

# !class EpsilonRule(ConstantRule)



class ConstructorRule(AbstractRule):
  """
  Représente un ensemble d'objets construit à partir d'autres ensembles
  """

  def __init__(self, parameters):
    """
    Input :
      - parameters, un tuple contenant les clés identifiant les ensembles
        nécessaires à l'ensemble construit
    """
    AbstractRule.__init__(self)  # initialisation de la super classe
    self._parameters = parameters

  def parameters(self):
    """
    Retourne les paramètres du constructeurs : les clés des ensembles
    nécessaires à l'ensemble construit
    """
    return self._parameters

# !class ConstructorRule(AbstractRule)



class UnionRule(ConstructorRule):
  """
  Représente un ensemble union de deux autres ensembles
  """

  def __init__(self, key1, key2):
    """
    Input :
      - key1, la clé du premier ensemble de l'union
      - key2, la clé du second ensemble de l'union
    """
    ConstructorRule.__init__(self,(key1,key2))

  def __repr__(self):
    return "Union of " + str(self._parameters)

  def count(self, i):
    if i < self.valuation():
      return 0
    kl, kr = self.parameters()
    rule_l, rule_r = [self._grammar[kl], self._grammar[kr]]

    return rule_l.count(i) + rule_r.count(i)

  def list(self, l):
    if len(l) < self.valuation():
      return []
    kl, kr = self.parameters()
    rule_l, rule_r = [self._grammar[kl], self._grammar[kr]]
    return rule_l.list(l) + rule_r.list(l)

# !class UnionRule(ConstructorRule)



class AbstractProductRule(ConstructorRule):
  """
  Représente un ensemble produit de deux autres ensembles
  """
  def __init__(self, key1, key2, cons):
    """
    Input :
      - key1, la clé du premier ensemble du produit
      - key2, la clé du second ensemble du produit
      - cons une fonction prenant deux paramètres : ``òbj1`` un objet
      de l'ensemble ``key1`` et ``obj2`` un objet de l'ensemble
      ``key2``, et renvoyant un objet de l'ensemble produit
    """''
    ConstructorRule.__init__(self,(key1,key2))
    self._cons = cons

  def construct(self, obj1, obj2):
    return self._cons(*(obj1,obj2))

  def count(self, i):
    raise Exception("Should be overriden")

  def iter_label(self, l, k):
    raise Exception("Should be overriden")

  def list(self, l):
    res = []

    kl, kr = self.parameters()
    rule_l, rule_r = [self._grammar[kl], self._grammar[kr]]

    for k in range(rule_l.valuation(), len(l) - rule_r.valuation() + 1):
    # Pour tous les k en fonction des valuations de E1 et E2...

      for lab_l, lab_r in self.iter_label(l, k):
      # Pour tous les découpages possibles de iter_label...

        for elmt_l in rule_l.list(lab_l):
          for elmt_r in rule_r.list(lab_r):
            res.append(self._cons(elmt_l, elmt_r))

    return res


# !class AbstractProductRule(ConstructorRule)



class OrdProdRule(AbstractProductRule):
  """
  Représente un ensemble produit de deux autres ensembles avec labels ordonnés
  """
  def __repr__(self):
    return "Ordered Product of " + str(self.parameters())

  def count(self, i):
    if i < self.valuation():
      return 0

    kl, kr = self.parameters()
    rule_l, rule_r = [self._grammar[kl], self._grammar[kr]]

    res = 0
    for k in range(rule_l.valuation(), i - rule_r.valuation() + 1):
      res += rule_l.count(k) * rule_r.count(i - k)
    return res

  def iter_label(self, l, k):
    if len(l) == 0:
      return []

    if k == 0:
      yield [], l
      return

    l, head = [l.copy(), []]
    l.sort()
    while not len(head) == k:
      head.append(l[0])
      l.remove(l[0])
    yield head, l

# !class OrdProdRule(AbstractProductRule)



class ProductRule(AbstractProductRule):
  """
  Représente un ensemble produit de deux autres ensembles
  """
  def __init__(self, key1, key2, fun):
    AbstractProductRule.__init__(self, key1, key2, fun)
    self._fun = fun
    self._key1 = key1
    self._key2 = key2

  def __repr__(self):
    return "Product of " + str(self.parameters())

  def count(self, i):
    if i < self.valuation():
      return 0

    kl, kr = self.parameters()
    rule_l, rule_r = [self._grammar[kl], self._grammar[kr]]

    res = 0
    for k in range(rule_l.valuation(), i - rule_r.valuation() + 1):
      res += binop(i, k) * rule_l.count(k) * rule_r.count(i - k)
    return res

  def iter_label(self, l, k):
    if len(l) == 0:
      return []

    if k == 0:
      yield [], l

    elif k == 1:
    # Listes contenant chaque élément
      for elmt in l:
        l_ = l.copy()
        l_.remove(elmt)
        yield [elmt], l_

    else:
    # Récursion
      for hd, tl in self.iter_label(l, k - 1):
        for elmt in tl:
          hd_, tl_ = [hd.copy(), tl.copy()]
          tl_.remove(elmt)
          hd_.append(elmt)
          yield hd_, tl_

# !class ProductRule(AbstractProductRule)



class BoxProdRule(AbstractProductRule):
  """
  Représente un ensemble produit de deux autres ensembles avec plus petit
  label à gauche
  """
  #def __init__(self):
  #  self._valuation = 1

  def __repr__(self):
    return "Boxed Product of " + str(self.parameters())

  def count(self, i):
    if i < self.valuation():
      return 0

    kl, kr = self.parameters()
    rule_l, rule_r = [self._grammar[kl], self._grammar[kr]]

    res = 0
    for k in range(max(rule_l.valuation(), 1), i - rule_r.valuation() + 1):
      res += binop(i - 1, k - 1) * rule_l.count(k) * rule_r.count(i - k)
    return res

  def iter_label(self, l, k):
    if len(l) == 0:
      return []
    if k == 0:
      return [], l

    elif k == 1:
    # Liste contenant le plus petit élément
      l.sort()
      elmt = l[0]
      l.remove(elmt)
      yield [elmt], l

    else:
    # Récursion
      for hd, tl in self.iter_label(l, k - 1):
        for elmt in tl:
          hd_, tl_ = [hd.copy(), tl.copy()]
          tl_.remove(elmt)
          hd_.append(elmt)
          yield hd_, tl_

# !class BoxProdRule(AbstractProductRule)

###                                                                          ###
### ======================================================================== ###
###                         EXTERNAL FUNCTIONS                               ###
### ======================================================================== ###
###                                                                          ###


def compute_valuations(gram):
  change = True

  while change:
  # LOOP  ---

    change = False
    for name, rule in gram.items():

      if   isinstance(rule, UnionRule):
      # UNION RULE  ---
        for p in rule.parameters():
          if gram[p].valuation() < rule.valuation():
            rule._set_valuation(gram[p].valuation())
            change = True
      # !UNION RULE ---

      elif isinstance(rule, AbstractProductRule):
      # ABSTRACT PRODUCT RULE  ---
        p1, p2 = rule.parameters()
        if gram[p1].valuation() + gram[p2].valuation() != rule.valuation():
          rule._set_valuation(gram[p1].valuation() + gram[p2].valuation())
          change = True
      # !ABSTRACT PRODUCT RULE ---
  # !LOOP ---


def check_grammar(gram):
  """
  Retourne vrai si toutes les clés utilisées dans les ConstructorRule
  appartiennent bien au dictionnaire de la grammaire.
  """
  for rule in gram.values():
    if isinstance(rule, ConstructorRule):
      for k in rule.parameters():
        if not k in gram.keys():
          return False
  return True


def save_grammar(gram):
  """
  Parcourt les ensembles de la grammaires et leur associe le dictionnaire
  (clé, ensemble) qui constitue la grammaire.

  Input :
    - gram, une grammaire donnée sous forme d'un dictionnaire
  """
  for tag, elmt in gram.items():
    elmt._set_grammar(gram)
    elmt._set_tag(tag)

def init_grammar(gram):
  """
   * Utilise la fonction save_grammar pour enregistrer la grammaire au
     niveau des différents ensembles
   * Vérifie la cohérence de la grammaire avec la fonction check_grammar
     (lève une exception si la fonction renvoie faux)
   * Calcul la valuation sur les ensembles de la grammaire

  Input :
    - gram, une grammaire donnée sous forme d'un dictionnaire clé - ensembles
  """
  if not check_grammar(gram):
    raise RuntimeError("Invalid grammar")

  compute_valuations(gram)
  for k, v in gram.items():
    print(k, v.valuation())
  print()
  save_grammar(gram)

TreeLabelNodes = {
  "Tree" :      UnionRule("Node", "Leaf"),
  "Node" :      ProductRule("Label","Subtrees", lambda l,t: Node(t[0],t[1],l)),
  "Label" :     SingletonRule(lambda x:x),
  "Subtrees" :  ProductRule("Tree","Tree", lambda t1,t2: (t1,t2)),
  "Leaf" :      EpsilonRule(0)
}

init_grammar(TreeLabelNodes)

"""
Liste des classes:

  ConstantRule
  SingletonRule
  EpsilonRule
  ConstructorRule
  UnionRule
  AbstractProductRule
  OrdProdRule
  ProductRule
  BoxProdRule
"""
