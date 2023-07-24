{{
  function EffectExpression(target, operator, equation) {
    return {
      type: 'EffectExpression' as const,
      target,
      operator,
      equation
    }
  }

  function BinaryExpression(operator, left, right) {
    return {
      type: 'BinaryExpression' as const,
      operator,
      left,
      right
    }
  }  

  function operatorReducer (result, element) {
    const left = result;
    const right = element[3];
    const op = element[1];

    return BinaryExpression(op, left, right);
  }

  function FunctionExpression(id, parameters) {
    return {
      type: 'FunctionExpression' as const,
      name: id,
      parameters
    }
  }

  function MemberExpression(object, property, computed) {
    return {
      type: 'MemberExpression' as const,
      object,
      property,
      computed
    }
  }

  function propertyReducer (result, element) {
    const computed = element[1] === '.';
    const property = element[3];

    return MemberExpression(result, property, computed);
  }

  function Identifier(value) {
    return {
      type: 'Identifier' as const,
      value
    }
  }

  function NumericLiteral(value) {
    return {
      type: 'NumericLiteral' as const,
      value: Number(value)
    }
  }
}}

Effects
  = head:EffectExpression _ tail:('\n' @EffectExpression _)* { return [head, ...tail] }

EffectExpression
  = target:MemberExpression _ operator:AssignmentOperator _ equation:Expression {
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
  / FunctionExpression
  / MemberExpression
  / NumericLiteral

// UnaryExpression
//   = '-' expr:Factor { return UnaryExpression(expr) }

ParenthesizedExpression
  = '(' _ @Expression _ ')'

FunctionExpression
  = id:MemberExpression _ parameters:CallExpression { return FunctionExpression(id, parameters) }

CallExpression
  = '(' _ head:(@Expression) tail:( _ ',' _ @Expression)* _ ')' { return [head, ...tail] }

MemberExpression
  = head:Identifier
    tail:(
        _ "[" _ Expression _ "]"
      / _ "." _ Identifier
    )*
    {
      return tail.reduce(propertyReducer, head)
    }

Identifier
  = [a-zA-Z_]+ { return Identifier(text()); }

NumericLiteral
  = _ [0-9]* ('.' [0-9]+)? _ { return NumericLiteral(text()) }

AssignmentOperator
  = ':='
  / '+='
  / '*='
  / '>='
  / '<='

_ 'whitespace'
  = [ \t]*
