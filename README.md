# MathGraph-combat
Welcome to MathGraph!

//тут надо будет расписать про механику игры, а ниже уже написано про сами формулы

# functions guide<br>

### available operators:

* '/'=':' - division
* '+' - addition
* '-' - subtraction
* '*' - multiplication
* '(' and ')' - parentheses
* '%' - modulo operator

### available functions:
*	abs() - absolute value
*	sqrt() = rt() - square root
*	exp() - exponent function = e^()
*	tan()=tg() - tangent
*	sin() - sinus
*	cos() - cosinus
*	log() = lg() - base  10 logarithm
*	ln - natural logarithm

### available constants:
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
* `sin 5*x+1 = sin(5*x)+1`
* `sqrt sin 5*x^2 +5 = sqrt(sin(5*x^2))+5`

You can skip the '*' sign between a number and any other object, but only when the number goes first :
* `5x=5*x`
* `23.1pi=23.1*pi`
* `2exp4(x+1) = 2*exp 4*(x+1)`

but 
* `x5≠x*5`
* `sin(x)3 ≠ sin(x)*3`
* `xx ≠ x*x` (`x x` also won't give `x*x` in result, because
firs `x` is not a number)

Or between parentheses: `(x-1)(x+sin x) = (x-1)*(x+sin x)`. In a similar way, the multiplication sign will be added 
between closing parenthesis and a name of other function or constant: `sin(x) sin(x) = sin(x)*sin(x)`.

White spaces, for instance a space, doesn't affect anything, so you can type 
`5*x` as well as `5 * x`, but the space sign is delimiter, so you must put it between constant or function names if
tere is no any other delimiters: `sin exp x` instead of `sinexpx` (I hope you don't plan to do so). Anyway it's better 
to use parentheses here to avoid mistakes `sin(exp(x))`. Also, `500 000` will
be interpreted as 2 numbers `500` and `0`. Number similarly can separate functions:<br> `sin4cos x = sin 4cos x =
sin(4cos x) = sin(4*cos x) = sin(4*cos(x))`

Using multiple or unnecessary operators is not allowed:
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
`-3.4-floor(-3.4) = -3.4-(-4) = 0.6`. It's quite hard operator, but very powerful. This operator makes a sharp jump,
using which you can go through obstacles, teammates or even enemies! 2 points are connected by red line, but it's not a
part of function, therefore this line hasn't collision.
