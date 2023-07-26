import { describe, expect, test } from 'vitest'
import '@testing-library/jest-dom'
import { createStore } from 'solid-js/store'
import { createRoot } from 'solid-js'

import { applyEffect } from '.'

async function inRoot(fn: () => void) {
  await new Promise<void>((resolve) => {
    createRoot((dispose) => {
      fn()
      dispose()
      resolve()
    })
  })
}

describe('apply effect', () => {
  test('applies a static effect', async () =>
    inRoot(() => {
      const [context, setContext] = createStore({ a: 1 })
      applyEffect('a := 2', context, setContext)
      expect(context.a).toBe(2)
    }))

  test('applies a derived effect', async () =>
    inRoot(() => {
      const [context, setContext] = createStore({ a: 1 })
      applyEffect('b := a', context, setContext)
      expect(context.b).toBe(context.a)
    }))

  test('applies a derived effect which updates from its dependency', async () =>
    inRoot(() => {
      const [context, setContext] = createStore({ a: 1 })
      applyEffect('b := a', context, setContext)
      setContext('a', 2)
      expect(context.b).toBe(context.a)
    }))

  test('applies a nested derived effect', async () =>
    inRoot(() => {
      const [context, setContext] = createStore({ nested: { a: 1 } })
      applyEffect('b := nested.a', context, setContext)
      expect(context.b).toBe(context.nested.a)
    }))

  test('applies a nested derived effect which updates from its dependency', async () =>
    inRoot(() => {
      const [context, setContext] = createStore({ nested: { a: 1 } })
      applyEffect('b := nested.a', context, setContext)
      setContext('nested', 'a', 2)
      expect(context.b).toBe(context.nested.a)
    }))

  test('applies a deeply nested derived effect', async () =>
    inRoot(() => {
      const [context, setContext] = createStore({
        deeply: { nested: { a: 1 } },
      })
      applyEffect('b := deeply.nested.a', context, setContext)
      expect(context.b).toBe(context.deeply.nested.a)
    }))

  test('applies a nested derived effect which updates from its dependency', async () =>
    inRoot(() => {
      const [context, setContext] = createStore({
        deeply: { nested: { a: 1 } },
      })
      applyEffect('b := deeply.nested.a', context, setContext)
      setContext('deeply', 'nested', 'a', 2)
      expect(context.b).toBe(context.deeply.nested.a)
    }))

  test('applies a non-computed nested derived effect', async () =>
    inRoot(() => {
      const [context, setContext] = createStore({ nested: { a: 1 }, key: 'a' })
      applyEffect('b := nested[key]', context, setContext)
      expect(context.b).toBe(context.nested.a)
    }))

  test('applies a non-computed nested derived effect which updates from its dependency', async () =>
    inRoot(() => {
      const [context, setContext] = createStore({ nested: { a: 1 }, key: 'a' })
      applyEffect('b := nested[key]', context, setContext)
      setContext('nested', 'a', 2)
      expect(context.b).toBe(context.nested.a)
    }))

  test('applies a non-computed deeply nested derived effect', async () =>
    inRoot(() => {
      const [context, setContext] = createStore({
        nested: { a_: { a__: 1 } },
        key_: 'a_',
        key__: 'a__',
      })
      applyEffect('b := nested[key_][key__]', context, setContext)
      expect(context.b).toBe(context.nested.a_.a__)
    }))

  test('applies a non-computed deeply nested derived effect which updates from its dependency', async () =>
    inRoot(() => {
      const [context, setContext] = createStore({
        nested: { a_: { a__: 1 } },
        key_: 'a_',
        key__: 'a__',
      })
      applyEffect('b := nested[key_][key__]', context, setContext)
      setContext('nested', 'a_', 'a__', 2)
      expect(context.b).toBe(context.nested.a_.a__)
    }))

  test('applies an effect containing a function', async () =>
    inRoot(() => {
      const [context, setContext] = createStore({ id: (i: number) => i })
      applyEffect('a := id(2)', context, setContext)
      expect(context.a).toBe(2)
    }))

  test('applies a derived effect containing a function', async () =>
    inRoot(() => {
      const [context, setContext] = createStore({ a: 1, id: (i: number) => i })
      applyEffect('b := id(a)', context, setContext)
      expect(context.b).toBe(context.a)
    }))

  test('applies a derived effect containing a function which updates from its dependency', async () =>
    inRoot(() => {
      const [context, setContext] = createStore({ a: 1, id: (i: number) => i })
      applyEffect('b := id(a)', context, setContext)
      setContext('a', 2)
      expect(context.b).toBe(context.a)
    }))

  test('applies a somewhat complex effect which updates from its dependency', async () =>
    inRoot(() => {
      const [context, setContext] = createStore({
        nested: { a: 1, b: 2, c: 3 },
        key: 'c',
        min: Math.min,
      })
      applyEffect(
        'd := nested.a + min(nested.b, nested[key])',
        context,
        setContext
      )
      setContext('nested', 'a', 2)
      expect(context.d).toBe(4)
    }))

  test('applies a somewhat complex effect on a nested target which updates from its dependency', async () =>
    inRoot(() => {
      const [context, setContext] = createStore({
        nested: { a: 1, b: 2, c: 3 },
        key: 'c',
        min: Math.min,
        effect: {},
      })
      applyEffect(
        'effect.d :=  nested.a + min(nested.b, nested[key])',
        context,
        setContext
      )
      setContext('nested', 'a', 2)
      expect(context.effect.d).toBe(4)
    }))

  test('applies a nested derived effect on a sibling target which updates from its dependency', async () =>
    inRoot(() => {
      const [context, setContext] = createStore({
        nested: { a: 1, b: 2, c: 3 },
        key: 'c',
        min: Math.min,
      })
      applyEffect('nested.d := nested.a', context, setContext)
      setContext('nested', 'a', 2)
      expect(context.nested.d).toBe(context.nested.a)
    }))

  // solid-js store doesn't seem to accept updates of functions
  test.skip('applies a derived effect containing a function which updates from its dependency', async () =>
    inRoot(() => {
      const [context, setContext] = createStore({ a: 1, id: (i: number) => i })
      applyEffect('b := id(a)', context, setContext)
      setContext('id', (i: number) => i + 1)
      expect(context.b).toBe(context.a + 1)
    }))
})
