# inputlib: handle python inputs with ease!
cause the input() command is not good enough!

## Intro :metal:

### a brief example

```
>>> import inputlib
>>>
>>> def foo():
...     print("bar :)")
...
>>>
>>> inp = inputlib.PInput()
>>> inp.add_keyword("foo", foo)
>>>
>>> inp.ask()
::>>> foo
bar :)
>>>
```

### available tools

* class: `inputlib.PInput`
* def: `inputlib.getConformation`

<br>

## Docs :v:

### class `inputlib.PInput`
creates a parsable input class

#### :sake: params:

**optional**

`foretext` - *default:* "::>>> " - the text that comes before what the user inputs
<br>

#### :sake: methods:

**:watermelon: `add_keyword`** - adds a usable keyword to the class

#### params:

##### **required**

`keyword` - *string* - adds a keyword to the class

`keyword_callback` - *callable (function, class, if something else callable exists)* - function to be executed when the keyword is entered
    
##### **optional**

`callback_args` - *tuple* - callback function args

`callback_kwargs` - *dict* - callback function keyword args

<br>

**:watermelon: `ask`** - asks with an input

#### params: none
<br>

### def `get_confirmation`
confirms *yes/no* with the user
#### :sake: params: none
