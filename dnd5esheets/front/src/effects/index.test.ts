// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-nocheck
import { describe, expect, test } from 'vitest'

import { computeEffect, applyEffects } from '.'

describe('computeEffect', () => {
  test('creates a static effect', () => {
    const context = { a: 1 }
    const effect = computeEffect('a := 2', context)
    expect(effect).toMatchObject(
      expect.objectContaining({
        target: 'a',
        equation: 2,
        operator: ':=',
      })
    )
    expect(effect.value()).toBe(2)
  })

  test('creates a derived effect', () => {
    const context = { a: 1 }
    const effect = computeEffect('b := a', context)
    expect(effect).toMatchObject(
      expect.objectContaining({
        target: 'b',
        equation: 'a',
        operator: ':=',
      })
    )
    expect(effect.value()).toBe(1)
    context.a = 2
    expect(effect.value()).toBe(2)
  })

  test('creates a nested derived effect', () => {
    const context = { nested: { a: 1 } }
    const effect = computeEffect('b := nested.a', context)
    expect(effect).toMatchObject(
      expect.objectContaining({
        target: 'b',
        equation: 'nested.a',
        operator: ':=',
      })
    )
    expect(effect.value()).toBe(1)
    context.nested.a = 2
    expect(effect.value()).toBe(2)
  })

  test('creates a non-computed nested derived effect', () => {
    const context = { nested: { a: 1 }, key: 'a' }
    const effect = computeEffect('b := nested[key]', context)
    expect(effect).toMatchObject(
      expect.objectContaining({
        target: 'b',
        equation: 'nested.a',
        operator: ':=',
      })
    )
    expect(effect.value()).toBe(1)
    context.nested.a = 2
    expect(effect.value()).toBe(2)
  })

  test('creates a non-computed deeply nested derived effect', () => {
    const context = {
      nested: { a_: { a__: 1 } },
      key_: 'a_',
      key__: 'a__',
    }
    const effect = computeEffect('b := nested[key_][key__]', context)
    expect(effect).toMatchObject(
      expect.objectContaining({
        target: 'b',
        equation: 'nested.a_.a__',
        operator: ':=',
      })
    )
    expect(effect.value()).toBe(1)
    context.nested.a_.a__ = 2
    expect(effect.value()).toBe(2)
  })

  test('creates a effect on a nested target', () => {
    const context = { nested: { a: 1 } }
    const effect = computeEffect('nested.b := nested.a', context)
    expect(effect).toMatchObject(
      expect.objectContaining({
        target: 'nested.b',
        equation: 'nested.a',
        operator: ':=',
      })
    )
    expect(effect.value()).toBe(1)
    context.nested.a = 2
    expect(effect.value()).toBe(2)
  })

  test('creates a static effect containing a Math function', () => {
    const context = {}
    const effect = computeEffect('a := Math.floor(2.4)', context)
    expect(effect).toMatchObject(
      expect.objectContaining({
        target: 'a',
        equation: 'Math.floor(2.4)',
        operator: ':=',
      })
    )
    expect(effect.value()).toBe(2)
  })

  test('creates a derived effect containing a function', () => {
    const context = { id: (i: number) => i }
    const effect = computeEffect('a := id(2)', context)
    expect(effect).toMatchObject(
      expect.objectContaining({
        target: 'a',
        equation: 'id(2)',
        operator: ':=',
      })
    )
    expect(effect.value()).toBe(2)
    context.id = (i: number) => i * 2
    expect(effect.value()).toBe(4)
  })

  test('creates a derived effect containing a function', () => {
    const context = { a: 1, id: (i: number) => i }
    const effect = computeEffect('b := id(a)', context)
    expect(effect).toMatchObject(
      expect.objectContaining({
        target: 'b',
        equation: 'id(a)',
        operator: ':=',
      })
    )
    expect(effect.value()).toBe(1)
    context.a = 2
    context.id = (i: number) => i * 2
    expect(effect.value()).toBe(4)
  })

  test('creates a somewhat complex effect', () => {
    const context = {
      nested: { a: 1, b: 2, c: 3 },
      key: 'c',
    }
    const effect = computeEffect(
      'd := nested.a + Math.min(nested.b, nested[key])',
      context
    )
    expect(effect).toMatchObject(
      expect.objectContaining({
        target: 'd',
        equation: '(nested.a + Math.min(nested.b, nested.c))',
        operator: ':=',
      })
    )
    expect(effect.value()).toBe(3)
    context.nested.a = 2
    expect(effect.value()).toBe(4)
  })
})

describe('applyEffects', () => {
  test('applies one effect', () => {
    const context = { a: 1 }
    const effect = computeEffect('b := a', context)

    expect(applyEffects([effect])).toEqual({
      value: 1,
      history: [
        {
          equation: 'a',
          operator: ':=',
          value: 1,
        },
      ],
    })
  })

  test('combine effects', () => {
    const context = { a: 1 }
    const effects = [
      computeEffect('b *= 3', context),
      computeEffect('b += 2', context),
      computeEffect('b := a', context),
    ]

    expect(applyEffects(effects)).toEqual({
      value: 9,
      history: [
        {
          equation: 'a',
          operator: ':=',
          value: 1,
        },
        {
          appliedValue: 3,
          equation: 2,
          operator: '+=',
          value: 2,
        },
        {
          appliedValue: 9,
          equation: 3,
          operator: '*=',
          value: 3,
        },
      ],
    })
  })

  test('stop applying effects after the first assignment effect', () => {
    const context = { a: 1 }
    const effects = [
      computeEffect('b := 2', context),
      computeEffect('b := a', context),
    ]

    expect(applyEffects(effects)).toEqual({
      value: 2,
      history: [
        {
          equation: 2,
          operator: ':=',
          value: 2,
        },
      ],
    })
  })

  test('apply effects with >= assignment operators', () => {
    const context = { a: 1 }
    const effects = [
      computeEffect('b >= 2', context),
      computeEffect('b >= 0', context),
      computeEffect('b := a', context),
    ]

    expect(applyEffects(effects)).toEqual({
      value: 2,
      history: [
        {
          equation: 'a',
          operator: ':=',
          value: 1,
        },
        {
          appliedValue: 1,
          equation: 0,
          operator: '>=',
          value: 0,
        },
        {
          appliedValue: 2,
          equation: 2,
          operator: '>=',
          value: 2,
        },
      ],
    })
  })

  test('apply effects with <= assignment operators', () => {
    const context = { a: 1 }
    const effects = [
      computeEffect('b <= 0', context),
      computeEffect('b <= 2', context),
      computeEffect('b := a', context),
    ]

    expect(applyEffects(effects)).toEqual({
      value: 0,
      history: [
        {
          equation: 'a',
          operator: ':=',
          value: 1,
        },
        {
          appliedValue: 1,
          equation: 2,
          operator: '<=',
          value: 2,
        },
        {
          appliedValue: 0,
          equation: 0,
          operator: '<=',
          value: 0,
        },
      ],
    })
  })
})
