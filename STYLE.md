# Stylistic Choices in this Course

There are a few questions of technical style in this course that I think need a few words explanation...

## HTML syntax

I have opted for the XML-style closing of empty elements: `<img />` instead of just `<img>` (or I suppose, `<img></img>`). This helps keep the "all tags get closed" rule consistent, and makes the empty tags more obvious which I think helps beginners.

Also an informal poll of some web developers said that many of whom said they use the XML syntax themselves, so I'm not totally out to lunch here.

## CSS colours

I use the three-character CSS colour codes (`#f70`) rather than six (`#ff7700`) because experience tells me that beginners can work with them without delving into a big explanation of hexadecimal.

I use the word "colour" because I'm Canadian. Admittedly, that's possibly confusing, but my fingers won't type anything else.

## JS syntax

I have made what are may seem like odd choices for the first steps at JavaScript syntax.

Taking a cue from John Resig's [JavaScript as a First Language](http://ejohn.org/blog/javascript-as-a-first-language/), I use only the `do_something = function(){}` syntax for function definitions. This makes every object-creation operation consistently a `variable = ...` statement, which minimizes new syntax and emphasises that functions are values.

It also means the anonymous function definition syntax is there ready to go when we want to use it for callbacks.

But I'm not using the inline anonymous function right away either, instead starting with:

```javascript
handle_click = function(){...}
$('#foo').click(handle_click)
```

This keeps the amount of stuff happening in one statement to a minimum, so it's easier to explain and digest. It also keeps the way functions get defined consistent while we're opening that door.

Similarly, I have generally erred on the side of putting something in a variable where it saves doing two or three things in one line.

```javascript
angle = ...
trans = 'r' + angle
attribs = {
  'transform': trans
}
shape.animate(attribs, 1000)
```

I didn't start with the jQuery `$`. I think spelling it `jQuery` is easier since it looks like other function names.

```javascript
handle_click = function(){...}
jQuery('#foo').click(handle_click)
```

The equivalence `jQuery === $` is introduced later for brevity and comprehensibility of other jQuery code.

### Anti-Styles

There are a few notable JavaScript styles used in this Guide that are definitely not considered best practices. Each of these is done deliberately to minimize the amount of syntax and complication introduced.

* statements do not end with `;`
* `var` is not introduced: all variables are global
* type coercion is allowed to happen: explicit conversions and `===` are not introduced.

In each case, if this was a full course in programming, I would certainly take the opposite position. As it is, with only about 6 weeks of programming time, my emphasis was on getting familiar with the way logic fits together to create behaviour. Extra syntax or concepts were purged mercilessly, even at the expense of creating non-strict or non-lint-clean code.
