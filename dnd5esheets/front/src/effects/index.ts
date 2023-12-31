// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-nocheck
import {
  AssignmentOperator,
  EffectExpression,
  FunctionExpression,
  Identifier,
  MemberExpression,
  NumericLiteral,
  parse,
} from './parser'

type Node =
  | BinaryExpression
  | EffectExpression
  | FunctionExpression
  | MemberExpression
  | NumericLiteral

interface BinaryExpression {
  type: 'BinaryExpression'
  right: Node
  left: Node
  operator: string
}

function get(object: unknown, path: string[]): unknown {
  const [property, ...ancestry] = path
  return path.length === 0 || object === undefined
    ? object
    : get(object[property], ancestry)
}

const serializers = {
  BinaryExpression: (node: BinaryExpression, context: object): string => {
    const right = display(node.right, context)
    const left = display(node.left, context)

    return `(${left} ${node.operator} ${right})`
  },
  // EffectExpression: (node: EffectExpression, context: object, setContext: (context: Partial<object>) => void): void => {},
  FunctionExpression: (node: FunctionExpression, context: object): string =>
    `${display(node.name, context)}(${node.parameters
      .map((parameter) => display(parameter, context))
      .join(', ')})`,
  MemberExpression: (node: MemberExpression, context: object): string =>
    [
      display(node.object, context),
      node.computed
        ? display(node.property, context)
        : evaluate(node.property, context),
    ].join('.'),
  // BinaryExpression: (node: BinaryExpression): number => {},
  Identifier: (node: Identifier): string => node.value,
  NumericLiteral: (node: NumericLiteral): number => node.value,
}

const visitors = {
  // EffectExpression: (node: EffectExpression, context: object, setContext: (context: Partial<object>) => void): void => {},
  // FunctionExpression: (node: Function): number => {},
  MemberExpression: (node: MemberExpression, context: object): string[] => [
    visit(node.object, context, context),
    node.computed
      ? visit(node.property, context)
      : evaluate(node.propert, context),
  ],
  // BinaryExpression: (node: BinaryExpression): number => {},
  Identifier: (node: Identifier): string => node.value,
  NumericLiteral: (node: NumericLiteral): number => node.value,
}

const evaluators = {
  EffectExpression: (node: EffectExpression, context: object) => {
    return {
      equation: display(node.equation, context),
      operator: node.operator,
      target: display(node.target, context),
      value: () => evaluate(node.equation, context),
    }
  },
  FunctionExpression: (
    node: FunctionExpression,
    context: object
  ): number | string => {
    const name = visit(node.name, context)
    const path = Array.isArray(name) ? name : [name]

    // TODO allow to provide function context
    const [root, ...restPath] = path
    const fn = root === 'Math' ? get(Math, restPath) : get(context, path)
    return fn(
      ...node.parameters.map((parameter) => evaluate(parameter, context))
    )
  },
  MemberExpression: (node: MemberExpression, context: object): unknown =>
    evaluate(node.object, context)[
      (node.computed ? visit : evaluate)(node.property, context)
    ],
  BinaryExpression: (node: BinaryExpression, context: object): number => {
    const right = evaluate(node.right, context)
    const left = evaluate(node.left, context)

    const operators = {
      '+': () => left + right,
      '-': () => left - right,
      '*': () => left * right,
      '/': () => left / right,
      '^': () => left ** right,
    }

    return operators[node.operator]()
  },
  Identifier: (node: Identifier, context: object): number | string =>
    context[node.value],
  NumericLiteral: (node: NumericLiteral): number | string => visit(node),
}

function display(node: Node, context: object) {
  if (!serializers[node.type]) {
    console.log('unknown node type', node)
    throw new Error(`unknown node type ${node.type}.`)
  }

  return serializers[node.type](node, context)
}

function visit(node: Node, context: object) {
  if (!visitors[node.type]) {
    console.log('unknown node type', node)
    throw new Error(`unknown node type ${node.type}.`)
  }

  return visitors[node.type](node, context)
}

function evaluate(node: Node, context: object) {
  if (!evaluators[node.type]) {
    console.log('unknown node type', node)
    throw new Error(`unknown node type ${node.type}.`)
  }

  return evaluators[node.type](node, context)
}

export function computeEffect<T extends object>(effect: string, context: T) {
  const [effectAst] = parse(effect)
  return evaluate(effectAst, context)
}

export interface Effect<Target> {
  equation: string
  operator: AssignmentOperator
  target: Target
  value: () => number
}

export type ComputedEffect =
  | {
      equation: string
      operator: ':='
      value: number
    }
  | {
      equation: string
      operator: Exclude<AssignmentOperator, ':='>
      value: number
      appliedValue: number
    }

const operatorFunctor: Record<
  Exclude<AssignmentOperator, ':='>,
  (currentValue: number, nextValue: number) => number
> = {
  '+=': (currentValue, nextValue) => currentValue + nextValue,
  '*=': (currentValue, nextValue) => currentValue * nextValue,
  '>=': (currentValue, nextValue) =>
    currentValue > nextValue ? currentValue : nextValue,
  '<=': (currentValue, nextValue) =>
    currentValue < nextValue ? currentValue : nextValue,
}

export function applyEffects<Target>(effects: Effect<Target>[]): {
  value: number
  history: ComputedEffect[]
} {
  const [effect, ...rest] = effects

  if (!effect) {
    return {
      value: 0,
      history: [],
    }
  }

  const { operator, equation } = effect
  const computedValue = effect.value()
  const computedEffect = {
    operator,
    equation,
    value: computedValue,
  }

  if (effect.operator === ':=') {
    return {
      value: computedValue,
      history: [{ ...computedEffect, operator: effect.operator }],
    }
  }

  const nextEffect = applyEffects(rest)
  const appliedValue = operatorFunctor[effect.operator](
    effect.value(),
    nextEffect.value
  )

  return {
    value: appliedValue,
    history: [...nextEffect.history, { ...computedEffect, appliedValue }],
  }
}
