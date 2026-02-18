---
source: ethresearch
topic_id: 10882
title: "\"Mutable Forest\" Memory Model for blockchain specs"
author: ericsson49
date: "2021-09-28"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/mutable-forest-memory-model-for-blockchain-specs/10882
views: 3140
likes: 7
posts_count: 11
---

# "Mutable Forest" Memory Model for blockchain specs

## TL;DR

[Ethereum PoS Consensus pyspecs](https://github.com/ethereum/consensus-specs) are expressed using destructive (i.e. in-place) memory updates. Reasoning about such updates can be complicated due to [aliasing](https://en.wikipedia.org/wiki/Aliasing_(computing)). However, in-place updates are (much) faster and often more readable. These two aspects are important, since the pyspecs are executable and employ nested data structures quite intensively.

The core problem is that a destructive update of a location can affects other parts of code via aliased references. Often unintended, such update can break invariants and assumptions throughout the entire codebase. Therefore, it’s important to limit aliasing - ideally, one should make updates via exclusive references only. Such “exclusive mutable reference” form can be translated to a pure form without much code blowup (as there is no aliases to propagate updates to).

The *exclusive mutable reference* requirement may seem too severe, however, a practical implementation can allow for richer forms of aliasing, transforming them to the *exclusive mutable reference* form under the hood (or rejecting the program, if such reduction is not possible).

Moreover, destructive updates via non-exclusive references can be dangerous and thus inappropriate, in the sense that they introduce opportunities for bugs (e.g. a missing copy operation). Ensuring that any mutable reference is exclusive prevents certain class of bug (e.g. one should make a copy of an immutable object to be able to modify it).

Such approach is aligned with the real pyspecs code: aliasing is relatively rare here, due to extensive use of copy operations and domain specifics. We therefore believe that imposing such constraint has a minor impact on how pyspecs are written, while allows to catch certain class of bugs and benefit from automated translation to pure form (without significant code blow up).

Actually, the approach is largely inspired by Rust’s [ownership memory model](https://doc.rust-lang.org/book/ch04-00-understanding-ownership.html), which is built around the same exclusive mutable reference principle. The success of the Rust proves that such restriction is indeed practical: a reasonable memory access discipline allows to obtain memory safety guarantees.

In the post, we first formulate a simple memory model, dubbed “Mutable Forest” Memory Model, which describes the *exclusive mutable reference* principle in a more rigorous way. We discuss motivation for such model. We then discuss how the model can be applied in practice, allowing for richer aliasing without loosing of benefits of the stricter approach.

Since our target language is Python and our main goal is transformation to pure form, we follow a somewhat different route than Rust’s designers, however, the differences are not very significant.

# Mutable Forest Memory Model

## Base memory model assumptions

We assume that memory consists of a set of objects, each object having a set of fields. Each field can either contain a value type (like an atomic type or a structure, like tuple or record) or a reference to an object (can be `nil` too). There can be two reference kinds: a reference to *mutable* objects and a reference to *immutable* ones.

An **immutable object** is an object, which fields and fields of its descendants (reachable via references from it) are not allowed to be modified.

A **mutable object** is an object such that either some its fields can be modified or it has a descendant, which fields can be modified.

**NB** One can distinguish *directly* or *indirectly* mutable object, but this distinction is not important here.

Perhaps contrary to object-oriented languages, we assume that *immutability* is enforced on the reference level rather than on the object level

So, there can be:

- an immutable reference, which cannot be used to modify fields of objects reachable from the reference
- a mutable reference, which allows to modify fields of an object it immediately points to (given that the field is not marked read-only)

Exact implementation details are not specified, but a most straightforward approach is to have a *reference-to-immutable-object* type and if there is a field or a variable of this type, static type checker prevents one from modifying fields reachable from the reference.

One reason to employ such approach is that a mutable object can reach immutable state without explicit conversions, i.e. when there exists no mutable references to it. Under *Safe Aliasing* property specified further, when one obtains an immutable reference, then there exists no mutable references to the object, so one can be sure the object is a truly immutable one.

Note that a mutable object is allowed to have a field pointing to an immutable object. Such field can be modified - contrary to fields of the objects reachable from it, which stay immutable.

## Aliasing

[Aliasing](https://en.wikipedia.org/wiki/Aliasing_(computing)) is a situation where a memory location can be accessed via different symbolic names. In our case, a memory location corresponds to a field (of an object).

**NB** We have discussed *object* references before. We can introduce a related concept of a field reference as a pair of object reference and a field accessor. The latter can be a field name or an index (in a list or an array).

If there are two reference to the same location (i.e. a field of an object), one of them being *mutable*, there can arise an implicit [data dependency](https://en.wikipedia.org/wiki/Data_dependency). In other words, if one updates the location (via the *mutable* reference), then before-update information obtained via aliased references is no longer valid in the after-update memory state.

The situation is potentially dangerous as a bug can be introduced - i.e. an update can unintendedly break an invariant or an assumption in other parts of code, which can access the location via aliases. In order to avoid certain class of bugs and the necessity to re-establish facts and invariants in the after-update memory state, we want to avoid such situations altogether.

**NB** Such situations are sometimes called [data races](https://en.wikipedia.org/wiki/Race_condition#Data_race) in a multi-threading context (see also [here](https://doc.rust-lang.org/book/ch04-02-references-and-borrowing.html#mutable-references)). However, similar problems arise in the single-threaded context too.

We therefore formulate **Safe Aliasing** property (adapted from Rust’s [The Rules of References](https://doc.rust-lang.org/book/ch04-02-references-and-borrowing.html#the-rules-of-references)):

> for any location and at any point of time:
>
>
> either all references to the location are immutable
> or, there is a single (exclusive) mutable reference to it

**NB** Immutable aliasing is not typically a problem, at least from correctness point of view. It can become an obstacle for optimizations though e.g. see [here](https://en.wikipedia.org/wiki/Escape_analysis#Optimizations).

## Mutable Forest Memory Model definition

There is a simple observation, laying in the foundation of our model. Let’s take all objects connected by mutable references. If the **Safe Aliasing** property holds then any mutable object is a part of a tree, since a tree node can have at most one parent (corresponds to a field or a variable holding a reference to the node in our case).

Vice versa, if any mutable object is a part of a tree the **Safe Aliasing** property is effectively enforced.

Since a set of trees is called forest, the set of mutable objects under **Safety Aliasing** property can be seen as a mutable forest.

For simplicity, let’s assume there is a single `<root>` reference, so that only objects reachable from the `<root>` exist (e.g. in a current view/state).

We can now define the **Mutable Forest** memory model as a base model (described above), where all mutable objects constitute a part of a tree (originating from the `<root>` reference). Or, alternatively, as a base model, where **Safe Aliasing** property holds.

## Model properties

### Ownership transfer

A single exclusive reference can be seen as an owner of the object it points to. An ownership can be transferred from one reference to another using an atomic swap operation (e.g. a parallel assignment), which becomes the primary tool for maintaining the *Safe Aliasing* property during memory graph modifications.

### Stack vs Heap

An important property of the model is that it doesn’t explicitly distinguish stack frames and heap objects. This makes the model inconvenient in practice, since one cannot keep a reference to a mutable object both on stack and on heap (in a field of another object) - it will obviously violate the *Safe Aliasing* property.

In practice, it may be necessary to allow on-stack aliasing when passing mutable references to method calls. We will discuss how to deal with such aliases below.

# Use cases

Let’s consider a couple of examples: transformation to pure form and enforcing immutability.

## Transform to pure form

As our target language is Python, we consider two destructive update forms here:

```auto
a.f = 1 # update of a field
c[i] = 1 # update of a list or a dictionary's element
```

One can define non-destructive counterparts, which make and return a copy of the `self` object, where one field or element is affected, while rest left intact, e.g.

```auto
a = a.updated(f = 1)
c = c.updated_at(i, 1)
```

### Nested data structures

One can update nested data structures

```auto
a.f.g = 1
a.c[i] = 2
```

which will look somewhat ugly in the non-destructive case.

```auto
a = a.updated(f = a.f.updated(g = 1))
a = a.updated(c = a.c.updated_at(i, 2))
```

Updates of deeply nested structures will look even more horrible, so one should perhaps consider using Lens/Optics.

### Effect of Aliasing

In presence of aliasing, i.e. two expressions referencing the same location, situation can become more complicated.

For example,

```auto
# assume a.f.g != 1
b = a.f
b.g = 1
assert a.f.g == 1 # shouldn't fail
```

However, one cannot just simply translate the code to

```auto
# assume a.f.g != 1
b = a.f
b = b.updated(g = 1)
assert a.f.g == 1 # fail
```

`b.updated(...)` returns a new version of the object referenced by `b`, whereas, the object referenced by `a` has been left intact.

The problem is that `a.f` and `b` point to the same object, so an update of `b.g` is seen when reading `a.f.g`. One just should propagate changes to aliases in the non-destructive version of the example.

```auto
# assume a.f.g != 1
b = a.f
b = b.updated(g = 1)
# propage changes to aliases
a = a.updated(f = b)
assert a.f.g == 1 # ok now
```

So, one should perform an [alias analysis](https://en.wikipedia.org/wiki/Alias_analys) when transforming an impure code to pure form. Such analysis is not decidable in general though. Restrictions on aliasing should be thus introduced, if a more or less straight-forward translation is desired.

The *Mutable Forest* memory model requires that any mutable reference is exclusive. Thus, if an object field is modified then it is performed using a mutable reference and therefore no other reference (i.e. alias) exist. Thus no information need to be propagated.

## Ensuring immutability

Immutable objects are natural in software engineering, e.g. they can be used to represent facts or express design principles. Inadvertent modification of an object, which should actually be immutable can become a serious problem, which can be difficult to debug. It’s thus tempting to enforce immutability in some way.

One quite common, but error-prone approach is to define a read-only interface to an entity and extend it with a mutating interface (e.g. that can be a `IBeaconState` and `IMutableBeaconState` interfaces in the case of beacon chain implementation). However, such approach can lead to problems in practice, since a code which has a reference to the read-only interface can’t assume it’s an immutable object, it just not allowed to modify the object. But there can exist another reference to the object, which allows modification. Or the read-only interface can be cast to the mutating one.

A safer approach would be to define two related classes: immutable and mutable ones (e.g. `BeaconState` and `MutableBeaconState`), and convert one into another, when necessary. Such approach is slower and less convenient, but can prevent such bugs more reliably.

There can be a third approach, which uses static analysis to determine when an object is safe to modify (e.g. using [typestate analysis](https://en.wikipedia.org/wiki/Typestate_analysis)). For example, initially an object is mutable, however, once it reaches certain state (e.g. it’s assigned to an *immutable* reference), then it becomes immutable and is not allowed to be modified. For example,

```auto
a = A()
a.f = 1 # okay, in a mutable state
b.some_field_marked_immutable = a
# reached immutable state
# a.f = 1 - error now
c = a.f # read access is still ok though
```

In the *Mutable Forest* memory model, any *mutable* reference is exclusive. So, when one assigns the *mutable* reference to an immutable one then the exclusive mutable reference should either be destroyed or cast as an *immutable* reference.

# Practical Considerations

## On-stack aliasing

As noted above, the model itself doesn’t distinguish stack frames and heap objects. Therefore, introducing an on-stack alias for an object referenced from heap and vice versa will violate the *Safe Aliasing* property.

Constraining programs from introducing on-heap aliases is actually fine (at least, in our situation), since tracking heap aliases can be much more problematic.

Tracking on-stack aliases is easier though (given that there are no pointers to stack variables). Moreover, on-stack aliases are often introduced when passing references as parameters to another method: the traditional approach keeps references both on the caller’s stack frame and on the stack frame of the callee. A similar problem can arise when returning a mutable reference.

We therefore propose an extension of the *Mutable Forest* memory model, which allows on-stack aliases. The extension is again largely inspired by the Rust’s [ownership](https://doc.rust-lang.org/book/ch04-00-understanding-ownership.html) memory model. Though there are some differences in our approach to make it more suitable for the subset of Python, employed to express the pyspecs.

## Extended Mutable Forest model

In the extended Mutable Forest model, we assume that the *Safe Aliasing* property still holds for the heap objects, however on-stack aliases can be introduced. That means, heap object graph satisfies the property, if all on-stack aliases are dropped.

In order to simplify alias analysis, we additionally assume that at the beginning of a method call, the *Safe Aliasing* property holds too. It means that when passing a reference to a mutable object as an actual parameter of a method call, its ownership is transferred.

Similarly, when returning a reference to a mutable object as a result of a method call, its ownership is transferred from the callee’s stack frame to the caller’s one. However, since the callee’s stack frame is destroyed after the call is over, it’s not a problem.

### Borrowing vs Claiming

In many cases, it can be natural to transfer ownership of a formal parameter back to the caller. Following the Rust’s [terminology](https://doc.rust-lang.org/book/ch04-02-references-and-borrowing.html), we call such ownership transfer as *borrowing*. However, in our model a method which receives a mutable reference as a parameter is not necessarily obliged to return ownership back. We call such ownership transfer as *claiming* (i.e. claiming ownership of the parameter).

### Casting as immutable ref and back

It can be the case that a reference to an mutable object is passed to a method which expects an immutable reference. In such case, an alternative approach is possible: the mutable reference is cast as an immutable one. So, the caller loses ownership of the object, but can still read its fields - *Safety Aliasing* property allows multiple immutable references.

Additionally, it can be the case that the immutable parameter doesn’t escape the method call (i.e. neither it is returned nor assigned to a field of an escaping object). In that case, after the method invocation is over, the caller becomes the exclusive owner of the object again. Therefore one can cast the immutable reference as a mutable one back.

### On-stack aliases during a method call

The same three approaches can be applied inside a single method call too.

Let’s assume that an on-stack alias is introduced, i.e. either `a = b` or `a = b.f` (`a = b[i]`) statement has been executed. Let’s call `a` as *aliased* variable and `b` as *base* variable - basically, `a` is an alias to a node of the tree that starts from `b`.

At some point of time the *aliased* variable will be destroyed:

- either a method invocation is over
- or the aliased variable is implicitly destroyed because it’s never used after some point in program (i.e. the variable becomes ‘dead’)
- or it’s explicitly destroyed (e.g. by assigning nil or by invoking del a in the Python’s case)

Let’s call the period between alias creation and destruction as *live range* (of the *aliased* variable).

Then again, there can be three cases:

- if the aliased variable has not escaped, then it can borrow ownership when created and return it back to the base variable after the live range is over. The base variable must not be used during the live range, but can be used afterward.
- the aliased variable has escaped, i.e. its ownership has been transferred to another field or variable. Then ownership cannot be returned back to the base variable, which corresponds to claiming case above. The base variable lost ownership and must not be used.
- the aliased variable has escaped via assigning to an immutable field. Then both the base and the aliased variables are cast as immutable references and can be used to read the object fields. The object becomes effectively immutable, as there are no mutable references exist now.

### Assigning to a field of an object

Let’s now consider the `a.f = b` statement. The statement creates an on-heap alias, which can be much more difficult to track. Thus our model disallows introducing such on-heap aliases for objects referenced from stack variables. In order to fulfill the requirement, the on-stack `b` reference should be invalidated after the assignment. For example,

```auto
def meth(a: A):
  b = B()
  b.g = 1
  a.f = b
  # c = b.g - not okay, `b` has been implicitly invalidated
```

## Examples

Here are some examples illustrating how the *Safe Aliasing* property looks like in a Python-like programs.

### borrowing mutable parameter

A callee can mutate a borrowed object and pass it as a *borrowing* parameter to other calls. It is not allowed to escape.

A caller regains full ownership after the call is over.

```auto
def meth(borrow mut a: A) -> A:
  a.f = 1 # can mutate
  meth_b(a) # can pass, if the first parameter of 'meth_b' is borrowing
  b = B()
  # b.g = a - can't do that
  # return a - can't return

a = A()
meth(a)
a.f = 2 # ownership is returned back
```

### claiming mutable parameter

A callee obtains full ownership of the claiming parameter, so such parameter can escape via return or assigning to a field of an escaping object.

After the call is over, the caller cannot use a reference passed as *claiming* parameters.

```auto
def meth(claim mut a: A) -> A:
  a.f = 1
  meth_b(a)
  b = B()
  # b.g = a - is not okay when 'a' will be returned
  return a

a = A()
a2 = meth(a)
# a.f = 1 - is not okay, ownership is lost
# b = a.f - is not okay either
a2.f = 2 # okay, ownerhsip is back via return
```

or

```auto
def meth(claim mut a: A) -> B:
  a.f = 1
  meth_b(a)
  b = B()
  b.g = a
  # meth_b(a) - can't use 'a' anymore
  return b # but it wouldn't be okay to return 'a'

a = A()
b = meth(a)
# a.f = 1 - is not okay again
b.g.f = 1 # okay, ownerhsip is back via return
```

### immutable parameter

An *immutable* parameter of a method forces an actual parameter become an immutable one.

A caller can pass a reference to a mutable object, since it’s an exclusive owner of such object. It loses full ownership, but can still read its fields.

```auto
def meth(immutable a: A) -> B:
  b = B()
  b.f = a # okay if assigning to an immutable ref
  return b

a = A()
a.f = 1
b = meth(a)

b = a.f # okay, it's accessible
# a.f = 1 - not okay, it's an immutable ref
```

# Conclusion

One of the goals to introduce the *Mutable Forest* memory model is to build a foundation for transforming programs with destructive updates into pure form. In general, such conversion can transofrm code so that it would be very difficult to read and/or analyze formally. On the opposite side, if every memory update is performed via an exclusive reference, transformation to pure form results in a code which is much closer to original.

There are still problems in practice, when dealing with the pyspecs code. We will discuss the problems and how they can be resolved in a follow-up post.

## Replies

**norswap** (2021-10-01):

I’ll probably be a bit blunt and I apologize in advance, but I think this is too light on the motivation part.

(1) readability

I read the beacon chain specs and ended up wondering why it was written in this mutable style. I personally very much disagree that it makes the spec more readable. Ben Edgington comments on it in [his annotated spec](https://benjaminion.xyz/eth2-annotated-spec/phase0/beacon-chain/), and it made me pause a couple time.

I do think code like:

```auto
def transform (foo: Structure):
  var new_x = transform_x(foo.x, foo.y)
  var new_y = transform_y(new_x, foo.y)
  return Structure(new_x, new_y)
```

is much better compared to:

```auto
def transform (foo: Structure):
  foo.x = transform_x(foo.x, foo.y)
  foo.y = transform_y(foo.x, foo.y)
```

See how easy it is to miss the implication that the new value of `foo.y` depends on the **new** value of `foo.y`. This only gets worse the more complex methods get.

I’m not excluding there is maybe good case to be made for the simplicity, but it would be nice if it was substantiated with examples.

(2) performance

Here I have three remarks:

1. I’d like to see the performance claim to be substantiated with numbers (and preferably in a language with a decent compiler or JIT compiler, i.e. not Python - maaaybe using pypy).
2. I’d also like to see that the performance for these kinds of transformation is actually a performance concern or bottleneck at all.
3. Why should performance be a concern in the specification? It’s nice to have an executable specification because it’s less ambiguous, it’s more inclusive, and it can be toyed with. I’m not sure performance should be a concern however, especially when we’re talking about (imho small) constant-factor overhead like here. (I do think allowances can be made for complexity if the more readable version is quadratic over a big list for instance).

And I want to stress I’m not a functional programming monk at all! It just seem like a ton of complexity (though, I will grant, fun complexity) to tack onto something whose benefits are dubious (my opinion) in the first place.

---

**ericsson49** (2021-10-01):

[@norswap](/u/norswap) Thanks for your comment!

I do agree that the motivation part can be better.

I perhaps was not good at expressing it clearly, but my idea has been that under some restrictions one can write code with destructive updates and transform it to a pure version. Basically, one can “enjoy” both, if there is a transformation to pure form (which keeps generated code structure close to what one could have written manually).

In the context of Eth2 pyspecs it’s important, since the pyspecs developers have chosen Python (for whatever reasons they have in mind) and they’ve chosen to express it using destructive updates (see e.g. [this](https://github.com/ethereum/consensus-specs/issues/1059#issuecomment-491501031) comment or [this](https://github.com/ethereum/consensus-specs/issues/1059#issuecomment-491585519) one). So, I can take the pyspecs as they are and translate to what I prefer more (e.g. as a Formal Method guy).

In a wider perspective, I believe it’s important too. I personally prefer functional programming paradigm, but still occasionally use destructive updates in some cases:

- updates of nested data structures
- accumulating info when traversing data-structures
- when performance is important

Assuming general audience, I do agree that non-destructive updates of nested data structures look too verbose (e.g. see Vitalik’s comments above). For example, consider an excerpt from [slash_validator](https://github.com/ethereum/consensus-specs/blob/f221674be4d6aad14bbb170efbbbba6a4c58e6cf/specs/phase0/beacon-chain.md#slash_validator):

```auto
validator = state.validators[slashed_index]
validator.slashed = True
validator.withdrawable_epoch = max(validator.withdrawable_epoch, Epoch(epoch + EPOCHS_PER_SLASHINGS_VECTOR))
state.slashings[epoch % EPOCHS_PER_SLASHINGS_VECTOR] += validator.effective_balance
```

In my transformation to pure form it looks something like this:

```auto
validator = state.validators[slashed_index]
state = state.updated(validators = state.validators.updated_at(slashed_index, state.validators[slashed_index].updated(slashed = true)))
state = state.updated(validators = state.validators.updated_at(slashed_index, state.validators[slashed_index].updated(withdrawable_epoch = max(state.validators[slashed_index].withdrawable_epoch, Epoch(epoch + EPOCHS_PER_SLASHINGS_VECTOR)))))
state = state.updated(slashings = state.slashings.updated_at(epoch % EPOCHS_PER_SLASHINGS_VECTOR, state.slashings[epoch % EPOCHS_PER_SLASHINGS_VECTOR] + state.validators[slashed_index].effective_balance))
```

Of course, it can be a bit more concise:

```auto
validator = state.validators[slashed_index]
state = state.set(validators = state.validators.set(slashed_index, validator.set(slashed = true)))
state = state.set(validators = state.validators.set(slashed_index, validator.set(withdrawable_epoch = max(validator.withdrawable_epoch, Epoch(epoch + EPOCHS_PER_SLASHINGS_VECTOR)))))
state = state.set(slashings = state.slashings.set(epoch % EPOCHS_PER_SLASHINGS_VECTOR, state.slashings[epoch % EPOCHS_PER_SLASHINGS_VECTOR] + validator.effective_balance))
```

But it’s still lengthy.

Similarly, traversing data structure while collecting some data (e.g. [filter_block_tree](https://github.com/ethereum/consensus-specs/blob/f221674be4d6aad14bbb170efbbbba6a4c58e6cf/specs/phase0/fork-choice.md#filter_block_tree)) looks more readable with destructive updates, in my opinion.

As for performance, [BeaconState](https://github.com/ethereum/consensus-specs/blob/f221674be4d6aad14bbb170efbbbba6a4c58e6cf/specs/phase0/beacon-chain.md#beaconstate) is full of huge vectors:

```auto
block_roots: Vector[Root, 8192]
state_roots: Vector[Root, 8192]
randao_mixes: Vector[SpecialByteVectorView, 65536]
slashings: Vector[Gwei, 8192]
```

There can be potentially huge lists too:

```auto
historical_roots: List[Root, 16777216]
validators: List[Validator, 1099511627776]
etc
```

So, while indeed it should not be a concern for a specification, it’s a concern for the executable one.

I do agree that the performance impact should be measured. I expect that given the vector sizes it won’t be negligible, even if using persistent data structures.

However, since EF decided to use destructive updates and I can translate them to a pure form, it doesn’t look critical for me. Still good to have. Let me do some experiments.

---

**norswap** (2021-10-01):

I guess my big question is: why not campaign to change the spec to be functional? The linked conversation seems short and open-minded enough that a good case could be made. I think a solution is to simply fork the spec, make it functional but still readable!

I’m still not really convinced that it’s a performance problem. I’m not saying there isn’t, I’m saying that without actually running code, it’s in my experience not really all that clear. (To be clear, I reckon it’s slower, but not sure it’s slow enough that it matters. Since this is a spec, I think that should be enough to trump that consideration.)

---

A bit nitpicky, but since it’s fun to do:

![](https://ethresear.ch/user_avatar/ethresear.ch/ericsson49/48/4680_2.png) ericsson49:

> ```auto
> validator = state.validators[slashed_index]
> validator.slashed = True
> validator.withdrawable_epoch = max(validator.withdrawable_epoch, Epoch(epoch + EPOCHS_PER_SLASHINGS_VECTOR))
> state.slashings[epoch % EPOCHS_PER_SLASHINGS_VECTOR] += validator.effective_balance
> ```

can be rewritten:

```python
validator      = state.validator[slashed_index]
epoch          = max(validator.withdrawable_epoch, Epoch(epoch + EPOCHS_PER_SLASHINGS_VECTOR))
new_validator  = Validator(slashed = True, withdrawable_epoch = epoch, ...) # fill ... as needed
new_validators = state.validators.set(slashed_index, new_validators)
index          = epoch % EPOCHES_PER_SLASHINGS_VECTOR
new_slashing   = state.slashings[index].add(validator.effective_balance)
new_slashings  = state.slashings.set(index, new_slashing)

return State(validators = new_validators, slashings = new_slashings, ...) # fill ... as needed
```

which is less readable for this case, but still readable enough imho.

The added requirements here are these `set` and `add` methods which must return modified copies of the underlying arrays. This can have efficient functional datastructure implementations, but that’s not a spec concern. The naive inefficient definition (copy then set) is a one-liner, and can be given at the start of the spec to explain the semantics.

If the structures are too big, we can imagine copy constructors:

`return new State(base = state, validators = new_validators, slashings = new_slashings)`

---

**ericsson49** (2021-10-01):

I wrote several simple tests in Scala 3, which has decent persistent data structures.

Something like append to a list, update list elements and update simplified BeaconState (which has a list of balances and list of Validators).

The test souce can be found [here](https://gist.github.com/ericsson49/fa4fa9a767bef2ec3cd8cef6666d66c2).

| test name | size | pure time | impure time | slowdown |
| --- | --- | --- | --- | --- |
| list append | 4096 | 240525 ns | 65662 ns | 3.7 |
|  | 8192 | 487984 ns | 125193 ns | 3.9 |
|  | 16384 | 1011154 ns | 254013 ns | 4.0 |
|  | 32768 | 2089448 ns | 514060 ns | 4.1 |
| list update | 4096 | 227630 ns | 49091 ns | 4.6 |
|  | 8192 | 484132 ns | 100428 ns | 4.8 |
|  | 16384 | 1030746 ns | 201762 ns | 5.1 |
|  | 32768 | 2192236 ns | 416478 ns | 5.3 |
| update balance | 4096 | 236758 ns | 52455 ns | 4.5 |
|  | 8192 | 525647 ns | 99047 ns | 5.3 |
|  | 16384 | 1098352 ns | 198503 ns | 5.5 |
|  | 32768 | 2329006 ns | 402757 ns | 5.8 |
| update validator balance | 4096 | 334559 ns | 76188 ns | 4.4 |
|  | 8192 | 718438 ns | 151427 ns | 4.7 |
|  | 16384 | 1486257 ns | 302854 ns | 4.9 |
|  | 32768 | 3147354 ns | 615497 ns | 5.1 |

So, pure versions are about 4-5 times slower than their impure counterparts.

---

**ericsson49** (2021-10-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/norswap/48/6891_2.png) norswap:

> I guess my big question is: why not campaign to change the spec to be functional? The linked conversation seems short and open-minded enough that a good case could be made. I think a solution is to simply fork the spec, make it functional but still readable!

I thought about this but then understood that I could just translate to pure form.

Taking a wider perspective, I’d like to be able to write mostly functional/declarative code but with some imperative bits. Usually, it means that there can be problems with formal method tools, since one have to consider their memory models, make sure they fit one’s needs, adapt/annotate code, etc.

But it turned out that following some discipline (e.g. exclusive mutable references plus limited aliasing), one can transform imperative code into pure version, simlar to what would be written manually.

So, I personally don’t think that it is worth pushing pure functional specification. It could be different, if pyspecs had been written using another language. But if developers are using Python, then limited destructive updates are natural, in my opinion.

---

**ericsson49** (2021-10-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/norswap/48/6891_2.png) norswap:

> I think a solution is to simply fork the spec, make it functional but still readable!

BTW, my colleagues at ConsenSys are re-writing [beacon chain specs in Dafny](https://github.com/ConsenSys/eth2.0-dafny)  and they avoid destructive updates as far as I remember.

---

**hwwhww** (2021-10-04):

Great exploration and write-up! [@ericsson49](/u/ericsson49)

My two wei:

### Readability v.s. Avoiding bad pattern

Personally, I was in favor of non-destructive updates, but I lost. ![:sweat_smile:](https://ethresear.ch/images/emoji/facebook_messenger/sweat_smile.png?v=9)

I still think Option 2 in [ethereum/consensus-specs#1059](https://github.com/ethereum/consensus-specs/issues/1059) would nuke most side effects with *minimal* changes.

- Note that remerkleable now supports state.copy() for deepcopy and we are using it in some specs (1, 2).
- Since state is the only object that we care about mutability in state transition. It could be implemented with a decorator for conciseness.

That would mitigate the side effect *between* functions, but your proposal is more complete to solve it fundamentally. ![:+1:](https://ethresear.ch/images/emoji/facebook_messenger/+1.png?v=9)

### Mutable Forest proposals

- Dumb question, does Python allow def meth(borrow mut a: A) -> A syntax? Or we would end up with decorator @borrow_mut('a')?
- Generally, I like the stricter rules it gives us! I look forward to the follow-up post.
- I’m concerned if the new syntax would make the readers even more confused.

### “The Spec”

Off this topic, but I hope to hear your thoughts or suggestions. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

#### It’s unlikely to make Pyspec perfect

It has been a lot of discussions about if Python is a good language for blockchain specs.

- Pros:

We learned to implement some dark tricks underlying without exposing them to the Markdown files
- Simple and common for most devs. Easier for onboarding.
- Cons:

Side effect
- It’s not formal enough
- It’s slow for test generation

As you mentioned, Dafny is doing an excellent job in creating formal verifiable specs. That made me feel less concerned about the ambiguity in Pyspec. (But of course, we still want to avoid ambiguity in Pyspec!)

#### Long-term to mid-term plans

1. Integrate consensus-specs with execution-specs
2. Support SSZ object forking typings (https://github.com/ethereum/consensus-specs/issues/2360)

p.s. I think [@protolambda](/u/protolambda) favors dealing with (1) before (2) for better integration.

IIUC, execution-specs has extra helpers to handle the mutableness very explicitly. (/cc [@matt](/u/matt))

That would also be a practice that we can consider for consensus-specs. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**ericsson49** (2021-10-04):

Thanks for your comments!

![](https://ethresear.ch/user_avatar/ethresear.ch/hwwhww/48/599_2.png) hwwhww:

> Dumb question, does Python allow def meth(borrow mut a: A) -> A syntax? Or we would end up with decorator @borrow_mut('a')?
> Generally, I like the stricter rules it gives us! I look forward to the follow-up post.
> I’m concerned if the new syntax would make the readers even more confused.

I don’t think Python allows such syntax. I wrote `borrow mut a: A` just to make the examples easier to read, so, it’s a kind of pseudo-Python.

However, I’m able to infer these annotations statically, at least for the subset of Python. One can use an explicit annotation (e.g. as a hint for a reader) too, but it’s not required. Basically, I’ m trying to leave the pyspecs intact as much as possible ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12).

![](https://ethresear.ch/user_avatar/ethresear.ch/hwwhww/48/599_2.png) hwwhww:

> It has been a lot of discussions about if Python is a good language for blockchain specs.
>
>
> Pros:
>
> We learned to implement some dark tricks underlying without exposing them to the Markdown files
> Simple and common for most devs. Easier for onboarding.
>
>
> Cons:
>
> Side effect
> It’s not formal enough
> It’s slow for test generation

I couldn’t decide for me whether it’s good or not (completely agree with your points here). Actually, I once understood that I could just resolve the problems ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12).

I have already done some steps towards this:

- variable declaration inference (i.e. infering missing val/var prefixes).
- type inference
- translators to Java and Kotlin (and WIP translations to Rust/Dafny)

With the addition of the *Mutable Forest* model and the transformation to pure form, I’m able to deal with side effects too (for the subset of Python, but it’s enough in our case).

I can now define formal semantics for the subset of Python by translating it to a language with formal semantics. E.g. that can be Coq, HOL. Or, I have already started to work on translation to Constrain Horn Clauses. It’s perhaps not very satisfactory from formal methods point of view, but it’s practical :).

So, I believe (a subset of) Python *can* be made a decent language for blockchain specs (for distributed protocols, in general), both in theory and in practice. There is still a lot to do to make such approach practical.

But, in my opion, certain reasonable discipline plus customized static analysis makes Python not that bad choice at all :).

---

**ericsson49** (2021-10-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/hwwhww/48/599_2.png) hwwhww:

> Personally, I was in favor of non-destructive updates, but I lost.

Personally, I’d prefer non-destructive updates too.

However:

- Python is an imperative language, so I believe it’s natural to have limited destructive updates, even in a protocol specification.
- my research confirms that (thanks to the disciplined approach of the pyspecs developers) it’s not difficult to deal with

Basically, under some (very reasonable in the case of pyspecs) restrictions, one can enjoy benefits of both approaches. The restrictions can be enforced with static analysis (though I have not impemented them completely yet).

---

**ericsson49** (2021-10-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/hwwhww/48/599_2.png) hwwhww:

> Support SSZ object forking typings (https://github.com/ethereum/consensus-specs/issues/2360 )

I have an idea to implement a (rather unusual) approach that would mix [Nominal](https://en.wikipedia.org/wiki/Nominal_type_system) and [Structural](https://en.wikipedia.org/wiki/Structural_type_system) subtyping. For example, [get_current_epoch](https://github.com/ethereum/consensus-specs/blob/fea3702b3ded8dc1b4f4b05fa4b79298a7d3cb29/specs/phase0/beacon-chain.md#get_current_epoch) requires an instance of `BeaconState`, but only needs `slot` field to be present.

So, the idea is to infer the structural type for the `get_current_epoch`’s paremeter, which would only require that the `slot: Slot` getter is not present. And, in addtion, would require that it should belong to `BeaconState` “familiy” (reguardless of actual phase it belongs too).

So, one can be more flexible with adding/removing/renaming `BeaconState` fields. If they are not required by a method from a prior phase, it’s not a problem (at least from static analysis point of view). And if the prior method does require a presense of a certain field, which is missing or altered in a newer phase, then it should be re-written in this new phase.

And one still catch problems like one has passed `Slot` where an `Epoch` is expected.

