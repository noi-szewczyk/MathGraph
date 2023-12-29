# MathGraph-combat
Welcome to MathGraph!

//тут надо будет рассписать про механику игры, а ниже уже написанно про сами формулы

# functions guide<br>

### avaliable operators:

* '/'=':' - division
* '+' - addition
* '-' - substraction
* '*' - multiplication
* '(' and ')' - parentheses
* '%' - modulo operator

### avaliable functions:
*	abs() - absolute value
*	sqrt() = rt() - square root
*	exp() - exponent function = e^()
*	tan()=tg() - tangent
*	sin() - sinus
*	cos() - cosinus
*	log() = lg() - base  10 logarithm
*	ln - natural logarithm

### avaliable constants:
*	e - Euler's number = 2.718281828459045
*	pi = 3.141592653589793238
	
### Syntax: 
Input is not case-sensitive. It means that `Pi = pi = PI`, `SQRT=sqrt`, `X=x `
but anyway I recommend  not to use caps.

You shouldn't type 'y=' or anything other than numbers, listed operators, functions or constants.

Two types of numbers are supported: 
integer and floating-point (divided via '.')
no complex numbers or anything else!

All operators have the same precedence as in math :
```
	highest ()
	  |	^
	  v  	*/:%
	 low    +,- 
```
Parentheses are optional, but recommended to avoid misinterpretations and to keep the formula 
readable. If a function doesn't have parentheses, it will take the left side expression until firs '+' or '-'
operator will be found (functions have the highest precedence only in relation to '+','-'):
`sin 5*x+1 = sin(5*x)+1`, `sqrt sin 5*x^2 +5 = sqrt(sin(5*x^2))+5`

You can skip the '*' sign between a number and any other object, but only when the number goes first :
`5x=5*x`, `23.1pi=23.1*pi`, `2exp4(x+1)=2*exp 4*(x+1)`
but `x5≠x*5`, `sin(x)3 ≠ sin(x)*3`, `xx ≠ x*x` (error).
or between parentheses: `(x-1)(x+sin x) = (x-1)*(x+sin x)`

White spaces, for instance a space , doen't affect anything, so you can type 
`5*x` as well as `5 * x`, but the names of functions and constants must be separated via space, a parenthes,
 an operator or a number to be interpreted correctly. For instance, you should type `sin x exp x` instead of
`sin xexp x` or even `sinxexpx` (I hope you didn’t plan to do so)

Using multiple operators together is not allowed:
equations `+5`, `5**x`, `pi^^x`, `12--x`,`5+-3x` are incorrect 
but unary '-' is allowed as the first symbol and after '(' :
`-x`, `sin(-exp)` is OK, but `sin -5x` isn't.

':' is equal to '/'

All operators are left-associative, so operators with the same precedence will 
be considered from the left side:
`5x/3/2*pi = (((5*x)/3)/2)*pi`

There's a limit of 50000 for values of value during calculation, all numbers higher (or lower than -50000) will 
be interpreted as (-)50000 + random value [0;10), but you shouldn't notice that. `exp(10x)`for x>9 will always be ~5000.
To avoid an unpredictable behavior, I recommend abstain of using meaningless large multipliers. for instance, `100000000x`
will be rather horizontal line, than expected vertical because of large values was trimmed and the difference between 2 point 
was also annihilated. Same result may give addition off large number to any evaluation: `sin (5x) + 1000000000000`

Modulo operator returns remainder of Donald Knuth's floored division. It means that `-3.4 % 1` will return `0.6` because 
`-3.4-floor(-3.4) = -3.4-(-4) = 0.6`. It's quet hard operator, but very powerful.
