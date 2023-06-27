import { parse } from ".";

describe("effect parser", () => {
  test.each([
    // Simple operations
    [
      "a := a + b",
      [
        {
          type: "EffectExpression",
          target: "a",
          operator: ":=",
          equation: {
            operator: "+",
            left: "a",
            right: "b",
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
            left: "a",
            operator: "-",
            right: "b",
            type: "BinaryExpression",
          },
          operator: ":=",
          target: "a",
          type: "EffectExpression",
        },
      ],
    ],
    [
      "a := 1 + 2",
      [
        {
          equation: {
            left: { type: "Number", value: 1 },
            operator: "+",
            right: { type: "Number", value: 2 },
            type: "BinaryExpression",
          },
          operator: ":=",
          target: "a",
          type: "EffectExpression",
        },
      ],
    ],
    [
      "a := 1 + 2 * 3 ^ 4",
      [
        {
          equation: {
            left: { type: "Number", value: 1 },
            operator: "+",
            right: {
              operator: "*",
              left: { type: "Number", value: 2 },
              right: {
                left: {
                  type: "Number",
                  value: 3,
                },
                operator: "^",
                right: {
                  type: "Number",
                  value: 4,
                },
                type: "BinaryExpression",
              },
              type: "BinaryExpression",
            },
            type: "BinaryExpression",
          },
          operator: ":=",
          target: "a",
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
                  type: "Number",
                  value: 3,
                },
                operator: "^",
                right: {
                  type: "Number",
                  value: 4,
                },
                type: "BinaryExpression",
              },
              operator: "*",
              right: {
                type: "Number",
                value: 2,
              },
              type: "BinaryExpression",
            },
            operator: "+",
            right: {
              type: "Number",
              value: 1,
            },
            type: "BinaryExpression",
          },
          operator: ":=",
          target: "a",
          type: "EffectExpression",
        },
      ],
    ],
    [
      "a := min(a, b)",
      [
        {
          equation: {
            name: "min",
            parameters: ["a", "b"],
            type: "Function",
          },
          operator: ":=",
          target: "a",
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
              name: "min",
              parameters: ["a", "b"],
              type: "Function",
            },
            operator: "+",
            right: "c",
            type: "BinaryExpression",
          },
          operator: ":=",
          target: "a",
          type: "EffectExpression",
        },
      ],
    ],
    [
      "a := a.b.c",
      [
        {
          equation: {
            computed: false,
            object: {
              computed: false,
              object: "a",
              property: "b",
              type: "MemberExpression",
            },
            property: "c",
            type: "MemberExpression",
          },
          operator: ":=",
          target: "a",
          type: "EffectExpression",
        },
      ],
    ],
    [
      "a := a[b].c",
      [
        {
          equation: {
            computed: false,
            object: {
              computed: true,
              object: "a",
              property: "b",
              type: "MemberExpression",
            },
            property: "c",
            type: "MemberExpression",
          },
          operator: ":=",
          target: "a",
          type: "EffectExpression",
        },
      ],
    ],
    [
      "a := a[min(b, d)].c",
      [
        {
          equation: {
            computed: false,
            object: {
              computed: true,
              object: "a",
              property: {
                name: "min",
                parameters: ["b", "d"],
                type: "Function",
              },
              type: "MemberExpression",
            },
            property: "c",
            type: "MemberExpression",
          },
          operator: ":=",
          target: "a",
          type: "EffectExpression",
        },
      ],
    ],
  ])("parses simple arithmetic expressions (%s)", (effects, expectedResult) => {
    expect(parse(effects)).toEqual(expectedResult);
  });
});
