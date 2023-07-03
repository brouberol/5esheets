import { parse } from ".";

describe("effect parser", () => {
  test.each([
    // Simple operations
    [
      "a := a + b",
      [
        {
          type: "EffectExpression",
          target: {
            type: "Identifier",
            value: "a",
          },
          operator: ":=",
          equation: {
            operator: "+",
            left: {
              type: "Identifier",
              value: "a",
            },
            right: {
              type: "Identifier",
              value: "b",
            },
            type: "BinaryExpression",
          },
        },
      ],
    ],
    [
      "a := a - b",
      [
        {
          equation: {
            left: {
              type: "Identifier",
              value: "a",
            },
            operator: "-",
            right: {
              type: "Identifier",
              value: "b",
            },
            type: "BinaryExpression",
          },
          operator: ":=",
          target: {
            type: "Identifier",
            value: "a",
          },
          type: "EffectExpression",
        },
      ],
    ],
    [
      "a := 1 + 2",
      [
        {
          equation: {
            left: { type: "NumericLiteral", value: 1 },
            operator: "+",
            right: { type: "NumericLiteral", value: 2 },
            type: "BinaryExpression",
          },
          operator: ":=",
          target: {
            type: "Identifier",
            value: "a",
          },
          type: "EffectExpression",
        },
      ],
    ],

    // Operator precedence
    [
      "a := 1 + 2 * 3 ^ 4",
      [
        {
          equation: {
            left: { type: "NumericLiteral", value: 1 },
            operator: "+",
            right: {
              operator: "*",
              left: { type: "NumericLiteral", value: 2 },
              right: {
                left: {
                  type: "NumericLiteral",
                  value: 3,
                },
                operator: "^",
                right: {
                  type: "NumericLiteral",
                  value: 4,
                },
                type: "BinaryExpression",
              },
              type: "BinaryExpression",
            },
            type: "BinaryExpression",
          },
          operator: ":=",
          target: {
            type: "Identifier",
            value: "a",
          },
          type: "EffectExpression",
        },
      ],
    ],
    [
      "a := 3 ^ 4 * 2 + 1",
      [
        {
          equation: {
            left: {
              left: {
                left: {
                  type: "NumericLiteral",
                  value: 3,
                },
                operator: "^",
                right: {
                  type: "NumericLiteral",
                  value: 4,
                },
                type: "BinaryExpression",
              },
              operator: "*",
              right: {
                type: "NumericLiteral",
                value: 2,
              },
              type: "BinaryExpression",
            },
            operator: "+",
            right: {
              type: "NumericLiteral",
              value: 1,
            },
            type: "BinaryExpression",
          },
          operator: ":=",
          target: {
            type: "Identifier",
            value: "a",
          },
          type: "EffectExpression",
        },
      ],
    ],

    // Function call
    [
      "a := min(a, b)",
      [
        {
          equation: {
            name: {
              type: "Identifier",
              value: "min",
            },
            parameters: [
              {
                type: "Identifier",
                value: "a",
              },
              { type: "Identifier", value: "b" },
            ],
            type: "FunctionExpression",
          },
          operator: ":=",
          target: {
            type: "Identifier",
            value: "a",
          },
          type: "EffectExpression",
        },
      ],
    ],
    [
      "a := min(a, b) + c",
      [
        {
          equation: {
            left: {
              name: {
                type: "Identifier",
                value: "min",
              },
              parameters: [
                {
                  type: "Identifier",
                  value: "a",
                },
                { type: "Identifier", value: "b" },
              ],
              type: "FunctionExpression",
            },
            operator: "+",
            right: { type: "Identifier", value: "c" },
            type: "BinaryExpression",
          },
          operator: ":=",
          target: {
            type: "Identifier",
            value: "a",
          },
          type: "EffectExpression",
        },
      ],
    ],

    // Property access
    [
      "a := a.b.c",
      [
        {
          equation: {
            computed: true,
            object: {
              computed: true,
              object: { type: "Identifier", value: "a" },
              property: { type: "Identifier", value: "b" },
              type: "MemberExpression",
            },
            property: { type: "Identifier", value: "c" },
            type: "MemberExpression",
          },
          operator: ":=",
          target: {
            type: "Identifier",
            value: "a",
          },
          type: "EffectExpression",
        },
      ],
    ],

    // Indirect property access
    [
      "a := a[b].c",
      [
        {
          equation: {
            computed: true,
            object: {
              computed: false,
              object: { type: "Identifier", value: "a" },
              property: { type: "Identifier", value: "b" },
              type: "MemberExpression",
            },
            property: { type: "Identifier", value: "c" },
            type: "MemberExpression",
          },
          operator: ":=",
          target: {
            type: "Identifier",
            value: "a",
          },
          type: "EffectExpression",
        },
      ],
    ],
    [
      "a := a[min(b, d)].c",
      [
        {
          equation: {
            computed: true,
            object: {
              computed: false,
              object: { type: "Identifier", value: "a" },
              property: {
                name: {
                  type: "Identifier",
                  value: "min",
                },
                parameters: [
                  { type: "Identifier", value: "b" },
                  { type: "Identifier", value: "d" },
                ],
                type: "FunctionExpression",
              },
              type: "MemberExpression",
            },
            property: { type: "Identifier", value: "c" },
            type: "MemberExpression",
          },
          operator: ":=",
          target: {
            type: "Identifier",
            value: "a",
          },
          type: "EffectExpression",
        },
      ],
    ],
  ])("parses simple arithmetic expressions (%s)", (effects, expectedResult) => {
    expect(parse(effects)).toEqual(expectedResult);
  });
});
