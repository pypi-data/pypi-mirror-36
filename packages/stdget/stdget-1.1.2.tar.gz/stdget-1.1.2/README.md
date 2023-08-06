># StdGet
>StdGet is a small python 2 and 3 compatible library that doesn't require any modules to work.
>
>What does it do?
>
>StdGet's purpose is to be a way to capture the StdOut (Standard Output) and StdErr (Standard Error Output).
>
>Sounds great! How does it work and how do I use it?
>
>>How to use it:
>>
>>First, let's import StdGet:
> `import stdget` 
> Then, let's say we want to capture the StdOut:
> `stdget.startstdoutcapture()`
> And you're done!
> "But how do I get the information it captures?"
> `stdget.stdouthook` will give you a list.
> You can just do `stdget.stdouthook=[]` to empty it.
> 
> >How it works:
> >
> >What it does is it adds a layer on top of the original 'sys.stdout.write' that actually 'takes' the data and copies it into the 'stdget.stdouthook' list.
> It works outside of the module's layer because the sys.stdout / -in and -err are global all across the session.
> That's also why you can just do `import stdget` and you don't have to do `from stdget import *` (it doesn't matter).

