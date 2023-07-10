import { createComputed, untrack } from "solid-js";
import {
  EffectExpression,
  FunctionExpression,
  Identifier,
  MemberExpression,
  NumericLiteral,
  parse,
} from "./parser";
import { reconcile } from "solid-js/store";

type Node =
  | BinaryExpression
  | EffectExpression
  | FunctionExpression
  | MemberExpression
  | NumericLiteral;

interface BinaryExpression {
  type: "BinaryExpression";
}

type NodeType = Node["type"];

function get(object: unknown, path: string[]): string | number {
  const [property, ...ancestry] = path;
  return ancestry.length === 0 || object === undefined
    ? object
    : get(object[property], ancestry);
}

const visitors = {
  // EffectExpression: (node: EffectExpression, context: Object, setContext: (context: Partial<Object>) => void): void => {},
  // FunctionExpression: (node: Function): number => {},
  MemberExpression: (node: MemberExpression, context: Object): string => [
    visit(node.object),
    node.computed ? visit(node.property) : evaluate(node.property),
  ],
  // BinaryExpression: (node: BinaryExpression): number => {},
  Identifier: (node: Identifier): string => node.value,
  NumericLiteral: (node: NumericLiteral): number => node.value,
};

const evaluators = {
  EffectExpression: (
    node: EffectExpression,
    context: Object,
    setContext: (context: Partial<Object>) => void,
  ): void => {
    const target = visit(node.target, context, setContext);
    const path = Array.isArray(target) ? target : [target];
    const targetValue = get(context, path);

    createComputed(() => {
      const assignment = evaluate(node.equation, context, setContext);

      // WARNING the targetValue is not (yet) part of the dependencies (for it would be a circular dependency),
      // hence, when the targetValue changes, it doesn't update itself, and can be outdated for comparison operators.
      const operators = {
        ":=": () => setContext(...path, assignment),
        "+=": () => setContext(...path, targetValue + assignment),
        "*=": () => setContext(...path, targetValue * assignment),
        ">=": () =>
          targetValue > assignement &&
          setContext(...path, targetValue * assignment),
        "<=": () =>
          targetValue < assignement &&
          setContext(...path, targetValue * assignment),
      };
      operators[node.operator]();
    });
  },
  FunctionExpression: (node: Function, context: Object): number | string =>
    context[visit(node.name)](
      ...node.parameters.map((parameter) => evaluate(parameter, context)),
    ),
  MemberExpression: (node: MemberExpression, context: Object): unknown =>
    evaluate(node.object, context)[
      (node.computed ? visit : evaluate)(node.property, context)
    ],
  BinaryExpression: (node: BinaryExpression, context: Object): number => {
    const right = evaluate(node.right, context);
    const left = evaluate(node.left, context);

    const operators = {
      "+": () => right + left,
      "-": () => right - left,
      "*": () => right * left,
      "/": () => right / left,
      "^": () => right ** left,
    };

    return operators[node.operator]();
  },
  Identifier: (node: Identifier, context: Object): number | string =>
    context[node.value],
  NumericLiteral: (node: NumericLiteral): number | string => visit(node),
};

function visit(
  node: Node,
  context: Object,
  setContext: (context: Partial<Object>) => void,
) {
  if (!visitors[node.type]) {
    console.log("unknown node type", node);
    throw new Error(`unknown node type ${node.type}.`);
  }

  return visitors[node.type](node, context, setContext);
}

function evaluate(
  node: Node,
  context: Object,
  setContext: (context: Partial<Object>) => void,
) {
  if (!evaluators[node.type]) {
    console.log("unknown node type", node);
    throw new Error(`unknown node type ${node.type}.`);
  }

  return evaluators[node.type](node, context, setContext);
}

export function applyEffect<T extends Object>(
  effect: string,
  context: T,
  setContext: (context: Partial<T>) => void,
) {
  const [effectAst] = parse(effect);
  evaluate(effectAst, context, setContext);
}
