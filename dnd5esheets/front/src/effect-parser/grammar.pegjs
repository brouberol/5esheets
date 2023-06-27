{{
  function EffectExpression(target, operator, equation) {
    return {
      type: 'EffectExpression',
      target,
      operator,
      equation
    }
  }

  function FunctionExpression(id, parameters) {
    return {
      type: 'Function',
      name: id,
      parameters
    }
  }

  function MemberExpression(object, property, computed) {
    return {
      type: 'MemberExpression',
      object,
      property,
      computed
    }
  }

  function BinaryExpression(operator, left, right) {
    return {
      type: 'BinaryExpression',
      operator,
      left,
      right
    }
  }

  function UnaryExpression(value) {
    return {
      type: 'UnaryExpression',
      value
    }
  }

  function NumericLiteral(value) {
    return {
      type: 'Number',
      value: Number(value)
    }
  }

  function operatorReducer (result, element) {
    const left = result;
    const right = element[3];
    const op = element[1];

    return BinaryExpression(op, left, right);
  }
}}

Effects
  = head:Effect _ tail:('\n' @Effect _)* { return [head, ...tail] }

Effect
  = target:Identifier _ operator:AssignmentOperator _ equation:Expression {
      return EffectExpression(target, operator, equation)
    }

Expression
  = head:Term tail:(_ ("+" / "-") _ Term)* {
      return tail.reduce(operatorReducer, head);
    }

Term
  = head:Factor tail:(_ ("*" / "/") _ Factor)* {
      return tail.reduce(operatorReducer, head);
    }

Factor
  = head:Group tail:(_ ("^") _ Factor)* {
      return tail.reduce(operatorReducer, head);
    }

Group
  = _ @Primary _

Primary
  = ParenthesizedExpression
  // / UnaryExpression
  / Function
  / MemberExpression
  / Decimal

// UnaryExpression
//   = '-' expr:Factor { return UnaryExpression(expr) }

ParenthesizedExpression
  = '(' _ @Expression _ ')'

Identifier
  = [a-z_]+ { return text(); }

Decimal
  = _ [0-9]* ('.' [0-9]+)? _ { return NumericLiteral(text()) }

Function
  = id:MemberExpression parameters:CallExpression { return FunctionExpression(id, parameters) }

CallExpression
  = '(' _ head:(@Expression) tail:( _ ',' _ @Expression)* _ ')' { return [head, ...tail] }

MemberExpression
  = head:Identifier
    tail:(
        _ "[" _ property:Expression _ "]" {
          return { property: property, computed: true };
        }
      / _ "." _ property:Identifier {
          return { property: property, computed: false };
        }
    )*
    {
      return tail.reduce(function(object, {property, computed}) {
        return MemberExpression(object, property, computed)
      }, head);
    }

AssignmentOperator
  = ':='
  / '+='
  / '*='
  / '>='
  / '<='

_ 'whitespace'
  = [ \t]*
